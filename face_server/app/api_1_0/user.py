from app.api_1_0 import api
import app
import os
from app import db
from flask import jsonify, request, g, current_app
from app.models import User, Event, Admin
from app.Face import Facepp
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_restful import Api, Resource, reqparse
from werkzeug.datastructures import FileStorage
from config import basedir
import  hashlib
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet

base_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme='Token')
API = Api(api)

imgSecret_key = b'L5udwIEY2jzFimjtANkrHdsdr-_K75yeTidMRc5dYeE=' #加密文件名用的key
key = "Dw-h4codShmYMjo9jo6VWrQcYwJlVjdG"
secret = "3GmEoY08YFH2QRZbwJoq2WBPMf96JEK6"


@api.route('/test', methods=['GET'])
@base_auth.login_required
def test():
    return jsonify(status='fail')
 
@base_auth.verify_password
def verify_password(username, password):
    print(username, password)
    user = User.query.filter_by(username = username).first()
    if user:
        if user.verify_password(password):
            return True
    return False

@token_auth.verify_token
def verify_token(token):
    print(token + '123123')
    g.user = None
    s = Serializer(current_app.config["SECRET_KEY"])
    try:
        username = s.loads(token)
        print(username)
        g.user = User.query.filter_by(username = username['username']).first()
        print('ok g user')
    except:
        return False
    return True

@token_auth.error_handler
def token_error():
    return  jsonify({"message":"token not correct", "code": 401}) , 201

@base_auth.error_handler
def base_error():
    return  jsonify({"message":"password not correct", "code": 401}),  201


def encrypt_filename(filename):
    '''新增的函数，用于加密文件名'''
    fencrypt = Fernet(imgSecret_key)
    bfilename = str.encode(filename)
    bfilename = fencrypt.encrypt(bfilename)
    filename = bytes.decode(bfilename)
    return filename

def decrypt_filename(filename):
    '''新增的函数，用于解密文件名，写后台的时候可能使用到'''
    fencrypt = Fernet(imgSecret_key)
    bfilename = str.encode(filename)
    bfilename = fencrypt.decrypt(bfilename)
    filename = bytes.decode(bfilename)
    return filename

class Authentication(Resource):
    # 登陆
    @base_auth.login_required
    def get(self):
        user = User.query.filter_by(username=base_auth.username()).first()
        if user:
            token = user.generate_auth_token()
            return jsonify({"token": str(token, encoding="utf-8"), "code": 201})
        else: 
            return jsonify({"message": "Login failed", "code": 401}), 201
    # 注册
    # def post(self):
    #     try:
    #         parser = reqparse.RequestParser()
    #         parser.add_argument('username', type=str)
    #         parser.add_argument('password', type=str)
    #         parser.add_argument('phone', type=str)
    #         args = parser.parse_args()
    #     except: 
    #         return {"message": "Error of parameters", "code": 400}, 201
    #     try:
    #         newUser = User(username = args['username'],password = args['password'],phone = args['phone'])
    #     except:
    #         return {"message": "Username has been used", "code": 400}, 201
    #     try:
    #         db.session.add(newUser)
    #     except:
    #         return {"message": "Failed to store data", "code": 400}, 201
    #     return {"message": "success register", "code": 201}, 201

# def findLastEvent(username)

# 用户照片信息
class Photo(Resource):
    # 获取照片
    @token_auth.login_required
    def get(self):
        user = g.user
        if user:
            event = Event.query.filter(Event.username == user.username, Event.status!=1).order_by(Event.time.desc()).first()
            if event:
                photoUrl = current_app.config["HOST"] + "resources/"+ current_app.config["PHOTO_DIR"]+"/uploadPhoto/" + event.uploadPhotoName + current_app.config["PHOTO_FORMAT"]
                return jsonify({"photoUrl": photoUrl, "code": 200, "status": event.status})
            else:
                defaultPhoto = current_app.config["HOST"] + "static/head_placeholder.jpg"
                return jsonify({"photoUrl": defaultPhoto, "code": 201, "status": 0 })
        else:
            return jsonify({'message': "没有该用户", "code": 406})


    # 修改照片
    @token_auth.login_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('img', type=FileStorage, location=['files','form'])
        args = parser.parse_args()
        img = args['img']
        user = g.user
        if user:
            path = basedir+"/resources/"+current_app.config["PHOTO_DIR"]
            tempFilename = secure_filename(encrypt_filename(user.username+"upload"))
            tempFilepath = path+"/uploadPhoto/" + tempFilename+current_app.config["PHOTO_FORMAT"]
            args.img.save(tempFilepath)
            originPhotoPath = path+"/systemPhoto/" + user.photoName+current_app.config["PHOTO_FORMAT"]
            face = Facepp(key, secret)
            res = face.FaceCompare(image_file1=tempFilepath, image_file2=originPhotoPath)
            if res.get('confidence'): 
                if  res['confidence'] < current_app.config["CONFIDENCE"]:
                    status = 1
                else:
                    status = 2
            else:
                status = 1
            newEvent = Event(id = Event.query.with_entities(Event.id).count()+1 ,username=user.username, uploadPhotoName = tempFilename, status = status, confidence = res.get('confidence'))
            db.session.add(newEvent)
            db.session.commit()
            if status == 2:
                user.lastStatus = status
            return jsonify({"code": 200, "status": status, "confidence": res['confidence']})
        else:
            return jsonify({"code": 500})


API.add_resource(Photo, '/Photo')
API.add_resource(Authentication, '/Authentication')



        


