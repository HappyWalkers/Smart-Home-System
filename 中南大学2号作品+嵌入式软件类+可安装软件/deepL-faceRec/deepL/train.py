#!/usr/bin env python

from keras.callbacks import EarlyStopping, ReduceLROnPlateau, CSVLogger, ModelCheckpoint
# DO NOT REMOVE THIS:
from model.cnn_models import *
from utils.data_generator import DataGenerator
from model.amsoftmax import wrap_cnn, amsoftmax_loss

input_shape = (64, 64, 1)
batch_size = 64
num_epochs = 10
patience = 10
log_file_path = "./log.csv"
cnn = "ResNet18"
trained_models_path = "./trained_models/" + cnn

generator = DataGenerator(dataset="olivettifaces",
                          path="./data/olivetti_faces/olivettifaces.jpg",
                          batch_size=batch_size,
                          input_size=input_shape,
                          is_shuffle=True,
                          data_augmentation=10,
                          validation_split=.2)
num_classes, num_images, training_set_size, validation_set_size = generator.get_number()
print(num_classes, num_images, training_set_size, validation_set_size)


model = wrap_cnn(model=eval(cnn),
                 feature_layer="feature",
                 input_shape=input_shape,
                 num_classes=num_classes)
model.compile(optimizer='adam',
              loss=amsoftmax_loss,
              metrics=['accuracy'])#模型配置
model.summary()#输出模型结构


# callbacks
early_stop = EarlyStopping('loss', 0.1, patience=patience)
#当被监测的数量不再提升，则停止训练
# monitor: 被监测的数据。
# min_delta: 在被监测的数据中被认为是提升的最小变化， 例如，小于 min_delta 的绝对变化会被认为没有提升。
# patience: 没有进步的训练轮数，在这之后训练就会被停止。

reduce_lr = ReduceLROnPlateau('loss', factor=0.1,
                              patience=int(patience / 2), verbose=1)
#当标准评估停止提升时，降低学习速率。
# 当学习停止时，模型总是会受益于降低 2-10 倍的学习速率。 这个回调函数监测一个数据
# 并且当这个数据在一定「有耐心」的训练轮之后还没有进步， 那么学习速率就会被降低。
# monitor: 被监测的数据。
# factor: 学习速率被降低的因数。新的学习速率 = 学习速率 * 因数
# patience: 没有进步的训练轮数，在这之后训练速率会被降低。
# verbose: 整数。0：安静，1：更新信息。

csv_logger = CSVLogger(log_file_path, append=False)
#把训练轮结果数据流到 csv 文件的回调函数。
# 支持所有可以被作为字符串表示的值，包括 1D 可迭代数据，例如，np.ndarray。
# filename: csv 文件的文件名，例如 'run/log.csv'。
# append: True：如果文件存在则增加（可以被用于继续训练）。False：覆盖存在的文件。

model_names = trained_models_path + '.{epoch:02d}-{accuracy:02f}.hdf5'
model_checkpoint = ModelCheckpoint(model_names,
                                   monitor='loss',
                                   verbose=1,
                                   save_best_only=True,
                                   save_weights_only=False)
# 在每个训练期之后保存模型。
# filepath 可以包括命名格式选项，可以由 epoch 的值和 logs 的键（由 on_epoch_end 参数传递）来填充。
# 例如：如果 filepath 是 weights.{epoch:02d}-{val_loss:.2f}.hdf5， 那么模型被保存的的文件名就会有训练轮数和验证损失。
# filepath: 字符串，保存模型的路径。
# monitor: 被监测的数据。
# verbose: 详细信息模式，0 或者 1 。
# save_best_only: 如果 save_best_only=True， 被监测数据的最佳模型就不会被覆盖。
# save_weights_only: 如果 True，那么只有模型的权重会被保存 (model.save_weights(filepath))， 否则的话，整个模型会被保存 (model.save(filepath))。


callbacks = [model_checkpoint, csv_logger, early_stop, reduce_lr]

# train model by generator
model.fit_generator(generator=generator.flow('train'),
                    steps_per_epoch=int(training_set_size / batch_size),
                    epochs=num_epochs,
                    verbose=1,
                    callbacks=callbacks,
                    validation_data=generator.flow('validate'),
                    validation_steps=int(validation_set_size) / batch_size)#模型训练
# 使用 Python 生成器（或 Sequence 实例）逐批生成的数据，按批次训练模型。
# generator: 一个生成器
# steps_per_epoch: 在声明一个 epoch 完成并开始下一个 epoch 之前从 generator 产生的总步数（批次样本）。 它通常应该等于你的数据集的样本数量除以批量大小。 
# epochs: 训练模型的迭代总轮数。一个 epoch 是对所提供的整个数据的一轮迭代，如 steps_per_epoch 所定义。
# verbose: 0, 1 或 2。日志显示模式。 0 = 安静模式, 1 = 进度条, 2 = 每轮一行。
# callbacks: keras.callbacks.Callback 实例的列表。在训练时调用的一系列回调函数。
# validation_data: 验证数据
# validation_steps: 仅当 validation_data 是一个生成器时才可用。 在停止前 generator 生成的总步数（样本批数）。 

