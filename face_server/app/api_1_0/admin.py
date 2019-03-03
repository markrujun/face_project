from app.api_1_0 import api
from app.models import Event, Admin, User
from flask import jsonify, request, g, current_app
from app import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet
from werkzeug.datastructures import FileStorage
from flask_restful import Api, Resource, reqparse
from app.api_1_0.user import encrypt_filename, decrypt_filename
from sqlalchemy import func
import json
import zipfile
import rarfile
import os
import datetime
from config import basedir

base_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme='adminToken')

API = Api(api)


def systemPhotoToUrl(photoname):
    return current_app.config["HOST"] + "resources/"+current_app.config["PHOTO_DIR"] +"/systemPhoto/"+ photoname + current_app.config["PHOTO_FORMAT"]


def uploadPhotoToUrl(photoname):
    return current_app.config["HOST"] + "resources/"+current_app.config["PHOTO_DIR"] +"/uploadPhoto/"+ photoname + current_app.config["PHOTO_FORMAT"]


@base_auth.verify_password
def verify_password(adminname, password):
    admin = Admin.query.filter_by(adminname = adminname).first()
    if admin:
        if admin.verify_password(password):
            g.admin = admin
            return True
    return False


@token_auth.verify_token
def verify_token(token):
    g.admin = None
    s = Serializer(current_app.config["SECRET_KEY"])
    try:
        adminname = s.loads(token)
        print(adminname)
        g.admin = Admin.query.filter_by(adminname = adminname['adminname']).first()
    except:
        return False
    return True


@token_auth.error_handler
def token_error():
    return jsonify({"message":"token not correct", "code": 401}), 201


@base_auth.error_handler
def base_error():
    return jsonify({"message":"password not correct", "code": 401}), 201


class AdminAuth(Resource):
    @base_auth.login_required
    def get(self):
        if g.admin:
            token = g.admin.generate_auth_token()
            return jsonify({"token": str(token, encoding="utf-8"), "code": 201})
        else: 
            return jsonify({"message": "Login failed", "code": 401}), 200


# 单个审核记录
class checkItem(Resource):
    # 审核员获取审核照片
    @token_auth.login_required
    def get(self):
        admin = g.admin
        if admin:
            uncheckUser = User.query.filter_by(lastStatus=2).order_by(func.rand()).first()
            if uncheckUser:
                try:
                    uncheckEvent = Event.query.filter_by(username = uncheckUser.username).order_by(Event.time.desc()).first()
                    uncheckUser.lastStatus = 3
                    return jsonify({'id': uncheckEvent.id, 'originPhotoUrl': systemPhotoToUrl(uncheckUser.photoName), 'eventPhotoUrl': uploadPhotoToUrl(uncheckEvent.uploadPhotoName), "code":200})
                except:
                    return jsonify({"code": 500})
            else:
                return jsonify({"code": 204})
        else:
            return jsonify({"code": 401})
    # 审核员审核
    @token_auth.login_required
    def post(self):
        admin = g.admin
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        parser.add_argument('pass', type=bool, required=True)
        parser.add_argument('mark', type=str, required=True)
        args = parser.parse_args()
        event_id = args['id']
        oldEvent = Event.query.filter_by(id=event_id).first()
        oldEvent.adminname = admin.adminname
        lastEvent = Event.query.filter_by(username = oldEvent.username).order_by(Event.time.desc()).first()
        print(lastEvent.id)
        if lastEvent.status is not 2:
            print(lastEvent.status)
            return jsonify({"code":202, "message": "已经被审核"})
        ispass = args['pass']
        print(ispass)
        if ispass:
            newEvent = Event(id=Event.query.with_entities(Event.id).count()+1, username = oldEvent.username, uploadPhotoName = oldEvent.uploadPhotoName, status=4, adminname = g.admin.adminname, confidence=oldEvent.confidence)
        else:
            mark = args['mark']
            newEvent = Event(id=Event.query.with_entities(Event.id).count()+1, username = oldEvent.username, uploadPhotoName = oldEvent.uploadPhotoName, status=3, adminname = g.admin.adminname, mark = mark, confidence=oldEvent.confidence)
        try:
            db.session.add(newEvent)
            db.session.commit()
            user = User.query.filter_by(username = newEvent.username).first()
            user.lastStatus = newEvent.status
            return jsonify({"code": 201, "message": "success check"})
        except:
            return jsonify({"code": 500, "message": "无法写入数据库"})
    # 管理员修改状态
    @token_auth.login_required
    def put(self):
        admin = g.admin
        if admin.permission == 2:
            parser = reqparse.RequestParser()
            parser.add_argument('username',type=str, required=True)    
            parser.add_argument('status',type=str, required=True)    
            parser.add_argument('remark',type=str, required=True)
            args = parser.parse_args()
            lastEvent = Event.query.filter_by(username=args.username).order_by(Event.time.desc()).first()
            newEvent = Event(id = Event.query.with_entities(Event.id).count()+1, username = lastEvent.username, uploadPhotoName = lastEvent.uploadPhotoName, status=args['status'], adminname = admin.adminname, mark = args['remark'], confidence = lastEvent.confidence)    
            user = User.query.filter_by(username = args['username']).first()
            print(args['status'])
            if(int(args['status'])==2):
                user.lastStatus = 2
            else:
                print('test')
                user.lastStatus = int(args['status']) + 1
            try:
                db.session.add(newEvent)
                db.session.commit()
                return jsonify({"code":201,"message":"success check"})
            except:
                return jsonify({"code":500,"message":"无法写入数据库"})
        else:
            return jsonify({"code":403,"message":"权限不够！"})

## 获取审核列表
class checkList(Resource):
    @token_auth.login_required
    def get(self):
        if g.admin.permission == 2:
            allCheckList = Event.query.order_by(Event.time.desc()).all()
            checkList = []
            tempUserList = []
            for i in allCheckList:
                if(i.username in tempUserList):
                    pass
                else:
                    tempUserList.append(i.username)
                    user = User.query.filter_by(username=i.username).first()
                    if user:
                        checkList.append({"username":i.username, "name": user.name, "systemPhoto": systemPhotoToUrl(user.photoName), "uploadPhoto": uploadPhotoToUrl(i.uploadPhotoName), "status": i.status, "confidence": i.confidence, "time": i.time.strftime('%c'), "auditor": i.adminname, "remark":i.mark})
            return jsonify({"checkList":checkList, "code": 201})
        else:
            return jsonify({"code": 403, "message":"权限不足"})


## 用户列表
class userTable(Resource):
    @token_auth.login_required
    def get(self):
        allUsers = User.query.all()
        allUsersList = []
        for i in allUsers:
            allUsersList.append(dict(username = i.username, photoUrl = systemPhotoToUrl(i.photoName)))
        return jsonify({"userList":allUsersList, "code": 200})
    
    ## 添加用户 type： 1--单个添加， 2--批量添加
    @token_auth.login_required
    def post(self):
        admin = g.admin
        if admin.permission == 2:
            parser = reqparse.RequestParser()
            parser.add_argument('photo',  type=FileStorage, location=['files','form'])
            parser.add_argument('password', type=str)
            parser.add_argument('username', type=str)
            parser.add_argument('type', type=int, required=True)
            parser.add_argument('data')
            parser.add_argument('zipFile', type=FileStorage, location=['files','form'])
            args = parser.parse_args()
            ## 单个添加
            if args.type == 1:
                user = User.query.filter_by(username = args.username).first()
                if user:
                    return jsonify({"code": 409, "message":"用户已存在"})
                else:
                    path = basedir+"/resources/"+current_app.config["PHOTO_DIR"]+"/systemPhoto/"
                    tempFilename = secure_filename(encrypt_filename(args.username+'system'))
                    tempFilepath = path + tempFilename+current_app.config["PHOTO_FORMAT"]
                    args.photo.save(tempFilepath)
                    newUser = User(username=args.username, password=args.password,photoName=tempFilename)
                    try:
                        db.session.add(newUser)
                        db.session.commit()
                        return jsonify({"code": 201, "message":"创建成功！"})
                    except:
                        return jsonify({"code": 503, "message": "无法写入数据库！" })
            ## 批量添加
            elif args.type == 2:
                zipFilename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                zipFilepath = basedir+"/resources/" + current_app.config["PHOTO_DIR"] + "/zipFile/" + zipFilename
                args.zipFile.save(zipFilepath)
                data = json.loads(args.data)
                failedList = []
                successList = []
                ## rar格式压缩包
                try:
                    ziper = rarfile.RarFile(zipFilepath)
                    os.rename(zipFilepath, zipFilepath+'.rar')
                    ziper.extractall(path=basedir+"/resources/"+current_app.config["PHOTO_DIR"]+"/systemPhoto/")
                except:
                    ## zip格式压缩包
                    try:
                        ziper = zipfile.ZipFile(zipFilepath)
                        os.rename(zipFilepath, zipFilepath+'.zip')
                        ziper.extractall(path=basedir+"/resources/"+current_app.config["PHOTO_DIR"]+"/systemPhoto/")
                        print(ziper.namelist())
                    except:
                            return jsonify({"code": 400, "message":"创建失败，无法处理的压缩类型！"})
                ## 添加用户，加密图片名
                for i in data:
                    try:
                        filename = secure_filename(encrypt_filename(i["photoName"]+"system")) + current_app.config["PHOTO_FORMAT"]
                        if(User.query.filter_by(username=i["username"]).first()):
                            raise Exception
                        newUser = User(username=i["username"], photoName = filename, name = i["name"], password = i["password"])
                        os.rename(basedir+"/resources/"+current_app.config["PHOTO_DIR"]+"/systemPhoto/" + i["photoName"] + current_app.config["PHOTO_FORMAT"],basedir+"/resources/"+current_app.config["PHOTO_DIR"]+"/systemPhoto/"+ filename)
                        db.session.add(newUser)
                        db.session.commit()
                        successList.append(i["username"])
                    except:
                        print("failed")
                        failedList.append(i["username"])
                return jsonify({"code": 201, "message": "处理完成", "successList": successList, "failedList": failedList})
        else:
            return jsonify({"code":403,"message":"权限不够！"})
    @token_auth.login_required
    def delete(self):
        admin = g.admin
        if admin.permission == 2:
            parser = reqparse.RequestParser()
            parser.add_argument('username',  type=str, required=True)
            args = parser.parse_args()
            user = User.query.filter_by(username = args.username).first()
            if user:
                try:
                    db.session.delete(user)
                    db.session.commit()
                    return jsonify({"code":200,"message":"删除成功！"})
                except:
                    return jsonify({"code":400,"message":"删除失败！"})
            else:
                return jsonify({"code":404,"message":"没有该用户！"})
        else:
            return jsonify({"code":403,"message":"权限不够！"})


## 管理员列表
class adminTable(Resource):
    @token_auth.login_required
    def get(self):
        admin = g.admin
        if admin.permission == 2:
            allAdmin = Admin.query.all()
            adminList = []
            for i in allAdmin:
                adminList.append({"adminname": i.adminname, "permission": i.permission})
            return jsonify({"adminList":adminList, "code": 200})
        else:
            return jsonify({"code": 403, "message":"权限不足"})
    @token_auth.login_required
    def delete(self):
        admin = g.admin
        if admin.permission == 2:
            parser = reqparse.RequestParser()
            parser.add_argument('adminname',  type=str, required=True)
            args = parser.parse_args()
            deleteAdmin = Admin.query.filter_by(adminname = args["adminname"]).first()
            if deleteAdmin:
                if deleteAdmin.permission >= 2:
                    return jsonify({"code":403,"message":"无法删除最高管理员！"})
                else:
                    db.session.delete(deleteAdmin)
                    db.session.commit()
                    return jsonify({"code":200,"message":"删除成功！"})
            else:
                return jsonify({"code":404,"message":"没有该管理员！"})
        else:
            return jsonify({"code":403,"message":"权限不足！"})
    @token_auth.login_required
    def put(self):
        admin = g.admin
        if admin.permission == 2:
            parser = reqparse.RequestParser()
            parser.add_argument('adminname',  type=str, required=True)
            args = parser.parse_args()
            resetAdmin = Admin.query.filter_by(adminname = args["adminname"])
            if resetAdmin:
                resetAdmin.password = "000000"
                return jsonify({"code":200,"message":"重置密码成功！"})
            else:
                return jsonify({"code":404,"message":"没有该管理员！"})
        else:
            return jsonify({"code":403,"message":"权限不足！"})
    @token_auth.login_required
    def post(self):
        admin = g.admin
        if admin.permission == 2:
            parser = reqparse.RequestParser()
            parser.add_argument('adminname',  type=str, required=True)
            parser.add_argument('password',  type=str, required=True)
            parser.add_argument('permission',  type=int, required=True)
            args = parser.parse_args()
            resetAdmin = Admin.query.filter_by(adminname = args["adminname"]).first()
            if resetAdmin:
                return jsonify({"code":409,"message":"该管理员已存在！"})
            else:
                newadmin = Admin(adminname = args["adminname"], permission = args["permission"], password = args["password"])
                db.session.add(newadmin)
                db.session.commit()
                return jsonify({"code":201,"message":"添加成功！"})
        else:
            return jsonify({"code":403,"message":"权限不足！"})

                    

## 系统配置
class App_config(Resource):
    @token_auth.login_required
    def get(self):
        if(g.admin.permission > 1):
            return jsonify(dict(app_HOST = current_app.config.get("HOST"),
                                app_PHOTO_LENGTH = current_app.config.get("PHOTO_LENGTH"),
                                app_PHOTO_WIDTH = current_app.config.get("PHOTO_WIDTH"),
                                app_PHOTO_FORMAT = current_app.config.get("PHOTO_FORMAT"),
                                app_CONFIDENCE = current_app.config.get("CONFIDENCE"),
                                app_PHOTO_DIR = current_app.config.get("PHOTO_DIR"),
                                code = 201, message= "success"))
        else:
            return jsonify(dict(app_HOST = current_app.config.get("HOST"),
                                app_PHOTO_LENGTH = current_app.config.get("PHOTO_LENGTH"),
                                app_PHOTO_WIDTH = current_app.config.get("PHOTO_WIDTH"),
                                app_PHOTO_FORMAT = current_app.config.get("PHOTO_FORMAT"),
                                app_CONFIDENCE = current_app.config.get("CONFIDENCE"),
                                app_PHOTO_DIR = current_app.config.get("PHOTO_DIR"),
                                code = 403, message = "Insufficient permissions"))
    @token_auth.login_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('host', type=str, required=True)
        parser.add_argument('dir', type=str, required=True)
        parser.add_argument('photoFormat', type=str, required=True)
        parser.add_argument('confidence', type=int, required=True)
        parser.add_argument('photoWidth', type=int, required=True)
        parser.add_argument('photoLength', type=int, required=True)
        args = parser.parse_args()
        print(args)
        with open('appconfig.json', 'w') as f:
            json.dump(dict(HOST = args['host'],
                            PHOTO_LENGTH = args['photoLength'],
                            PHOTO_WIDTH = args['photoWidth'],
                            PHOTO_FORMAT = args['photoFormat'],
                            CONFIDENCE = args['confidence'],
                            PHOTO_DIR = args['dir']), f)
            current_app.config["HOST"] = args["host"]
            current_app.config["PHOTO_LENGTH"] = args["photoLength"]
            current_app.config["PHOTO_WIDTH"] = args["photoWidth"]
            current_app.config["PHOTO_FORMAT"] = args["photoFormat"]
            current_app.config["CONFIDENCE"] = args["confidence"]
            current_app.config["PHOTO_DIR"] = args["dir"]
            f.close()
        return jsonify(dict(code = 201, message="success modify config"))

    

API.add_resource(checkItem, '/checkItem')
API.add_resource(AdminAuth, '/adminAuth')
API.add_resource(App_config, '/appConfig')
API.add_resource(userTable, '/userTable')
API.add_resource(adminTable, '/adminTable')
API.add_resource(checkList, '/checkList')

    