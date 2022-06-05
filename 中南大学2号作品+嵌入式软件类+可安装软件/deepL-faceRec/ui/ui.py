# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import * 
from PyQt4 import QtCore
from PyQt4 import QtGui

from facerec import recognize, train
from facerec import face
from camera import VideoStream
from configure import config, userManager

from .soft_keyboard import *

import os
import cv2

try:
    from PyQt4.QtCore import QString
except ImportError:
    # we are using Python3 so QString is not defined
    QString = type("")

try:
    _fromUtf8 =QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

#Qt css样式文件
style = QString(open('./ui/css/style.css').read())

#显示视频的Qt控件
#setRect当前一帧图像上画出方框，用于标记人脸的位置
#setRectColor设置方框的颜色
#setUserLabel在方框旁边添加识别信息，比如识别到的用户名
class VideoFrame(QtGui.QLabel):
    '''
    显示视频的Qt控件
    '''    
    userName = None
    pen_faceRect = QtGui.QPen()
    pen_faceRect.setColor(QtGui.QColor(255, 0, 0))
    x = 0;y = 0;w = 0;h = 0
    
    def __init__(self, parent):
        QtGui.QLabel.__init__(self, parent)
        

        
    def setRect(self, x, y, w, h):
        '''
        在当前一帧图像上画出方框，用于标记人脸的位置
        '''
        self.x, self.y, self.w, self.h = x, y, w, h
    
    def setRectColor(self, r, g, b):
        '''
        设置方框的颜色
        '''
        self.pen_faceRect.setColor(QtGui.QColor(r, g, b))

    def setUserLabel(self, userName):
        '''
        添加识别信息，比如识别到的用户名
        '''
        self.userName = userName

    def paintEvent(self, event):
        QtGui.QLabel.paintEvent(self,event)
        painter = QtGui.QPainter(self)
        painter.setPen(self.pen_faceRect)
        painter.drawRect(self.x, self.y, self.w, self.h)
        if self.userName != None:
            painter.drawText(self.x, self.y+15, self.userName)

class FaceRec(QWidget):
    '''
    人脸识别界面
    '''
    model = None
    confidence = -1
    label = ''
    faceRect = None
    
    captureFlag = 0
    
    confidences = []
    
    def __init__(self, mainWindow):
        '''
        初始化界面，定时器连接playVideo
        '''
        super().__init__()
        self.mainWindow = mainWindow
        self.manager = userManager.UserManager()
        
        self.setupUi(self)
        
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.playVideo)
        self._timer.start(10)
        self.update()
    
    def setModel(self, model):
        self.model = model
    
    def setupUi(self, FaceRec):
        '''
        画界面，初始化按钮与label
        '''
        FaceRec.setObjectName(_fromUtf8("FaceRec"))
        FaceRec.resize(480, 800)

        font = QtGui.QFont()
        font.setPointSize(16)
        
        self.video_frame = VideoFrame(FaceRec)
        self.video_frame.setGeometry(QtCore.QRect(250, 100, 480, 360))

        self.pushButton_back = QtGui.QPushButton(FaceRec)
        self.pushButton_back.setGeometry(QtCore.QRect(450, 600, 80, 50))
        self.pushButton_back.setFont(font)
        self.pushButton_back.clicked.connect(self.pushButton_back_clicked)

        self.label_title = QtGui.QLabel(FaceRec)
        self.label_title.setGeometry(QtCore.QRect(450, 10, 100, 50))
        self.label_title.setFont(font)
        
        self.label_info = QtGui.QLabel(FaceRec)
        self.label_info.setGeometry(QtCore.QRect(350, 500, 300, 50))
        self.label_info.setFont(font)

        self.retranslateUi(FaceRec)
        QtCore.QMetaObject.connectSlotsByName(FaceRec)

    def pushButton_capture_clicked(self):
        '''
        没用到
        '''
        #print 'capture clicked'
        self.captureFlag = 10

    def pushButton_back_clicked(self):
        '''
        返回 按钮被按下时调用
        '''
        self._timer.stop()
        self.vs.stop()
        self.video.release()
        self.mainWindow.setupUi(self.mainWindow)

    def pushButton_capture_clicked(self):
        '''
        没用到
        '''
        self.startRec()

    def setVideo(self, video):
        self.video = video
        
        self.vs = VideoStream.VideoStream(self.video,'192.168.1.113', 8888)
        #self.vs.startStream()
        
        self.startRec()
        
    def playVideo(self):
        '''
        将来自摄像头的一张图像显示在界面上
        '''
        try:
            pixMap_frame = QtGui.QPixmap.fromImage(self.video.getQImageFrame())
            # getQImageFrame()返回qtGUI的摄像头一帧图像
            # Converts the given image to a pixmap using the specified flags to control the conversion. 
            # The flags argument is a bitwise-OR of the Qt::ImageConversionFlags. Passing 0 for flags sets all the default options.
            x = 0;y = 0;w = 0;h = 0
            if self.faceRect is not None:
                #640x480 to 480x360
                x, y, w, h = self.faceRect[0]*0.75, self.faceRect[1]*0.75, self.faceRect[2]*0.75, self.faceRect[3]*0.75
            self.video_frame.setRect(400-x, y, w, h)# 在人脸上画方框
            self.video_frame.setPixmap(pixMap_frame)# 设置图像
            self.video_frame.setScaledContents(True)
        except TypeError:
            print("No frame")
       
    def startRec(self):
        self.recognizer = recognize.Recognizer()#初始化recognizer
        self.recognizer.finished.connect(self.reciveRecognizeResult)#一次识别线程结束调用reciveRecognizeResult
        #image = self.video.getGrayCVImage()#将视频中的图像转化为灰度图像并返回
        image = self.video.read()#返回一张视频中的图像
        self.recognizer.startRec(image, self.model)#将获得的视频图像image和模型model传入recognizer开始检测
        
    def reciveRecognizeResult(self):
        self.faceRect = self.recognizer.result#人脸方框坐标
        userName = None
        if not self.video.is_release:
            if self.recognizer.result is not None:
                self.confidences.append(self.recognizer.confidence)#置信率
                mean = sum(self.confidences) / float(len(self.confidences))
                #print 'label:',self.recognizer.label
                #print 'confidence: %.4f'%self.recognizer.confidence,'mean:%.4f'%mean

                user = self.manager.getUserById(self.recognizer.label)
                print(self.recognizer.label)
                print(user)
                #self.video_frame.setUserLabel(userName)

                if user != None:
                    userName = user['userName']
                    self.video_frame.setUserLabel(userName)#显示用户名
                    
                if self.recognizer.confidence <= 85:
                    self.video_frame.setRectColor(0, 255, 0)#绿
                else:
                    self.video_frame.setRectColor(255, 0, 0)#红
            
            info = 'user: ' + str(userName) + ' | confidence: ' + str(self.recognizer.confidence)
            self.label_info.setText(info)
            self.startRec()

    def retranslateUi(self, FaceRec):
        FaceRec.setWindowTitle(_translate("FaceRec", u"from", None))
        self.label_title.setText(_translate("FaceRec", u"人脸识别", None))
        self.video_frame.setText(_translate("FaceRec", "video_frame", None))
        self.label_info.setText(_translate("FaceRec", "label_info", None))
        self.pushButton_back.setText(_translate("FaceRec", u"返回", None))

#人脸录入界面
class FaceRegister(QWidget):
    
    faceRect = None
    
    captureFlag = 0
    personName = None
    recOver = False
    model = None
    
    def __init__(self, mainWindow):
        super().__init__()
        
        self.mainWindow = mainWindow
        self.manager = userManager.UserManager()
        
        self.setupUi(self)
        
        #The QTimer class provides a high-level programming interface for timers. 
        # To use it, create a QTimer, connect its timeout() signal to the appropriate slots, and call start(). 
        # From then on, it will emit the timeout() signal at constant intervals.
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.playVideo)
        #print "start begin"
        self._timer.start(10)    
        #print "start began"
        self.update()
        
    def setupUi(self, FaceRegister):
        '''
        画界面
        '''
        FaceRegister.setObjectName(_fromUtf8("FaceRegister"))
        FaceRegister.resize(480, 800)
        
        self.inputDialog = InputDialog(self.reciveUserName)#输入框连接函数

        font = QtGui.QFont()
        font.setPointSize(16)

        self.label_title = QtGui.QLabel(FaceRegister)
        self.label_title.setGeometry(QtCore.QRect(450, 50, 100, 60))
        self.label_title.setFont(font)

        self.progressBar = QtGui.QProgressBar(FaceRegister)
        self.progressBar.setGeometry(QtCore.QRect(300, 700, 440, 60))
        self.progressBar.setRange(0, 20)
        self.progressBar.setValue(0)
        self.progressBar.setVisible(False)

        self.video_frame = VideoFrame(FaceRegister)
        self.video_frame.setGeometry(QtCore.QRect(250, 100, 480, 360))
         
        self.pushButton_capture = QtGui.QPushButton(FaceRegister)
        self.pushButton_capture.setGeometry(QtCore.QRect(450, 500, 100, 60))
        self.pushButton_capture.setFont(font)
        self.pushButton_capture.clicked.connect(self.pushButton_capture_clicked)
         
        self.pushButton_back = QtGui.QPushButton(FaceRegister)
        self.pushButton_back.setGeometry(QtCore.QRect(450, 600, 100, 60))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton_back.setFont(font)
        self.pushButton_back.clicked.connect(self.pushButton_back_clicked)
 
        self.retranslateUi(FaceRegister)
        QtCore.QMetaObject.connectSlotsByName(FaceRegister)
        
    def setVideo(self, video):
        self.video = video
        if self.video.is_release:
            self.video.open(0)
        
    def setModel(self, model):
        self.model = model
        
    def playVideo(self):
        '''
        显示视频
        '''
        #print "playVideo"
        try:
            pixMap_frame = QtGui.QPixmap.fromImage(self.video.getQImageFrame())
            x = 0;y = 0;w = 0;h = 0
            if self.faceRect is not None:
                x, y, w, h = self.faceRect[0]*0.75, self.faceRect[1]*0.75, self.faceRect[2]*0.75, self.faceRect[3]*0.75
            self.video_frame.setRect(x, y, w, h)
            self.video_frame.setPixmap(pixMap_frame)
            self.video_frame.setScaledContents(True)
        except TypeError:
            print('No frame')

    def startRec(self):
        self.recognizer = recognize.Recognizer()
        self.recognizer.finished.connect(self.reciveRecognizeResult)#一次识别线程结束调用reciveRecognizeResult
        image = self.video.getGrayCVImage()#将视频中的图像转化为灰度图像并返回
        self.recognizer.startRec(image, None)
        
    def reciveRecognizeResult(self):
        self.faceRect = self.recognizer.result#人脸方框坐标
        if self.faceRect is not None and self.captureFlag != 0:
            x, y, w, h = self.faceRect
            crop = face.crop(self.recognizer.faceImage, x, y, w, h)
            personDir = os.path.join(config.FACES_DIR, self.personName)
            if not os.path.exists(personDir):
                os.makedirs(personDir)
            fileName = os.path.join(personDir, 'face_'+'%03d.pgm'%self.captureFlag)
            cv2.imwrite(fileName, crop)#保存图片
            #print 'capture'
            self.captureFlag -= 1
            self.progressBar.setValue(20 - self.captureFlag)#读20张图片
            if self.captureFlag == 0:#读完释放，开始选择图片
                self.recOver = True
                #print 'capture over'
                self.video.release()
                self.startPictureSelect()#图片选择界面
   
        if not self.video.is_release and self.recOver == False:#没读完接着读
            self.startRec()
        
    def reciveUserName(self, name):
        '''
        确认 按钮点击后调用,查看用户是否存在，不存在就准备开始截取图片，调用self.startRec()
        '''
        self.personName = str(name)
        
        #self.inputDialog.deleteLater()
        #print name
        personDir = os.path.join(config.FACES_DIR, self.personName)
        if os.path.exists(personDir):
            #print 'person already exist'
            #TODO alert
            self.inputDialog.show(u'用户已存在！')
        else:
            self.pushButton_capture.setEnabled(False)
            self.captureFlag = 20#连续读20张图片
            self.progressBar.setVisible(True)#进度条
            self.label_title.setText(u'开始截取图片')
            self._timer.start(10)
            self.startRec()
            
    def startPictureSelect(self):
        '''
        打开图片选择界面
        '''
        #print 'start picture select'
        pictureSelect = PictureSelect(self.mainWindow, self.personName)
        pictureSelect.setModel(self.model)
        self.mainWindow.setCentralWidget(pictureSelect)
        
    def pushButton_capture_clicked(self):
        '''
        开始按钮按下时输入用户名
        '''
        self.inputDialog.setInfo(u'请输入用户名')
        self.inputDialog.show()
        self.inputDialog.clear()
            
    def pushButton_back_clicked(self):
        '''
        返回按钮按下时返回主界面
        '''
        self._timer.stop()
        self.video.release()
        self.mainWindow.setupUi(self.mainWindow)
        
    def retranslateUi(self, FaceRegister):
        FaceRegister.setWindowTitle(_translate("FaceRegister", "Form", None))
        self.label_title.setText(_translate("FaceRegister", u"人脸录入", None))
        self.video_frame.setText(_translate("FaceRegister", " ", None))
        self.pushButton_capture.setText(_translate("FaceRegister", u"开始", None))#开始按钮
        self.pushButton_back.setText(_translate("FaceRegister", u"返回", None))#返回按钮

#软键盘控件
class InputDialog(TouchInputWidget):
#class InputDialog(QWidget):
    def __init__(self, callback):
        TouchInputWidget.__init__(self)
        #super().__init__() 
        self.callback = callback#回调函数
        
        self.labelInfo = QtGui.QLabel()
        
        self.editUserName = QtGui.QLineEdit()
        self.editUserName.keyboard_type = 'default'
        
        self.pushButton_accept = QtGui.QPushButton(self)
        self.pushButton_accept.setText(u'确认')
        self.pushButton_accept.clicked.connect(self.reciveUserName)#确认 按钮按下时调用
        
        gl = QtGui.QVBoxLayout()
        gl.addWidget(self.pushButton_accept)
        gl.addWidget(self.labelInfo)
        gl.addWidget(self.editUserName)
        
        self.setLayout(gl)
        
    def setInfo(self, info):
        self.labelInfo.setText(info)
        
    def clear(self):
        self.editUserName.clear()
        
    def reciveUserName(self):
        '''
        确认 按钮按下时调用,将输入的用户名传入回调函数
        '''
        self.touch_interface._input_panel_all.hide()
        self.userName = self.editUserName.text()
        if self.userName == '':
            return
        self.callback(self.userName)
        self.hide()

class PictureSelect(QWidget):
    '''
    图片选择界面
    '''
    pictures = []
    pictureNames = []
    path = None
    model = None

    def __init__(self, mainWindow, path):
        super(PictureSelect, self).__init__()
        self.mainWindow = mainWindow
        self.path = path

        self.setupUi(self)
        
        self.readPictures()
        
        self.showPictures()
        
    def setupUi(self, pictureSelect):
        pictureSelect.setObjectName(_fromUtf8("pictureSelect"))
        pictureSelect.resize(480, 800)
        
        self.setStyleSheet(style)
        
        font = QtGui.QFont()
        font.setPointSize(18)
        
        self.label_info = QtGui.QLabel(pictureSelect)
        self.label_info.setGeometry(QtCore.QRect(0, 20, 480, 50))
        self.label_info.setFont(font)
        
        self.scrollArea = QtGui.QScrollArea(pictureSelect)
        self.scrollArea.setGeometry(QtCore.QRect(0, 100, 480, 550))
        self.scrollArea.setWidgetResizable(False)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 478, 548))
        
        self.gridLayoutWidget = QtGui.QWidget(self.scrollArea)
        
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        
        self.scrollArea.setWidget(self.gridLayoutWidget)
        
        font = QtGui.QFont()
        font.setPointSize(16)
        
        self.pushButton_delete = QtGui.QPushButton(pictureSelect)
        self.pushButton_delete.setGeometry(QtCore.QRect(70, 680, 100, 60))
        self.pushButton_delete.setFont(font)
        self.pushButton_delete.clicked.connect(self.pushButton_delete_clicked)
        
        self.pushButton_ok = QtGui.QPushButton(pictureSelect)
        self.pushButton_ok.setGeometry(QtCore.QRect(190, 680, 100, 60))
        self.pushButton_ok.setFont(font)
        self.pushButton_ok.clicked.connect(self.pushButton_ok_clicked)
        
        self.pushButton_back = QtGui.QPushButton(pictureSelect)
        self.pushButton_back.setGeometry(QtCore.QRect(310, 680, 100, 60))
        self.pushButton_back.setFont(font)
        self.pushButton_back.setObjectName(_fromUtf8("pushButton_back"))
        self.pushButton_back.clicked.connect(self.pushButton_back_clicked)

        self.retranslateUi(pictureSelect)
        QtCore.QMetaObject.connectSlotsByName(pictureSelect)

    def setModel(self, model):
        self.model = model

    def readPictures(self):
        '''
        读出存下的图
        '''
        self.pictures = []
        self.pictureNames = []
        path = os.path.join(config.FACES_DIR, self.path)
        for fileName in train.walkFiles(path, '*.pgm'):
            self.pictures.append(QtGui.QPixmap(fileName))
            self.pictureNames.append(fileName)

    def clearGridLayout(self):
        for i in reversed(range(self.gridLayout.count())):
            self.gridLayout.itemAt(i).widget().deleteLater()

    def showPictures(self):
        '''
        显示存下的图
        '''
        for i in range(0, len(self.pictures)):
            label_pic = PictureLabel()
            label_pic.mousePressEvent = label_pic.clicked
            h = self.pictures[i].height()
            w = self.pictures[i].width()
            label_pic.setFixedSize(QSize(w, h))
            label_pic.setPixmap(self.pictures[i])
            label_pic.setPictureName(self.pictureNames[i])
            self.gridLayout.addWidget(label_pic, i/2, i%2, 1, 1)
        self.gridLayoutWidget.setFixedSize(self.gridLayout.sizeHint())

    def trainFinish(self):
        '''
        训练完成后调用
        '''
        dialog = QtGui.QMessageBox()
        dialog.setWindowTitle('info')
        dialog.setText(u'人脸录入已完成(%s)'%self.path)
        if dialog.exec_():
            #print 'over'
            self.label_info.setText(u'选择要删除的图片，点击删除按钮进行删除')
            self.pushButton_ok.setEnabled(True)

    def pushButton_delete_clicked(self):
        self.pushButton_delete.setEnabled(False)
        for i in range(self.gridLayout.count()):
            item = self.gridLayout.itemAt(i)
            if item != None:
                label_pic = item.widget()
                #print label_pic.pictureName
                if label_pic.selected:
                    #print 'delete',label_pic.pictureName
                    os.remove(os.path.join(config.FACES_DIR, self.path, label_pic.pictureName))
            
        self.clearGridLayout()   
        self.readPictures()
        self.showPictures()
        self.pushButton_delete.setEnabled(True)

    def pushButton_ok_clicked(self):
        '''
        确定 按钮按下调用，开启线程训练模型
        '''
        self.label_info.setText(u'正在录入人脸...')
        self.pushButton_ok.setEnabled(False)
        self.trainThread = TrainThread(self.model, os.path.join(config.TRAINING_DIR, config.TRAINING_FILE))
        self.trainThread.finished.connect(self.trainFinish)
        self.trainThread.start()

    def pushButton_back_clicked(self):
        self.gridLayout = None
        self.pictures = []
        self.pictureNames = []
        self.mainWindow.setupUi(self.mainWindow)

    def retranslateUi(self, pictureSelect):
        pictureSelect.setWindowTitle(_translate("pictureSelect", "Form", None))
        self.label_info.setText(_translate("pictureSelect", u"选择要删除的图片，点击删除按钮进行删除", None))
        self.pushButton_back.setText(_translate("pictureSelect", u"返回", None))
        self.pushButton_delete.setText(_translate("pictureSelect", u"删除", None))
        self.pushButton_ok.setText(_translate("pictureSelect", u"录入", None))

class TrainThread(QtCore.QThread):
    
    model = None
    trainFileName = None
    
    def __init__(self, model, trainFileName):
        super(TrainThread, self).__init__()
        
        self.model = model
        self.trainFileName = trainFileName
        
    def run(self):
        '''
        训练模型并重新加载模型
        '''
        train.trainFace(self.model)
        print('train faces over')
        self.model.read(self.trainFileName)
        print('model reload over')

#显示单个图像的Qt控件
class PictureLabel(QtGui.QLabel):
        
    selected = False
    pictureName = None
    
    def __init__(self):
        QtGui.QLabel.__init__(self)
        self.deleteImage = QtGui.QPixmap('./res/pic/delete_100x100.png')
        
    def setPictureName(self, name):
        self.pictureName = name
        
    def clicked(self, event):
        #print 'clicked'
        if self.selected:
            self.selected = False
        else:
            self.selected = True
        self.update()
        
    def paintEvent(self, event):
        QtGui.QLabel.paintEvent(self,event)
        if self.selected:
            painter = QtGui.QPainter(self)
            size = self.sizeHint()
            x = size.width()/2 - 50
            y = size.height()/2 - 50
            painter.drawPixmap(x, y, self.deleteImage)
