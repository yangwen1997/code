# from model import CRNN
# # import tensorflow as tf
# # import string
# # import random
# # import os
# # import cv2
# # import numpy as np
# # # 定义模型图片输入大小和总字符列表
# # shape = [32,100]
# # content = list(string.digits)+list(string.ascii_lowercase)
# # # 初始化模型
# # classes_number =len(content)+1
# # model = CRNN(shape, classes_number, batch_size=1, training=False)
# # sess = tf.Session()
# # saver = tf.train.Saver(tf.global_variables())
# # saver.restore(sess,'./model_weights/final_model.ckpt')
# # # 读取图片
# # # image_path = os.listdir('images')
# # image_path = random.sample(image_path,1)
# # # image_path = os.path.join('images',image_path[0])
# # image_path = r'D:\TSBrowserDownloads\a.png'
# #
# # image = cv2.imread(image_path)
# # image = cv2.resize(image,(shape[1],shape[0]), interpolation=cv2.INTER_CUBIC) # 改变图大小
# # image = np.array(image).astype(np.float32)[:,:,::-1]/255 # 把图片转换成RGB格式，然后像素值归一化到[0，1]之间
# # image = np.expand_dims(image,0) # 给图片数据增加一个维度
# # # 预测
# # out = sess.run(model.decoded,feed_dict={model.input:image})
# # out_str = ''.join([content[i] for i in out[0][1]])
# # print(image_path,out_str)
# # sess.close()

