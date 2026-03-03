# Building a CNN-VAE model
import numpy as np
import tensorflow as tf

# Initializing all the parameters and variables of the CNN-VAE class
class ConVAE(object):
    def __init__(self, z_size=32, batch_size=1, learning_rate=0.0001, kl_tolerance=0.5, is_training=False, reuse=False, gpu_mode=False):
        self.z_size = z_size
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.kl_tolerance = kl_tolerance
        self.is_training = is_training
        self.reuse = reuse
        # self.gpu_mode = gpu_mode
        with tf.variable_scope("conv_vae", reuse=self.reuse):
            if not gpu_mode:
                with tf.device('/cpu:0'):
                    tf.logging.info('Model using cpu.')
                    self.build_graph()
            else:
                tf.logging.info('Model using gpu.')
                self.build_graph()
        self._init_session()

    # Building the Encoder part of the VAE
    def _build_graph(self):
        self.g = tf.Graph()
        with self.g.as_default():
            self.x = tf.placeholder(tf.float32, shape=[None, 64, 64, 3])
            # Building the encoder part of the VAE
            h= tf.layers.conv2d(self.x, filters=32, kernel_size=4, strides=2, activation=tf.nn.relu, name='enc_conv1')
            h= tf.layers.conv2d(h, filters=64, kernel_size=4, strides=2, activation=tf.nn.relu, name='enc_conv2')
            h= tf.layers.conv2d(h, filters=128, kernel_size=4, strides=2, activation=tf.nn.relu, name='enc_conv3')
            h= tf.layers.conv2d(h, filters=256, kernel_size=4, strides=2, activation=tf.nn.relu, name='enc_conv4')
            h= tf.reshape(h, shape=[-1, 2*2*256])

            # Building the “V” part of the VAE
            self.mu= tf.layers.dense(h, units=self.z_size, name='enc_fc_mu')
            self.logvar= tf.layers.dense(h, units=self.z_size, name='enc_fc_logvar')
            self.sigma= tf.exp(0.5 * self.logvar)
            self.epsilon= tf.random_normal([self.batch_size, self.z_size])
            self.z = self.mu + self.sigma * self.epsilon

            # ARCHITECTURE OF THE VAE
            # Building the decoder part of the VAE
            h= tf.layers.dense(self.z, units=2*2*256, name='dec_fc')
            # h= tf.reshape(h, shape=[-1, 2, 2, 256])
            h= tf.reshape(h, shape=[-1, 1, 1, 1024])
            h= tf.layers.conv2d_transpose(h, filters=128, kernel_size=5, strides=2, activation=tf.nn.relu, name='dec_deconv1')
            h= tf.layers.conv2d_transpose(h, filters=64, kernel_size=5, strides=2, activation=tf.nn.relu, name='dec_deconv2')
            h= tf.layers.conv2d_transpose(h, filters=32, kernel_size=6, strides=2, activation=tf.nn.relu, name='dec_deconv3')
            self.y= tf.layers.conv2d_transpose(h, filters=3, kernel_size=6, strides=2, activation=tf.nn.sigmoid, name='dec_deconv4')

            # TRAINING THE VAE MODEL
            # Implementing the training operations (loss functions and optimizers)
            if self.is_training:
                self.global_step = tf.Variable(0, name='global_step', trainable=False)
                self.r_loss = tf.reduce_sum(tf.square(self.x - self.y), reduction_indices =[1, 2, 3])
                self.r_loss = tf.reduce_mean(self.r_loss)
                self.kl_loss = -0.5 * tf.reduce_sum(1 + self.logvar - tf.square(self.mu) - tf.exp(self.logvar), reduction_indices=1)
                self.kl_loss = tf.maximum(self.kl_loss, self.kl_tolerance * self.z_size)
                self.kl_loss = tf.reduce_mean(self.kl_loss)
                self.loss = self.r_loss + self.kl_loss
                self.lr = tf.Variable(self.learning_rate, trainable=False) #lr = learning rate
                self.optimizer = tf.train.AdamOptimizer(self.lr)
                grads = self.optimizer.compute_gradients(self.loss)
                self.train_op = self.optimizer.apply_gradients(grads, global_step=self.global_step, name='train_step') #train_op = training operation
            self.init = tf.global_variables_initializer()
