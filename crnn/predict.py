#!/usr/bin/env python
# encoding: utf-8
'''
@author: Li Huan
@contact: lihuan@dgg.net
@file: predict.py
@time: 2019/5/6 23:07
@desc:
'''
from model import CRNN
import os
import cv2
import numpy as np
import random
import tensorflow as tf
from util import compute_image_shape
import string
import time
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
content = list(string.digits)+list(string.ascii_lowercase)
im_shape = compute_image_shape(60,160)
image_path = os.listdir('images')
image_path = random.sample(image_path,100)
num_classes = len(content)+1
model = CRNN(im_shape,num_classes,batch_size = 1,training=False)
saver = tf.train.Saver(tf.global_variables())
with tf.Session() as sess:
    saver.restore(sess,'./model_weights/final_model.ckpt')
    score = []
    for im in image_path:
        start = time.time()
        image = cv2.imread(os.path.join('images',im))
        image = cv2.resize(image,(im_shape[1],im_shape[0]), interpolation=cv2.INTER_CUBIC)
        image = np.array(image).astype(np.float32)[:,:,::-1]/255
        image = np.expand_dims(image,0)
        out = sess.run(model.decoded,feed_dict={model.input:image})
        out_str = ''.join([content[i] for i in out[0][1]])
        score.append(im.split('.')[0] == out_str)
        an = '正确' if score[-1] == 1 else '错误'
        print('图片', im,'的验证码为:', out_str,'判断{}'.format(an), '用时{:.2f}秒'.format(time.time()-start))
    print('测试准确率为: {:.4f}'.format(sum(score)/len(score)))
