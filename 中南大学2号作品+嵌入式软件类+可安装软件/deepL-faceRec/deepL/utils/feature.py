import cv2
import numpy as np
from keras import backend as K
import tensorflow as tf
from tensorflow import keras

def rebuild_model(model, input_layer="input", output_layer="feature"):
    '''
    加载模型，将网络以函数形式构建并返回函数句柄
    '''
    # if model is not an instance of Model, then try to load_model it by filepath.
    if isinstance(model, str):
        import sys
        sys.path.append("..")
        import os
        sys.path.extend([os.path.join(root, name) for root, dirs, _ in os.walk("../") for name in dirs])
        from model.amsoftmax import load_model
        print(model)
        model = load_model(filepath=model)

    __input_layer = model.get_layer(name=input_layer)
    __output_layer = model.get_layer(name=output_layer)
    func = K.function([__input_layer.input],
                      [__output_layer.output])#https://blog.csdn.net/qq_43258953/article/details/105901666
    # 实例化 Keras 函数
    # inputs: 占位符张量列表
    # outputs: 输出张量列表

    input_shape = __input_layer.input_shape[1:]
    output_shape = __output_layer.output_shape[1:]
    return func, input_shape, output_shape


def get_feature_function(model, **kwargs):
    '''
    重新构建模型，并定义inner函数，返回inner函数的句柄
    '''
    session = tf.Session()
    keras.backend.set_session(session)

    feature_function, input_shape, _ = rebuild_model(model, **kwargs)

    def inner(img):
        '''
        处理图片并返回输入模型，将模型输出的向量返回
        '''
        if isinstance(img, str):
            img = cv2.imread(img)
            assert img is not None
        if not isinstance(img, np.ndarray):
            raise Exception("img must be 'numpy.ndarray' type.But input #1 argument type is "
                            + str(type(img)))
        # preprocess
        img = cv2.resize(img, input_shape[:-1])
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = img / 256
        img = np.expand_dims(img, -1)#https://blog.csdn.net/qingzhuyuxian/article/details/90510203
        img = np.expand_dims(img, 0)
        with session.as_default():
            with session.graph.as_default():
                vector = feature_function([img])[0]
        vector = vector.flatten()
        return vector

    return inner
