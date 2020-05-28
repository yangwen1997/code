#!/usr/bin/env python
# encoding: utf-8
'''
@author: Li Huan
@contact: lihuan@dgg.net
@file: train.py
@time: 2019/5/6 14:00
@desc:
'''
from util import data_generater_test
from model import CRNN
import os
import string
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
in_put = (32,100)
content = list(string.digits)+list(string.ascii_lowercase)
data = data_generater_test(content,batch_size=128,input_shape = in_put)
class_numbers = data.class_numbers
im_shape = data.im_shape
print('training model on {} samples'.format(data.lenth))
model = CRNN(in_put,class_numbers,batch_size = 128)
model.train(data,content,epoch=60)