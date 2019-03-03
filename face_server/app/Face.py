# import matplotlib.pyplot as plt
# import numpy as np
# 专注于解决并发问题
# 使用过多，排队太多，轮不到我
import requests
import time
from json import JSONDecoder

import ssl

ssl._create_default_https_context = ssl._create_unverified_context  # 防止读入网站时出错

key = "Dw-h4codShmYMjo9jo6VWrQcYwJlVjdG"
secret = "	3GmEoY08YFH2QRZbwJoq2WBPMf96JEK6"

TEXT_DIS = 10
OUTER_ID = "call_the_roll"

class FaceSet:
    def __init__(self, key, secret):
        self.__key = key
        self.__secret = secret

    def SetCreate(self, outer_id, display_name=0):  # test
        print("Face set create...")
        http_url = "https://api-cn.faceplusplus.com/facepp/v3/faceset/create"
        if display_name:
            data = {"api_key": self.__key, "api_secret": self.__secret, "outer_id": outer_id,
                    "display_name": display_name}
        else:
            data = {"api_key": self.__key, "api_secret": self.__secret, "outer_id": outer_id}
        response = requests.post(http_url, data=data)
        req_con = response.content.decode('utf-8')
        req_dict = JSONDecoder().decode(req_con)
        while 'error_message' in req_dict and req_dict['error_message'] == 'CONCURRENCY_LIMIT_EXCEEDED':
            print("{'error_message': 'CONCURRENCY_LIMIT_EXCEEDED'}\nNetwork error!\n")
            print("Retry...")
            response = requests.post(http_url, data=data)
            req_con = response.content.decode('utf-8')
            req_dict = JSONDecoder().decode(req_con)
        # if 'error_message' in req_dict:
        #     print("{'error_message': 'CONCURRENCY_LIMIT_EXCEEDED'}\nNetwork error!\n")
        #     return 0
        # else:
        print("Face set create:", req_dict)
        return req_dict

    def SetAdd(self, face_tokens, outer_id='', faceset_token=''):
        print("Face set add...")
        http_url = " https://api-cn.faceplusplus.com/facepp/v3/faceset/addface"
        data = {"api_key": self.__key, "api_secret": self.__secret, "face_tokens": face_tokens}
        if outer_id != '':
            data["outer_id"] = outer_id
        elif faceset_token != '':
            data["faceset_token"] = faceset_token
        else:
            print("Parameters error!\n")
            return 0
        response = requests.post(http_url, data=data)
        req_con = response.content.decode('utf-8')
        req_dict = JSONDecoder().decode(req_con)
        while 'error_message' in req_dict and req_dict['error_message'] == 'CONCURRENCY_LIMIT_EXCEEDED':
            print("{'error_message': 'CONCURRENCY_LIMIT_EXCEEDED'}\nNetwork error!\n")
            print("Retry...")
            response = requests.post(http_url, data=data)
            req_con = response.content.decode('utf-8')
            req_dict = JSONDecoder().decode(req_con)
        # if 'error_message' in req_dict:
        #     print("{'error_message': 'CONCURRENCY_LIMIT_EXCEEDED'}\nNetwork error!\n")
        #     return 0
        # else:
        print(req_dict)
        return req_dict

    def SetGetdetail(self, outer_id='', faceset_token=''):
        print("Face set getdetail...")
        http_url = "https://api-cn.faceplusplus.com/facepp/v3/faceset/getdetail"
        data = {"api_key": self.__key, "api_secret": self.__secret}
        if outer_id != '':
            data["outer_id"] = outer_id
        elif faceset_token != '':
            data["faceset_token"] = faceset_token
        else:
            print("Parameters error!\n")
            return 0
        response = requests.post(http_url, data=data)
        req_con = response.content.decode('utf-8')
        req_dict = JSONDecoder().decode(req_con)
        while 'error_message' in req_dict and req_dict['error_message'] == 'CONCURRENCY_LIMIT_EXCEEDED':
            print("{'error_message': 'CONCURRENCY_LIMIT_EXCEEDED'}\nNetwork error!\n")
            print("Retry...")
            response = requests.post(http_url, data=data)
            req_con = response.content.decode('utf-8')
            req_dict = JSONDecoder().decode(req_con)
        # if 'error_message' in req_dict:
        #     print("{'error_message': 'CONCURRENCY_LIMIT_EXCEEDED'}\nNetwork error!\n")
        #     return 0
        # else:
        print("Face set detail:", req_dict)
        return req_dict

    def SetGetFaceSets(self, tags=0, start=0):
        print("Face set getsets...")
        http_url = "https://api-cn.faceplusplus.com/facepp/v3/faceset/getfacesets"
        data = {"api_key": self.__key, "api_secret": self.__secret}
        if tags:
            data["tags"] = tags
        if start:
            data["start"] = start
        response = requests.post(http_url, data=data)
        req_con = response.content.decode('utf-8')
        req_dict = JSONDecoder().decode(req_con)
        while 'error_message' in req_dict and req_dict['error_message'] == 'CONCURRENCY_LIMIT_EXCEEDED':
            print("{'error_message': 'CONCURRENCY_LIMIT_EXCEEDED'}\nNetwork error!\n")
            print("Retry...")
            response = requests.post(http_url, data=data)
            req_con = response.content.decode('utf-8')
            req_dict = JSONDecoder().decode(req_con)
        # if 'error_message' in req_dict:
        #     print("{'error_message': 'CONCURRENCY_LIMIT_EXCEEDED'}\nNetwork error!\n")
        #     return 0
        # else:
        print("Face set getfaceset:", req_dict)
        return req_dict

    def SetDelete(self, faceset_token='', outer_id=''):
        print("Face set delete...")
        http_url = "https://api-cn.faceplusplus.com/facepp/v3/faceset/delete"
        data = {"api_key": self.__key, "api_secret": self.__secret}
        if faceset_token != '':
            data['faceset_token'] = faceset_token
        elif outer_id != '':
            data['outer_id'] = outer_id
        else:
            print("Parameters error!\n")
            return 0

        response = requests.post(http_url, data=data)
        req_con = response.content.decode('utf-8')
        req_dict = JSONDecoder().decode(req_con)
        while 'error_message' in req_dict and req_dict['error_message'] == 'CONCURRENCY_LIMIT_EXCEEDED':
            print("{'error_message': 'CONCURRENCY_LIMIT_EXCEEDED'}\nNetwork error!\n")
            print("Retry...")
            response = requests.post(http_url, data=data)
            req_con = response.content.decode('utf-8')
            req_dict = JSONDecoder().decode(req_con)
        # if 'error_message' in req_dict:
        #     print("{'error_message': 'CONCURRENCY_LIMIT_EXCEEDED'}\nNetwork error!")
        #     return 0
        # else:
        print("Face set delete:", req_dict)
        return req_dict

    def SetRemove(self, outer_id, face_tokens="RemoveAllFaceTokens"):
        print("Face set remove...")
        http_url = "https://api-cn.faceplusplus.com/facepp/v3/faceset/removeface"
        data = {"api_key": self.__key, "api_secret": self.__secret, "outer_id": outer_id, "face_tokens":face_tokens}
        response = requests.post(http_url, data=data)
        req_con = response.content.decode('utf-8')
        req_dict = JSONDecoder().decode(req_con)
        while 'error_message' in req_dict and req_dict['error_message'] == 'CONCURRENCY_LIMIT_EXCEEDED':
            print("{'error_message': 'CONCURRENCY_LIMIT_EXCEEDED'}\nNetwork error!\n")
            print("Retry...")
            response = requests.post(http_url, data=data)
            req_con = response.content.decode('utf-8')
            req_dict = JSONDecoder().decode(req_con)
        # if 'error_message' in req_dict:
        #     print("{'error_message': 'CONCURRENCY_LIMIT_EXCEEDED'}\nNetwork error!\n")
        #     return 0
        # else:
        print("Face set remove:", req_dict)
        return req_dict


class Face:
    def __init__(self, key, secret):
        self.__key = key
        self.__secret = secret

    def GetDetail(self, face_token):
        print("Face getdetail...")
        http_url = "https://api-cn.faceplusplus.com/facepp/v3/face/getdetail"
        data = {"api_key": self.__key, "api_secret": self.__secret, "face_token": face_token}
        response = requests.post(http_url, data=data)
        req_con = response.content.decode('utf-8')
        req_dict = JSONDecoder().decode(req_con)
        while 'error_message' in req_dict and req_dict['error_message'] == 'CONCURRENCY_LIMIT_EXCEEDED':
            print("{'error_message': 'CONCURRENCY_LIMIT_EXCEEDED'}\nNetwork error!\n")
            print("Retry...")
            response = requests.post(http_url, data=data)
            req_con = response.content.decode('utf-8')
            req_dict = JSONDecoder().decode(req_con)
        # if 'error_message' in req_dict:
        #     print("{'error_message': 'CONCURRENCY_LIMIT_EXCEEDED'}\nNetwork error!\n")
        #     return 0
        # else:
        print("Face detail:", req_dict)
        print('\n')
        return req_dict

    def SetUserID(self, face_token, user_id):
        print("Face set id...")
        http_url = "https://api-cn.faceplusplus.com/facepp/v3/face/setuserid"
        data = {"api_key": self.__key, "api_secret": self.__secret, "face_token": face_token, "user_id":user_id}
        response = requests.post(http_url, data=data)
        req_con = response.content.decode('utf-8')
        req_dict = JSONDecoder().decode(req_con)
        while 'error_message' in req_dict and req_dict['error_message'] == 'CONCURRENCY_LIMIT_EXCEEDED':
            print("{'error_message': 'CONCURRENCY_LIMIT_EXCEEDED'}\nNetwork error!\n")
            print("Retry...")
            response = requests.post(http_url, data=data)
            req_con = response.content.decode('utf-8')
            req_dict = JSONDecoder().decode(req_con)
        # if 'error_message' in req_dict:
        #     print("{'error_message': 'CONCURRENCY_LIMIT_EXCEEDED'}\nNetwork error!\n")
        #     return 0
        # else:
        print("Face user_id:", req_dict)
        # print('\n')
        return req_dict

class Facepp:
    def __init__(self, key, secret):
        self.__key = key
        self.__secret = secret
        self.faceset = FaceSet(key, secret)
        self.face = Face(key, secret)

    def FaceDetect(self, filepath='', image_url='', return_landmark=1, return_attributes="none"):  # 检测filepath图片中有无人脸
        print("Face detect begin...\n")
        http_url_detect = "https://api-cn.faceplusplus.com/facepp/v3/detect"
        if filepath != '':
            data = {"api_key": self.__key, "api_secret": self.__secret, "return_landmark": return_landmark,
                    "return_attributes": return_attributes}
            files = {"image_file": open(filepath, "rb")}
            response = requests.post(http_url_detect, data=data, files=files)
            req_con = response.content.decode('utf-8')
            req_dict = JSONDecoder().decode(req_con)
            while 'error_message' in req_dict and req_dict['error_message'] == 'CONCURRENCY_LIMIT_EXCEEDED':
                print("{'error_message': 'CONCURRENCY_LIMIT_EXCEEDED'}\nNetwork error!\n")
                print("Retry...")
                response = requests.post(http_url_detect, data=data, files=files)
                req_con = response.content.decode('utf-8')
                req_dict = JSONDecoder().decode(req_con)
        elif image_url != '':
            data = {"api_key": self.__key, "api_secret": self.__secret, "image_url": image_url,
                    "return_landmark": return_landmark,
                    "return_attributes": return_attributes}
            response = requests.post(http_url_detect, data=data)
            req_con = response.content.decode('utf-8')
            req_dict = JSONDecoder().decode(req_con)
            while 'error_message' in req_dict and req_dict['error_message'] == 'CONCURRENCY_LIMIT_EXCEEDED':
                print("{'error_message': 'CONCURRENCY_LIMIT_EXCEEDED'}\nNetwork error!\n")
                print("Retry...")
                response = requests.post(http_url_detect, data=data)
                req_con = response.content.decode('utf-8')
                req_dict = JSONDecoder().decode(req_con)
        else:
            print("Not support image_base64 or parameters error!\n")
            return 0
        # req_con = response.content.decode('utf-8')
        # req_dict = JSONDecoder().decode(req_con)
        # if 'error_message' in req_dict:
        #     print("{'error_message': 'CONCURRENCY_LIMIT_EXCEEDED'}\nNetwork error!\n")
        #     return 0
        # else:
        #     # img = Image.open(filepath)
        #     # a = ImageDraw.Draw(img)
        #     # http_url_add = " https://api-cn.faceplusplus.com/facepp/v3/faceset/addface"
        #     # for i in req_dict['faces']:
        #     #     # save tokens
        #     #     face_tokens = i['face_token']
        #     #     data = {"api_key": key, "api_secret": secret, "outer_id": outer_id, "face_tokens": face_tokens}
        #     #     response = requests.post(http_url_add, data=data)
        #     #     req_con = response.content.decode('utf-8')
        #     #     req_dict = JSONDecoder().decode(req_con)
        #     #     print(req_dict)
        #     #
        #     #     # draw
        #     #     x = i['face_rectangle']['left']
        #     #     y = i['face_rectangle']['top']
        #     #     h = i['face_rectangle']['height']
        #     #     w = i['face_rectangle']['width']
        #     #     a.line(((x, y), (x, y + h)), fill=(255, 0, 0,), width=width)
        #     #     a.line(((x, y + h), (x + w, y + h)), fill=(255, 0, 0), width=width)
        #     #     a.line(((x + w, y + h), (x + w, y)), fill=(255, 0, 0), width=width)
        #     #     a.line(((x + w, y), (x, y)), fill=(255, 0, 0), width=width)
        #     #
        #     # img.save(savepath)
        print("Face detect:", req_dict)
        print('\n')
        return req_dict

    def FaceCompare(self, image_file1='', image_file2='', image_url1='', image_url2='', face_token1='', face_token2=''):
        print("Face compare begin...\n")
        http_url = "https://api-cn.faceplusplus.com/facepp/v3/compare"
        data = {"api_key": self.__key, "api_secret": self.__secret}
        files = {}
        if image_file1 != '':
            files = {"image_file1": open(image_file1, "rb")}
        elif image_url1 != '':
            data["image_url1"] = image_url1
        elif face_token1 != '':
            data["face_token1"] = face_token1
        else:
            print("Parameters error!\n")
            return 0

        if image_file2 != '':
            files.update({"image_file2": open(image_file2, "rb")})
        elif image_url2 != '':
            data["image_url2"] = image_url2
        elif face_token2 != '':
            data["face_token2"] = face_token2
        else:
            print("Parameters error!\n")
            return 0
        if files:
            response = requests.post(http_url, data=data, files=files)
            req_con = response.content.decode('utf-8')
            req_dict = JSONDecoder().decode(req_con)
            while 'error_message' in req_dict and req_dict['error_message'] == 'CONCURRENCY_LIMIT_EXCEEDED':
                print("{'error_message': 'CONCURRENCY_LIMIT_EXCEEDED'}\nNetwork error!\n")
                print("Retry...")
                response = requests.post(http_url, data=data, files=files)
                req_con = response.content.decode('utf-8')
                req_dict = JSONDecoder().decode(req_con)
        else:
            response = requests.post(http_url, data=data)
            req_con = response.content.decode('utf-8')
            req_dict = JSONDecoder().decode(req_con)
            while 'error_message' in req_dict and req_dict['error_message'] == 'CONCURRENCY_LIMIT_EXCEEDED':
                print("{'error_message': 'CONCURRENCY_LIMIT_EXCEEDED'}\nNetwork error!\n")
                print("Retry...")
                response = requests.post(http_url, data=data)
                req_con = response.content.decode('utf-8')
                req_dict = JSONDecoder().decode(req_con)
        print("Face compare:", req_dict)
        return req_dict

    def FaceSearch(self, face_token='', image_url='', image_file='', faceset_token='', outer_id='', return_result_count=1):
        print("Face search begin...\n")
        http_url = "https://api-cn.faceplusplus.com/facepp/v3/search"
        data = {"api_key": self.__key, "api_secret": self.__secret, \
                "return_result_count": return_result_count}
        files = {}
        if face_token != '':
            data["face_token"] = face_token
        elif image_url != '':
            data["image_url"] = image_url
        elif image_file != '':
            files = {"image_file": open(image_file, "rb")}
        else:
            print("Parametes error!\n")
            return 0

        if faceset_token != '':
            data['faceset_token'] = faceset_token
        elif outer_id != '':
            data['outer_id'] = outer_id
        else:
            print("Parametes error!\n")
            return 0

        if files:
            response = requests.post(http_url, data=data, files=files)
            req_con = response.content.decode('utf-8')
            req_dict = JSONDecoder().decode(req_con)
            while 'error_message' in req_dict and req_dict['error_message'] == 'CONCURRENCY_LIMIT_EXCEEDED':
                print("{'error_message': 'CONCURRENCY_LIMIT_EXCEEDED'}\nNetwork error!\n")
                print("Retry...")
                response = requests.post(http_url, data=data, files=files)
                req_con = response.content.decode('utf-8')
                req_dict = JSONDecoder().decode(req_con)
        else:
            response = requests.post(http_url, data=data)
            req_con = response.content.decode('utf-8')
            req_dict = JSONDecoder().decode(req_con)
            while 'error_message' in req_dict and req_dict['error_message'] == 'CONCURRENCY_LIMIT_EXCEEDED':
                print("{'error_message': 'CONCURRENCY_LIMIT_EXCEEDED'}\nNetwork error!\n")
                print("Retry...")
                response = requests.post(http_url, data=data)
                req_con = response.content.decode('utf-8')
                req_dict = JSONDecoder().decode(req_con)

        print("Face search:", req_dict)
        return req_dict

    def DrawDetected(self, outer_id, req_dict, filepath='', image_url='', return_landmark=1, return_attributes="none", width=10):
        print("DrawDetected...")
        if filepath == '':
            print("Only support filepath\n")
            return 0

        # result = self.FaceDetect(filepath, return_landmark, return_attributes)
        img = Image.open(filepath)
        a = ImageDraw.Draw(img)
        # http_url_add = " https://api-cn.faceplusplus.com/facepp/v3/faceset/addface"
        for i in req_dict['faces']:
            # save tokens
            face_tokens = i['face_token']
            # self.faceset.SetAdd(face_tokens, outer_id)

            # draw
            # x = i['face_rectangle']['left']
            # y = i['face_rectangle']['top']
            # h = i['face_rectangle']['height']
            # w = i['face_rectangle']['width']
            # a.line(((x, y), (x, y + h)), fill=(255, 0, 0,), width=width)
            # a.line(((x, y + h), (x + w, y + h)), fill=(255, 0, 0), width=width)
            # a.line(((x + w, y + h), (x + w, y)), fill=(255, 0, 0), width=width)
            # a.line(((x + w, y), (x, y)), fill=(255, 0, 0), width=width)
            self.Draw(a, i['face_rectangle'])

        img.show()
        # img.save(savepath)
        # print("Face detect:", )
        return req_dict

    def Draw(self, img_tar, faces_rect, width=10):
        # img_tar是指打开的，img_tar = ImageDraw.Draw(img)
        # face_tokens = faces_dic['face_token']
        x = faces_rect['left']
        y = faces_rect['top']
        h = faces_rect['height']
        w = faces_rect['width']
        img_tar.line(((x, y), (x, y + h)), fill=(255, 0, 0,), width=width)
        img_tar.line(((x, y + h), (x + w, y + h)), fill=(255, 0, 0), width=width)
        img_tar.line(((x + w, y + h), (x + w, y)), fill=(255, 0, 0), width=width)
        img_tar.line(((x + w, y), (x, y)), fill=(255, 0, 0), width=width)
        # img.show()

    def DrawSearched(self, search_reslt, image_file):
        print("Draw searched...")
        if "results" in search_reslt.keys():
            face_token = search_reslt["results"][0]["face_token"]
            img = Image.open(image_file)
            a = ImageDraw.Draw(img)
            face_detail = self.face.GetDetail(face_token)
            face_rect = face_detail["face_rectangle"]
            self.Draw(a, faces_rect=face_rect)
            img.show()
            return face_detail
        else:
            print("No face searched!")
            return 0

    # 仅一张脸
    def AddFaceData(self, filepath, user_id, outer_id):
        print("Add face data...")
        dict = self.FaceDetect(filepath)
        face_token = dict['faces'][0]['face_token']
        self.face.SetUserID(face_token, user_id)
        tmp = self.faceset.SetAdd(face_token, outer_id=outer_id)
        print("Added:", tmp)

    def PrintName(self, img_tar, face_detail, source_face):
        draw = ImageDraw.Draw(img_tar)
        x = source_face['face_rectangle']['left']
        y = source_face['face_rectangle']['top']
        h = source_face['face_rectangle']['height']
        w = source_face['face_rectangle']['width']
        # 注意下面第一个参数，是draw句柄而不是img_tar
        self.Draw(draw, source_face['face_rectangle'])
        draw.text((x, y - h - TEXT_DIS), face_detail['user_id'], fill=(0, 0, 0))
        return face_detail['user_id']

    def CallRoll(self, filepath, outer_id):
        count = 0
        print("Call the roll...")
        rec_dict = self.FaceDetect(filepath)
        img = Image.open(filepath)
        for i in rec_dict['faces']:
            # t = self.FaceDetect(filepath="img/test.jpg")
            # #
            # result = self.FaceSearch(face_token=t['faces'][0]['face_token'], outer_id=outer_id)
            result = self.FaceSearch(face_token=i['face_token'], outer_id=outer_id)
            # self.DrawSearched(result, filepath)
            # 添加判断非空，并且调出第一个，其中，第一个要加下标0
            if "results" in result.keys() and result['results'][0]['confidence'] >= 80:
                # self.DrawSearched(result, "img/zh1.jpg")
                print(result['results'][0])
                face_token = result['results'][0]['face_token']
                face_detail = self.face.GetDetail(face_token)
                name = self.PrintName(img, face_detail, i)
                print("name:", name)
                self.face.SetUserID(i['face_token'], name)
                self.faceset.SetAdd(face_token, outer_id)
            else:
                # face_token = i['face_token']
                # face_detail = self.face.GetDetail(face_token)
                # name = face_detail['user_id']

                count += 1
                print("Absent num: %d" % count)

        print("Show image...")
        img.show()




# test = Facepp(key, secret)
# req_dict = test.FaceDetect(r"img/zh1.jpg")
# item = test.DrawDetected("call_the_roll", req_dict, r"img/zh1.jpg")
# searched = test.FaceSearch(image_file="img/syd1.jpg", outer_id="call_the_roll")
# test.DrawSearched(searched, "img/zh1.jpg")
# test.faceset.SetDelete(outer_id="test")
# test.faceset.SetCreate("call_the_roll")


# req = test.FaceDetect(filepath='img/ss2.jpg')
# test.DrawDetected("call_the_roll", req_dict=req, filepath='img/ss2.jpg')


# test.faceset.SetRemove(outer_id=OUTER_ID)
# test.faceset.SetGetdetail(outer_id=OUTER_ID)
# test.AddFaceData(r"img/syd1.jpg", "Shao", OUTER_ID)
# test.AddFaceData(r"img/cc1.jpg", "ChenCheng", OUTER_ID)
# test.AddFaceData(r"img/lyc1.jpg", "LuYancheng", OUTER_ID)
# test.AddFaceData(r"img/brs1.jpg", "Anonymous", OUTER_ID)
# test.AddFaceData(r"img/yx1.jpg", "Yue", OUTER_ID)
#
# c = test.faceset.SetGetdetail(OUTER_ID)
# test.faceset.SetGetFaceSets()
# test.faceset.SetGetdetail(OUTER_ID)
# test.CallRoll(r"img/zh1.jpg", OUTER_ID)
# test.faceset.SetGetdetail(OUTER_ID)

# p = test.FaceDetect("img/spring.jpg")
# test.DrawDetected("call_the_roll", p, "img/spring.jpg")

# OUTER_ID1 = "gaokao"
# OUTER_ID2 = "jiaowu"
# test.faceset.SetDelete(outer_id=OUTER_ID1)
# test.faceset.SetDelete(outer_id=OUTER_ID2)
# test.faceset.SetCreate(outer_id=OUTER_ID1)
# test.faceset.SetCreate(outer_id=OUTER_ID2)

# test.faceset.SetRemove(outer_id=OUTER_ID2)
# i = 1
# while(i <= 34):
#     num = 161271000 + i
#     test.AddFaceData(r"img/d/jw/"+str(num) + ".JPG", str(num), OUTER_ID2)
#     i += 1
# i = 1
# while(i <= 54):
#     num = 161278000 + i
#     test.AddFaceData(r"img/d/jw/"+str(num) + ".JPG", str(num), OUTER_ID2)
#     i += 1

# x = np.linspace(0, 30, 31)  ##[-3,3]之间50个点

# plt.xlim((50, 100)) #横坐标范围
# plt.ylim((0, 20)) #纵坐标范围
# x_data = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0}
# mysum = 0
# y = {}

# i = 1
# while(i <= 34):
#     num = 161271000 + i
#     try:
#         tmp = test.FaceSearch(image_file=r"img/d/2016T/"+str(num)+".jpg", outer_id=OUTER_ID2)
#         print(num)
#         print(tmp["results"][0]["confidence"])
#         a = int(tmp["results"][0]["confidence"])
#         mysum += 1
#         # x[(int(tmp["results"][0]["confidence"])) / 10 + 1] += 1
#         if a in y.keys():
#             y[a] += 1
#         else:
#             y[a] = 1
#         # y[tmp["results"][0]["confidence"]]

#     except Exception:
#         i += 1
#         continue
#     i += 1

# i = 1
# while i <= 34:
#     num = 161271000 + i
#     try:
#         tmp = test.FaceSearch(image_file=r"img/d/2016T/" + str(num) + "x.jpg", outer_id=OUTER_ID2)
#         print(num, "x")
#         print(tmp["results"][0]["confidence"])
#         a = int(tmp["results"][0]["confidence"])
#         mysum += 1
#         # x[(int(tmp["results"][0]["confidence"])) / 10 + 1] += 1
#         if a in y.keys():
#             y[a] += 1
#         else:
#             y[a] = 1
#     except Exception:
#         i += 1
#         continue
#     i += 1

# i = 1
# while i <= 34:
#     num = 161271000 + i
#     try:
#         tmp = test.FaceSearch(image_file=r"img/d/2016T/" + str(num) + "y.jpg", outer_id=OUTER_ID2)
#         print(num, "y")
#         print(tmp["results"][0]["confidence"])
#         a = int(tmp["results"][0]["confidence"])
#         mysum += 1
#         # x[(int(tmp["results"][0]["confidence"])) / 10 + 1] += 1
#         if a in y.keys():
#             y[a] += 1
#         else:
#             y[a] = 1
#     except Exception:
#         i += 1
#         continue
#     i += 1

# i = 1
# while i <= 54:
#     num = 161278000 + i
#     try:
#         tmp = test.FaceSearch(image_file=r"img/d/2016T/" + str(num) + ".jpg", outer_id=OUTER_ID2)
#         print(num)
#         print(tmp["results"][0]["confidence"])
#         a = int(tmp["results"][0]["confidence"])
#         mysum += 1
#         # x[(int(tmp["results"][0]["confidence"])) / 10 + 1] += 1
#         if a in y.keys():
#             y[a] += 1
#         else:
#             y[a] = 1
#     except Exception:
#         i += 1
#         continue
#     i += 1

# plt.scatter(y.keys(), y.values())
# print(y.keys())
# print(y.values())
# print(mysum)

# plt.show()






