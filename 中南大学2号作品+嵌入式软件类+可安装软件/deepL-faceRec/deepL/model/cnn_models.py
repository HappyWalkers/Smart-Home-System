from keras import layers
from keras.layers import Activation, Dropout, Conv2D, Dense
from keras.layers import BatchNormalization
from keras.layers import Flatten
from keras.layers import GlobalAveragePooling2D
from keras.layers import InputLayer, Input
from keras.layers import MaxPooling2D
from keras.layers import SeparableConv2D
from keras.layers import ZeroPadding2D, Add
from keras.models import Model
from keras.models import Sequential
from keras.regularizers import l2


# 这个是basic block,还有一个是bottleneck block.
def basic_block(filters, kernel_size=3, is_first_block=True):
    stride = 1
    if is_first_block:
        stride = 2

    def f(x):
        # 1st Conv
        y = ZeroPadding2D(padding=1)(x)

        y = Conv2D(filters, kernel_size, strides=stride, kernel_initializer='he_normal')(y)

        y = BatchNormalization()(y)

        y = Activation("relu")(y)


        # 2nd Conv
        y = ZeroPadding2D(padding=1)(y)

        y = Conv2D(filters, kernel_size, kernel_initializer='he_normal')(y)

        y = BatchNormalization()(y)

        # f(x) + x
        if is_first_block:#不同的filters之间调整大小
            shortcut = Conv2D(filters, kernel_size=1, strides=stride, kernel_initializer='he_normal')(x)
            shortcut = BatchNormalization()(shortcut)
        else:
            shortcut = x

        y = Add()([y, shortcut])
        # 计算输入张量列表的和。
        # 它接受一个张量的列表， 所有的张量必须有相同的输入尺寸， 然后返回一个张量（和输入张量尺寸相同）。

        y = Activation("relu")(y)

        return y

    return f



# 论文：https://arxiv.org/abs/1512.03385
def ResNet18(input_shape, num_classes):
    input_layer = Input(shape=input_shape, name="input")
    # Input() 用于实例化 Keras 张量。
    # shape: 一个尺寸元组（整数），不包含批量大小。 例如，shape=(32,) 表明期望的输入是按批次的 32 维向量。
    # name: 一个可选的层的名称的字符串。 在一个模型中应该是唯一的（不可以重用一个名字两次）。 

    # Conv1
    x = layers.ZeroPadding2D(padding=(3, 3), name='conv1_pad')(input_layer)
    # 2D 输入的零填充层（例如图像）。
    # 该图层可以在图像张量的顶部、底部、左侧和右侧添加零表示的行和列。
    # padding: 整数，或 2 个整数的元组，或 2 个整数的 2 个元组。
    # 如果为整数：将对宽度和高度运用相同的对称填充。
    # 如果为 2 个整数的元组：
    # 如果为整数：: 解释为高度和高度的 2 个不同的对称裁剪值： (symmetric_height_pad, symmetric_width_pad)。
    # 如果为 2 个整数的 2 个元组： 解释为 ((top_pad, bottom_pad), (left_pad, right_pad))。

    x = layers.Conv2D(64, (7, 7),
                      strides=(2, 2),
                      padding='valid',
                      kernel_initializer='he_normal',
                      name='conv1')(x)
    # 2D 卷积层 (例如对图像的空间卷积)。
    # 该层创建了一个卷积核， 该卷积核对层输入进行卷积， 以生成输出张量。 
    # filters: 整数，输出空间的维度 （即卷积中滤波器的输出数量）。
    # kernel_size: 一个整数，或者 2 个整数表示的元组或列表， 指明 2D 卷积窗口的宽度和高度。 
    # strides: 一个整数，或者 2 个整数表示的元组或列表， 指明卷积沿宽度和高度方向的步长。 
    # padding: "valid" 或 "same" (大小写敏感)。
    # kernel_initializer: kernel 权值矩阵的初始化器 (详见 initializers)。
    # 初始化定义了设置 Keras 各层权重随机初始值的方法。

    x = layers.BatchNormalization()(x)
    # 在每一个批次的数据中标准化前一层的激活项， 即，应用一个维持激活项平均值接近 0，标准差接近 1 的转换。

    x = layers.Activation('relu')(x)
    # 将激活函数应用于输出。

    x = layers.ZeroPadding2D(padding=(1, 1), name='pool1_pad')(x)

    x = layers.MaxPooling2D((3, 3), strides=(2, 2))(x)
    # 对于空间数据的最大池化。
    # pool_size: 整数，或者 2 个整数表示的元组， 沿（垂直，水平）方向缩小比例的因数。 （2，2）会把输入张量的两个维度都缩小一半。 如果只使用一个整数，那么两个维度都会使用同样的窗口长度。
    # strides: 整数，2 个整数表示的元组，或者是 None。 表示步长值。 如果是 None，那么默认值是 pool_size。

    # Conv2
    x = basic_block(filters=64)(x)
    x = basic_block(filters=64, is_first_block=False)(x)

    # Conv3
    x = basic_block(filters=128)(x)
    x = basic_block(filters=128, is_first_block=False)(x)

    # Conv4
    x = basic_block(filters=256)(x)
    x = basic_block(filters=256, is_first_block=False)(x)

    # Conv5
    x = basic_block(filters=512)(x)
    x = basic_block(filters=512, is_first_block=False)(x)

    x = GlobalAveragePooling2D(name="feature")(x)
    # 对于空域数据的全局平均池化。

    output_layer = Dense(num_classes, activation='softmax')(x)
    # 全连接层。
    # Dense 实现以下操作： output = activation(dot(input, kernel) + bias) 
    # units: 正整数，输出空间维度。
    # activation: 激活函数 

    model = Model(input_layer, output_layer)
    # Model 将层分组为具有训练和推理特征的对象。
    # 输入：模型的输入：一个keras.Input对象或对象列表 keras.Input。
    # 输出：模型的输出。
    return model
