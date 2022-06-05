import os

import cv2

import sys
sys.path.append("..")
from .utils.feature import get_feature_function
from .utils.measure import *
from configure import config, userManager

def model_predict(get_feature, template_image):
    threshold=0.85#判断是否识别的阈值
    csv_path=os.path.join(os.getcwd(), "facerec/training/users.csv")
    manager = userManager.UserManager(csv_path)
    features=[]
    base_feature=get_feature(template_image)
    base_path=os.getcwd()
    data_path="facerec/faces"
    data_path=os.path.join(base_path, data_path)
    for root, dirs, files in os.walk(data_path):#从存放用户照片的目录下搜寻匹配的用户
        for name in dirs:
            path_faces = os.path.join(root, name)
            for file in os.listdir(path_faces):
                path_face=os.path.join(path_faces, file)
                print(path_face)
                face = cv2.imread(path_face)
                face_feature = get_feature(face)
                similarity = cosine_similarity(base_feature, face_feature)#计算相似性
                print(name)
                print(similarity)
                if similarity > threshold:
                    label = manager.getUserByName(name)['id']
                    return label, similarity#返回用户id与相似性的值
                break
    return None

if __name__ == '__main__':
    model_path = "ResNet18.10-0.995387.hdf5"
    get_feature = get_feature_function(model=model_path)#加载训练好的模型
    test_image = cv2.imread("/home/pi/Desktop/deepL-faceRec/facerec/faces/aaa/face_001.pgm")
    model_predict(get_feature, test_image)
