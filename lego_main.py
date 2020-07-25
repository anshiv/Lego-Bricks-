# -*- coding: utf-8 -*-
"""question1_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uXrh3iWHqqSOa92NfFP4VpOYvxFMmz4K
"""

import os
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np

train_dir = os.path.join('train/train')
train_validation = pd.read_csv('Train.csv')
train_validation.category = train_validation.category.astype(str)
train_labels = train_validation.iloc[:3500]
validation_labels=train_validation.iloc[3500:]

IMG_SHAPE = (224,224,3)
VGG16_MODEL=tf.keras.applications.VGG16(input_shape=IMG_SHAPE,
                                               include_top=False,
                                               weights='imagenet')

VGG16_MODEL.trainable=False
global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
prediction_layer = tf.keras.layers.Dense(16,activation='softmax')

model = tf.keras.Sequential([
  VGG16_MODEL,
  global_average_layer,
  prediction_layer
])

model.compile(tf.keras.optimizers.Adam(learning_rate=0.05),loss='sparse_categorical_crossentropy',metrics=['accuracy'])

train_datagen=ImageDataGenerator(rescale=1./255.,
                                 rotation_range=40,
                                 width_shift_range=0.2,
                                 height_shift_range=0.2,
                                 shear_range=0.2,
                                 zoom_range=0.2,
                                 horizontal_flip=True)

validation_datagen=ImageDataGenerator(rescale=1./255.)

train_generator=train_datagen.flow_from_dataframe(dataframe=train_labels,
                                              directory=train_dir,
                                                 x_col='name',
                                                 y_col='category',
                                                 batch_size=128,
                                                 class_mode='sparse',
                                                 target_size=(224,224),
                                                  validate_filenames=False)

validation_generator=validation_datagen.flow_from_dataframe(dataframe=validation_labels,
                                              directory=train_dir,
                                                 x_col='name',
                                                 y_col='category',
                                                 batch_size=128,
                                                 class_mode='sparse',
                                                 target_size=(224,224),
                                                  validate_filenames=False)

model.fit( train_generator,
           steps_per_epoch=28,
           validation_data = validation_generator,
           validation_steps=8,
           epochs = 70,
           verbose = 1)

test_dir = os.path.join('test/test')
test_file =  pd.read_csv('Test.csv')

test_datagen=ImageDataGenerator(rescale=1./255.)
test_generator=test_datagen.flow_from_directory(test_dir,
                                                classes=['test'],
                                                 batch_size=32,
                                                 class_mode='sparse',
                                                 target_size=(150,150))

class_names=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16']
prediction=model.predict_generator(test_generator,60)

test_label= []
for i in range(1914):
  test_label.append(class_names[np.argmax(prediction[i])])

test_label=np.array(test_label)
print(test_label.shape)

test_file.insert(1,'category',test_label,False)

test_file.to_csv('submission.csv',index=False)