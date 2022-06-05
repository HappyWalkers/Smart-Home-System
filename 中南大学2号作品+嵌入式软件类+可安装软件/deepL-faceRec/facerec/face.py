#coding=utf-8
import cv2

from configure import config

haar_faces = cv2.CascadeClassifier(config.CLASSIFIER_FILE)

def detectSingleFace(image):
    """ 返回脸部区域的边界(x, y, width, height)
        如果没有检测到人脸则返回None
    """
     # Detects objects of different sizes in the input image. The detected objects are returned as a list of rectangles.
    # cascade – Haar classifier cascade (OpenCV 1.x API only). It can be loaded from XML or YAML file using Load(). When the cascade is not needed anymore, release it using cvReleaseHaarClassifierCascade(&cascade).
    # image – Matrix of the type CV_8U containing an image where objects are detected.
    # objects – Vector of rectangles where each rectangle contains the detected object.
    # scaleFactor – Parameter specifying how much the image size is reduced at each image scale.
    # minNeighbors – Parameter specifying how many neighbors each candidate rectangle should have to retain it.
    # flags – Parameter with the same meaning for an old cascade as in the function cvHaarDetectObjects. It is not used for a new cascade.
    # minSize – Minimum possible object size. Objects smaller than that are ignored.
    # maxSize – Maximum possible object size. Objects larger than that are ignored.
    faces = haar_faces.detectMultiScale(image, 
            scaleFactor=config.HAAR_SCALE_FACTOR, 
            minNeighbors=config.HAAR_MIN_NEIGHBORS, 
            minSize=config.HAAR_MIN_SIZE, 
            flags=cv2.CASCADE_SCALE_IMAGE)
    #是否检测到人脸
    if len(faces) != 1:
        return None
    return faces[0]#返回第一个检测到的人脸边界

def crop(image, x, y, w, h):
    """
    从图片中截下人脸的部分返回
    """
    crop_height = int((config.FACE_HEIGHT / float(config.FACE_WIDTH)) * w)
    midy = y + h/2
    y1 = max(0, midy-crop_height/2)
    y2 = min(image.shape[0]-1, midy+crop_height/2)
    y1=int(y1)
    y2=int(y2)
    return image[y1:y2, x:x+w]

def resize(image):
    """
    调整图像大小 92x112 以进行图像训练或人脸检测
    """
    return cv2.resize(image, (config.FACE_WIDTH, config.FACE_HEIGHT), interpolation=cv2.INTER_LANCZOS4)

def markFace(image):
    result = detectSingleFace(image)
    if result != None:
        x, y, w, h = result
        #print result
        cv2.rectangle(image, (x, y), (x+w, y+h), (255,0,0))
    return image
