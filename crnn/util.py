#!/usr/bin/env python
# encoding: utf-8
'''
@author: Li Huan
@contact: lihuan@dgg.net
@file: data_generater.py
@time: 2019/5/6 13:58
@desc:
'''
import numpy as np
import cv2
import os
import random
# class data_generater():
#     def __init__(self,batch_size = 32,path = r'D:\BaiduNetdiskDownload\360label\360_train.txt',input_shape = (60,160)):
#         rate = 32/input_shape[0]
#         new_w = int(input_shape[1]*rate)
#         self.im_shape = [32,new_w]
#         with open(path,'r',encoding='UTF-8') as f:
#             data = f.readlines()
#             np.random.shuffle(data)
#         self.label = [d.split(' ')[1].strip() for d in data]
#         self.content = []
#         for l in self.label:
#             self.content += list(set(l))
#         self.content = list(set(self.content))
#         self.class_numbers = len(self.content)+1
#         self.content_range = np.arange(len(self.content))
#         self.image = [d.split(' ')[0].strip() for d in data]
#         self.index = 0
#         self.batch_size = batch_size
#         self.lenth = len(self.label)
#     def sparse_transform(self,x):
#         index = []
#         value = []
#         shape = []
#         for i,t in enumerate(x):
#             shape.append(len(t))
#             for j,c in enumerate(list(t)):
#                 index.append([i,j])
#                 value.append(self.content.index(c))
#         return np.array(index),np.array(value),np.array(shape)
#     def next_batch(self):
#         if (self.index+1) * self.batch_size <self.lenth:
#             target = self.label[self.index*self.batch_size:(self.index+1)*self.batch_size]
#             image_path = self.image[self.index*self.batch_size:(self.index+1)*self.batch_size]
#             self.index += 1
#         else:
#             target = self.label[self.index*self.batch_size:]
#             image_path = self.image[self.index*self.batch_size:]
#             self.index = 0
#         image = []
#         for im in image_path:
#             im_data = cv2.imread(os.path.join(r'D:\BaiduNetdiskDownload\Synthetic Chinese String Dataset\images',im))[:,:,::-1].astype(np.float32)
#             im_data = im_data/255
#             image.append(im_data)
#         index , values, shape = self.sparse_transform(target)
#         return np.array(image) , (index,values,np.array([self.batch_size,max(shape)])), shape
#     def ret_index(self):
#         self.index = 0

class data_generater_test():
    def __init__(self,content,batch_size = 32,path = r'images/',input_shape = (32,100)):
        print('check data...')
        self.im_shape = input_shape
        all_data = os.listdir(path)
        wrong_name = []
        for i,d in enumerate(all_data):
            for c in list(d.split('.')[0]):
                if c.lower() not in content:
                    wrong_name.append(d)
                    print('{} name wrong'.format(d))
        else:
            print('data genetatered!')
        if len(wrong_name)>0:
            wrong_name = list(set(wrong_name))
            for w in wrong_name:
                all_data.remove(w)
        all_lenth = len(all_data)
        np.random.shuffle(all_data)
        self.test_data = all_data[int(all_lenth*0.8):]
        self.test_data_label = [i.split('.')[0] for i in self.test_data]
        self.train_data = all_data[:int(all_lenth*0.8)]
        self.train_data_label = [i.split('.')[0] for i in self.train_data]
        self.content = content
        self.class_numbers = len(self.content)+1
        self.content_range = np.arange(len(self.content))
        self.index = 0
        self.batch_size = batch_size
        self.lenth = len(self.train_data_label)
    def sparse_transform(self,x):
        index = []
        value = []
        shape = []
        for i,t in enumerate(x):
            shape.append(len(t))
            for j,c in enumerate(list(t)):
                index.append([i,j])
                value.append(self.content.index(c.lower()))
        return np.array(index),np.array(value),np.array(shape)
    def next_batch(self):
        if (self.index+1) * self.batch_size <self.lenth:
            image_path = self.train_data[self.index*self.batch_size:(self.index+1)*self.batch_size]
            self.index += 1
        else:
            image_path = self.train_data[self.index*self.batch_size:]
            self.index = 0
        target = [im.split('.')[0] for im in image_path]
        image = []
        for im in image_path:
            im_data = cv2.imread(os.path.join(r'images',im))[:,:,::-1].astype(np.float32)
            im_data = cv2.resize(im_data, (self.im_shape[1], self.im_shape[0]), interpolation=cv2.INTER_CUBIC)
            im_data = im_data/255
            image.append(im_data)
        index , values, shape = self.sparse_transform(target)
        return np.array(image) , (index,values,np.array([self.batch_size,max(shape)])) , target
    def sample_test_data(self):
        sample = random.sample(self.test_data,self.batch_size)
        sample_lable = [s.split('.')[0] for s in sample]
        image = []
        for im in sample:
            im_data = cv2.imread(os.path.join(r'images', im))[:, :, ::-1].astype(np.float32)
            im_data = cv2.resize(im_data, (self.im_shape[1], self.im_shape[0]), interpolation=cv2.INTER_CUBIC)
            im_data = im_data / 255
            image.append(im_data)
        return np.array(image) , sample_lable
    def ret_index(self):
        self.index = 0

def compute_image_shape(h=60,w=160):
    rate = 32/h
    new_w = int(w*rate)
    return [32,new_w]
if __name__ == '__main__':
    data = data_generater_test()
    print(data.next_batch())
