# -*- coding: utf-8 -*-
"""Resnet.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ybL037Ork9R2b2hB8sudmvUz4lkyX3N6
"""

import numpy as np
from keras.datasets import cifar10
from keras.utils import to_categorical, plot_model
from keras.layers import Conv2D, Input, Flatten, Dense, Activation, BatchNormalization
from keras.layers import add, AveragePooling2D
from keras.regularizers import l2
from keras.models import Model
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint, LearningRateScheduler, ReduceLROnPlateau

# dataset cifar10 = 32*32*3

(x_train, y_train), (x_test, y_test) = cifar10.load_data()
x_train = x_train.astype('float32')/255
x_test = x_test.astype('float32')/255

pixel_mean = np.mean(x_train, axis=0)   # ziro mean
x_train = x_train - pixel_mean
x_test = x_test - pixel_mean

y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

print('x_train shape:', x_train.shape)
print('y_train shape:', y_train.shape)
print('x_train shape:', x_test.shape)
print('y_train shape:', y_test.shape)
print(y_train[4])

n_classes = 10   # number of classes
n = 3    # number of residual blocks in per stack
n_stacks = 3  # number of stacks
filters = [16, 32, 64]   # number of filters in layers
m_train = x_train.shape[0]  # number of data train

batch_size = 32
epochs = 200

def resnet_layer(inputs,
                 filters,
                 strides=1,
                 kernel_size=3,   # most of time, this is 3
                 activation='relu',
                 batch_normalization=True):
    
    x = Conv2D(filters=filters,
               kernel_size=kernel_size,
               strides=strides,
               padding='same',
               kernel_initializer='he_normal',
               kernel_regularizer=l2(1e-4)
              )(inputs)
    if batch_normalization:
        x = BatchNormalization()(x)
    if activation is not None:
        x = Activation('relu')(x)
    
    return x

inputs = Input(shape=(32, 32, 3) , name = 'inputs')
x = inputs
x = resnet_layer(inputs= x,
                 filters=16)
print('conv_1:', x.shape)

for stack in range(n_stacks):  # for stack
    for block in range(n):   # for residual block
        if stack !=0 and block == 0:
            strides = 2
        else:
            strides = 1
        y = resnet_layer(inputs=x,
                         filters=filters[stack],
                         strides=strides)
        y = resnet_layer(inputs=y,
                         filters=filters[stack],
                         activation=None,
                         strides=1)
        if stack !=0 and block == 0:
            # for transition : (CNN 1*1)
            x = resnet_layer(inputs=x,
                            filters=filters[stack],
                            kernel_size=1,  # CNN 1*1
                            strides=2,
                            activation=None,
                            batch_normalization=False)
        x = add([x, y])   # x(shortcut connection) + y(2 block in stack)
        x = Activation('relu')(x)
x = AveragePooling2D(8)(x)  # 8 = since last Residual stack is 8*8
x = Flatten()(x) # output size in Average Pooling is 1*1 (must be befor a Dense layer)
outputs = Dense(10, activation='softmax',kernel_initializer='he_normal')(x)  # last layer

model = Model(inputs, outputs, name='resnet_v1_20')
model.compile(loss='categorical_crossentropy',
              optimizer=Adam(),
              metrics=['acc'])
model.summary()
plot_model(model, 'resnet_v1_20.png', show_shapes=True)