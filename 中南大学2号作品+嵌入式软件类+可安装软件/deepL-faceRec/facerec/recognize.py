from . import face
from PyQt4.QtCore import QThread

import sys
import os
sys.path.append("..")
from deepL import predict
from deepL.utils.feature import get_feature_function

class Recognizer(QThread):
    
    faceImage = None
    model = None
    result = None
    label = None
    confidence = None
    base_path = os.getcwd()
    model_path = "deepL/ResNet18.10-0.995387.hdf5"
    model_path = os.path.join(base_path, model_path)
    #print(model_path)
    get_feature = get_feature_function(model=model_path)

    def __init__(self):
        super(Recognizer, self).__init__()
        
    def run(self):
        '''
        从图片中检测人脸，并用model进行预测，标签与置信率
        '''
        if self.faceImage is None:
            # print 'face Image is None'
            return

        self.result = face.detectSingleFace(self.faceImage)
        
        if self.result is None:
            # print 'Could not detect single face!'
            return

        if self.model is None:
            # only return result when model is None
            return
        else:
            # print 'face detected'
            x, y, w, h = self.result
            # crop
            crop = face.resize(face.crop(self.faceImage, x, y, w, h))
            #self.label, self.confidence = self.model.predict(crop)

            try:
                self.label, self.confidence = predict.model_predict(Recognizer.get_feature, crop)
            except:
                self.label=0
                self.confidence=0


    def startRec(self, image, model):
        '''
        读入图像和模型，并开始线程的运行
        '''
        self.faceImage = image
        self.model = model
        
        self.start()
 
