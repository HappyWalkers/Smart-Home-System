# -*- coding: utf-8 -*-
import cv2
import numpy as np
from PyQt4 import QtGui

class Video():
    '''
    封装cv2.VideoCapture函数，用于读取摄像头每帧图像的数据
    可将每帧图像数据转化为QImage及CVImage
    '''
    def __init__(self, device):
        self.capture = cv2.VideoCapture(device)
        self.currentFrame = np.array([])
        self.readFrame = None
        self.is_release = False
 
    def setFrameSize(self, width, height):
        '''
        CV_CAP_PROP_FRAME_WIDTH Width of the frames in the video stream.
        CV_CAP_PROP_FRAME_HEIGHT Height of the frames in the video stream.
        '''
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        
    def setFPS(self, fps):
        '''
        CV_CAP_PROP_FPS Frame rate.
        '''
        self.capture.set(cv2.CAP_PROP_FPS, fps)

    def read(self):
        '''
        读一张图片保存到self.readFrame，并返回
        '''
        ret, self.readFrame = self.capture.read()
        if ret == True:
            return self.readFrame
        else:
            return None

    def open(self, device):
        self.is_release = False
        self.capture.open(device)

    def release(self):
        self.is_release = True
        self.capture.release()

    def captureNextFrame(self, isFlip = True):
        """                           
        capture frame and reverse RBG BGR and return opencv image                                      
        """
        self.read()
        if self.readFrame is not None:
            self.currentFrame = cv2.cvtColor(self.readFrame, cv2.COLOR_BGR2RGB)
            if isFlip == True:
                self.currentFrame = cv2.flip(self.currentFrame, 1)
            
    def convertFrame(self):
        """
        converts frame to format suitable for QtGui
        """
        try:
            height,width = self.currentFrame.shape[:2]
            img = QtGui.QImage(self.currentFrame,
                              width,
                              height,
                              QtGui.QImage.Format_RGB888)
            return img
        except:
            return None

    def getFrame(self):
        readFrame = self.read()
        return readFrame
        
    def getQImageFrame(self):
        '''
        返回qtGUI的摄像头一帧图像
        '''
        self.captureNextFrame()
        return self.convertFrame()

    def getCVImage(self, params):
        return cv2.cvtColor(self.readFrame, params)
    
    def getGrayCVImage(self, isFlip=True):
        if self.readFrame is not None:
            grayFrame = cv2.cvtColor(self.readFrame, cv2.COLOR_BGR2GRAY)
            if isFlip == True:
                grayFrame = cv2.flip(grayFrame, 1)
            return grayFrame
        else:
            #print 'readFrame is None'
            return None
