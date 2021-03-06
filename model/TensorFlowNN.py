#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np

from utils import tester
from utils import tools
from utils import featureExtractor as fe


class TensorFlowNN:
    def __init__(self, stepSize=0.1, activation_function=None, hiddenLayers=1, layerNodes=10, classification=False, plot=False):
        self.stepSize = stepSize
        self.activation_function = activation_function
        self.hiddenLayers = hiddenLayers
        self.layerNodes = layerNodes
        self.classification = classification
        self.plot = plot

    def train(self, X, Y, iterations=100000, msg=None):
        # X data (n, d)
        # Y data (n, 1)
        D = X.shape[1]         # dimension of each date point
        X, Y = X[:], Y[:]
        self.x = tf.placeholder(tf.float32, shape=(None, D))
        self.y = tf.placeholder(tf.float32, shape=(None, 1))

        # define layers
        assert(self.hiddenLayers > 0)
        layer = self.add_layer(self.x, D, self.layerNodes)   # input layer
        for i in range(self.hiddenLayers):
            layer = self.add_layer(layer, self.layerNodes, self.layerNodes)   # hidden layers
        self.output = self.add_layer(layer, self.layerNodes, 1)

        # define loss and train process
        self.loss = tf.reduce_mean(tf.reduce_sum(tf.square(self.y - self.output), axis=[1]))
        self.train_step = tf.train.GradientDescentOptimizer(self.stepSize).minimize(self.loss)

        init = tf.global_variables_initializer()
        self.sess = tf.Session()
        self.sess.run(init)

        # print('----------------------------------------')
        # self.print_self_info()
        prev = 0
        for i in range(iterations):
            self.sess.run(self.train_step, feed_dict={self.x: X, self.y:Y})
            if (i + 1) % 100 == 0:
                loss = self.sess.run(self.loss, feed_dict={self.x: X, self.y: Y})
                if abs(prev - loss) < 0.00001:
                    break;
                prev = loss
        if msg:
            tools.plot(self.predict(X), Y, msg)
        # print('----------------------------------------\n')

    def predict(self, X):
        predict = self.sess.run(self.output, feed_dict={self.x: X})
        if self.classification:
            return tools.sign(predict)
        else:
            return predict.ravel()

    # add one more layer and return the output of this layer
    def add_layer(self, inputs, in_size, out_size):
        Weights = tf.Variable(tf.random_normal(shape=(in_size, out_size)))
        biases = tf.Variable(tf.zeros(shape=(1, out_size)) + 0.01)
        Wx_plus_b = tf.matmul(inputs, Weights) + biases
        if self.activation_function is None:
            outputs = Wx_plus_b
        else:
            outputs = self.activation_function(Wx_plus_b)
        return outputs

    def print_self_info(self):
        print('step: ' + str(self.stepSize) 
          + ' layers: ' + str(self.hiddenLayers) 
          + ' layerNodes: ' + str(self.layerNodes) 
          + ' activation: ' + str(self.activation_function))



    


    # foo(False, x, y, 2, 2, tf.tanh)

# iteration: 300k
# step: 0.01 layers: 2  layerNodes: 2  err: 2.37969e-4
# step: 0.01 layers: 3  layerNodes: 3  err: 2.4034e-4
# step: 0.01 layers: 4  layerNodes: 4  err: 2.27995e-4
# step: 0.01 layers: 5  layerNodes: 5  err: 2.29507e-4
# step: 0.01 layers: 1  layerNodes: 50 err: 2.47892e-4
# step: 0.01 layers: 50 layerNodes: 1  err: 2.66042e-4
# step: 0.01 layers: 2  layerNodes: 20 err: 2.26958e-4
# step: 0.01 layers: 20 layerNodes: 2  err: 2.03621e-4

# step: 0.1  layers: 2  layerNodes: 2  err: 2.08698e-4
# step: 0.1  layers: 3  layerNodes: 3  err: 2.10886e-4
# step: 0.1  layers: 4  layerNodes: 4  err: 2.34041e-4
# step: 0.1  layers: 5  layerNodes: 5  err: 2.03047e-4
# step: 0.1  layers: 10 layerNodes: 10 err: 2.47254e-4

# iteration: 1000k
# step: 0.0005 layers: 2  layerNodes: 5   err: 0.000277568
# step: 0.001  layers: 2  layerNodes: 2   err: 0.000190092
# step: 0.001  layers: 10 layerNodes: 10  err: 0.00124087
# step: 0.01   layers: 10 layerNodes: 10  err: 0.000175113
# step: 0.001  layers: 1  layerNodes: 2   err: 0.000256699
# step: 0.001  layers: 1  layerNodes: 5   err: 0.000205079
# step: 0.001  layers: 1  layerNodes: 10  err: 0.000301821
# step: 0.0005  layers: 2  layerNodes: 7  err: 0.000311183
# step: 0.0005  layers: 3  layerNodes: 3  err: 0.000229741
# step: 0.0005  layers: 3  layerNodes: 6  err: 0.000271247

# iteration: 10000k
# step: 0.001   layers: 2  layerNodes: 2  err: 0.000240726
# step: 0.0001  layers: 2  layerNodes: 3  err: 0.00024662
# step: 0.0005  layers: 3  layerNodes: 3  err: 0.000218282
# step: 0.0005  layers: 2  layerNodes: 3  err: 0.000223182

