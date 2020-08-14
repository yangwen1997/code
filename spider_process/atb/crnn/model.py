#!/usr/bin/env python
# encoding: utf-8
'''
@author: Li Huan
@contact: lihuan@dgg.net
@file: model.py
@time: 2019/5/6 14:00
@desc:
'''

import tensorflow as tf
import numpy as np

class CRNN():
    def __init__(self, input_shape, classes_number, batch_size=32, training=True):
        self.classes_number = classes_number
        self.training = training
        self.batch_size = batch_size
        self.input = tf.placeholder(shape=(batch_size, input_shape[0], input_shape[1], 3), dtype=tf.float32)
        self.target = tf.sparse_placeholder(tf.int32)
        self.cnn_output = self.cnn(self.input)
        self.seq_lenth = tf.fill([self.cnn_output.shape[0]],self.cnn_output.shape[1])
        # self.lstm_output = self.lstm(self.cnn_output)
        self.output = tf.transpose(self.cnn_output, (1, 0, 2))
        self.loss = tf.reduce_sum(tf.nn.ctc_loss(self.target,self.output,self.seq_lenth))
        self.decoded, self.log_prob = tf.nn.ctc_beam_search_decoder(self.output,self.seq_lenth,merge_repeated=False)

    def leaky_relu(self,x):
        x_positive = tf.nn.relu(x)
        x_negative = tf.nn.relu(-x)
        x = tf.subtract(x_positive, x_negative * 0.1)
        return x

    def cnn(self, x):
        # 64*280*3->64*140*64
        x = tf.layers.conv2d(x, filters=64, kernel_size=3, strides=1, padding='SAME')
        x = tf.layers.batch_normalization(x, training=self.training)
        x = self.leaky_relu(x)
        x = tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
        # 32*140*64->16*70*128
        x = tf.layers.conv2d(x, filters=128, kernel_size=3, strides=1, padding='SAME')
        x = tf.layers.batch_normalization(x, training=self.training)
        x = self.leaky_relu(x)
        x = tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
        # 16*70*128->8*70*256
        x = tf.layers.conv2d(x, filters=256, kernel_size=3, strides=1, padding='SAME')
        x = tf.layers.batch_normalization(x, training=self.training)
        x = self.leaky_relu(x)
        x = tf.layers.conv2d(x, filters=256, kernel_size=3, strides=1, padding='SAME')
        x = tf.layers.batch_normalization(x, training=self.training)
        x = self.leaky_relu(x)
        x = tf.nn.max_pool(x, ksize=[1, 2, 1, 1], strides=[1, 2, 1, 1], padding='SAME')
        # 8*70*256->4*70*512
        x = tf.layers.conv2d(x, filters=512, kernel_size=3, strides=1, padding='SAME')
        x = tf.layers.batch_normalization(x, training=self.training)
        x = self.leaky_relu(x)
        x = tf.layers.conv2d(x, filters=512, kernel_size=3, strides=1, padding='SAME')
        x = tf.layers.batch_normalization(x, training=self.training)
        x = self.leaky_relu(x)
        x = tf.nn.max_pool(x, ksize=[1, 2, 1, 1], strides=[1, 2, 1, 1], padding='SAME')
        # 4*70*512->2*70*512
        x = tf.layers.conv2d(x, filters=512, kernel_size=(2, 1), strides=1, padding='valid')
        x = tf.layers.batch_normalization(x, training=self.training)
        x = self.leaky_relu(x)
        # 2*70*512->1*70*512
        # x = tf.layers.conv2d(x, filters=512, kernel_size=(3, 1), strides=1, padding='valid')
        # x = tf.layers.batch_normalization(x, training=self.training)
        # x = self.leaky_relu(x)
        x = tf.squeeze(x,1)
        x = tf.layers.dense(x,self.classes_number)
        return x

    def lstm(self, x):
        lstm1 = tf.nn.rnn_cell.BasicLSTMCell(num_units=self.classes_number)
        x, s = tf.nn.dynamic_rnn(lstm1, x, dtype=tf.float32)
        return x
    def decode_to_str(self,predict,content):
        index = predict[0][0]
        value = predict[0][1]
        result = [[] for i in range(self.batch_size)]

        for k, item in enumerate(index):
            result[item[0]].append(content[value[k]])
        result = [''.join(i) for i in result]
        return result
    def train(self, data, content ,epoch=1000,save_path = r'./model_weights/final_model.ckpt'):
        steps = data.lenth // self.batch_size
        lr = tf.Variable(1e-2, trainable=False)
        step = tf.Variable(0, trainable=False)
        optimizer = tf.train.AdamOptimizer(lr)
        loss = self.loss
        update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
        with tf.control_dependencies(update_ops):  # 保证train_op在update_ops执行之后再执行。
            train_op = optimizer.minimize(loss, global_step=step)
        init = tf.global_variables_initializer()
        saver = tf.train.Saver(tf.global_variables())
        with tf.Session() as sess:
            losses = []
            sess.run(init)
            adjust = 0
            for i in range(epoch):
                adjust+=1
                batch_loss = []
                train_accuracy = []
                for j in range(steps):
                    x, y, target= data.next_batch()
                    x_test,y_test = data.sample_test_data()
                    if x.shape[0] == self.batch_size:
                        train_loss, _ = sess.run((loss, train_op), feed_dict={self.input: x, self.target: y})
                        test_predict = sess.run(self.decoded,feed_dict={self.input: x_test})
                        train_predict = sess.run(self.decoded,feed_dict={self.input: x})
                        test_result = self.decode_to_str(test_predict,content)
                        train_result = self.decode_to_str(train_predict,content)
                        learning = sess.run(lr)
                        test_accu = [test_result[i] == y_test[i] for i in range(len(test_result))]
                        train_accu = [train_result[i] == target[i] for i in range(len(train_result))]
                        batch_loss.append(train_loss)

                        print('epoch {}/step {}: loss {:.4f}  train_accuracy {:.4f}  test_accuracy {:.4f}  lr {}'\
                              .format((i + 1),(j + 1),train_loss,sum(train_accu)/len(train_accu),
                                      sum(test_accu)/len(test_accu),learning))
                        train_accuracy.append(sum(train_accu)/len(train_accu))
                    else:
                        pass
                losses.append(sum(batch_loss)/len(batch_loss))
                print('epoch  loss {}: {:.4f}'.format(i+1,losses[-1]))
                if len(losses)>2 and losses[-1]*1.05>=losses[-2] and adjust>=5:
                    print('reduce learning_rate by 20%')
                    sess.run(tf.assign(lr,lr/5))
                    adjust = 0
                # 训练误差准确率较高时，停止训练
                elif losses[-1] <= 0.1:
                    print('early stop!')
                    break
            saver.save(sess,save_path)