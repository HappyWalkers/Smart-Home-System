# -*- coding: utf-8 -*-
import sys
import cv2

from ui import mainwindow
from camera import Video
from configure import config

from PyQt4.QtGui import QApplication

from facerec.train import *

def main():
    
    #model = cv2.createLBPHFaceRecognizer()
    model = cv2.face.LBPHFaceRecognizer_create()
    #函数介绍：https://blog.csdn.net/qq_30815237/article/details/89185371
    #原理介绍：https://blog.csdn.net/qq_30815237/article/details/88541546

    #retrain
    #trainFace(model)

    #model.load(config.TRAINING_FILE)
    model.read(config.TRAINING_FILE)

    video = Video.Video(0)#初始化video对象
    video.setFrameSize(640, 480)#设置大小
    video.setFPS(30)#设置帧率
    #print " create QtApp"
    QtApp = QApplication(sys.argv)#Initializes the window system and constructs an application object with argc command line arguments in argv.
    #print "create mainWindow"
    mainWindow = mainwindow.Ui_MainWindow()#初始化界面
    mainWindow.setModel(model)#mainwindow获取模型
    mainWindow.showFullScreen()#Shows the window as fullscreen.
    mainWindow.setVideo(video)#mainwindow获取模型获取视频
    mainWindow.raise_()
    
    QtApp.exec_()

if __name__ == '__main__':
    main()
