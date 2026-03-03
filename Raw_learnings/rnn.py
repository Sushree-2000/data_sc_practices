# Building a MDN-RNN model
import numpy as np
import tensorflow as tf
from torch import layer_norm

# Initializing all the parameters and variables of the MDN-RNN class
class MDNRNN(object):
    def __init__(self, hps, reuse=False, gpu_mode=False):
        self.hps = hps
        self.reuse = reuse
        with tf.variable_scope("conv_vae", reuse=self.reuse):
            if not gpu_mode:
                with tf.device('/cpu:0'):
                    tf.logging.info('Model using cpu.')
                    self.g = tf.Graph()
                    with self.g.as_default():
                        self.build_model(hps)
            else:
                tf.logging.info('Model using gpu.')
                self.build_graph()
        self._init_session()

    # Method to create a MDN-RNN model architecture
    def build_model(self, hps):
        # Building the RNN
        self.num_mixture = hps.num_mixture
        KMIX = self.num_mixture
        INWIDTH = hps.input_seg_width
        OUTWIDTH = hps.output_seg_width
        LENGTH = self.hps.max_seq_len
        # LSTM cell building
        if hps.is_training:
            self.global_step = tf.Variable(0, name='global_step', trainable=False)
        cell_fn = tf.contrib.rnn.LayerNormBasicLSTMCell
        use_recurrent_dropout = False if self.hps.use_recurrent_dropout == 0.0 else True
        use_input_dropout = False if self.hps.use_input_dropout == 0.0 else True
        use_output_dropout = False if self.hps.use_output_dropout == 0.0 else True
        use_layer_norm = False if self.hps.use_layer_norm == 0.0 else True
        if use_recurrent_dropout:
            cell = cell_fn(hps.rnn_size, layer_norm=use_layer_norm, dropout_keep_prob= hps.recurrent_dropout_prob)
        else:
            cell = cell_fn(hps.rnn_size, layer_norm=use_layer_norm)
        if use_input_dropout:
            cell = tf.nn.rnn_cell.DropoutWrapper(cell, input_keep_prob=hps.input_dropout_prob)
        if use_output_dropout:
            cell = tf.nn.rnn_cell.DropoutWrapper(cell, output_keep_prob=hps.output_dropout_prob)
        self.cell = cell
        self.sequence_lengths = LENGTH
        self.input_x = tf.placeholder(dtype=tf.float32, shape=[self.hps.batch_size, self.hps.max_seq_len, INWIDTH]) 
        self.output_x = tf.placeholder(dtype=tf.float32, shape=[self.hps.batch_size, self.hps.max_seq_len, OUTWIDTH]) 
        actual_input_x = self.input_x
        self.initial_state = cell.zero_state(batch_size=hps.batch_size, dtype=tf.float32)
        NOUT = OUTWIDTH * KMIX * 3
        with tf.variable_scope('rnn'):
            output_w = tf.get_variable("output_w", [hps.rnn_size, NOUT])
            output_b = tf.get_variable("output_b", [NOUT])
        output, last_state = tf.nn.dynamic_rnn(cell=cell, inputs=actual_input_x, initial_state=self.initial_state, dtype=tf.float32, swap_memory=True, scope="RNN")

        # Building the MDN
        output = tf.reshape(output, [-1, hps.rnn_size])
        output = tf.nn.xw_plus_b(output, output_w, output_b)
        output = tf.reshape(output, [-1, KMIX * 3])
        self.final_state = last_state
        def get_mdn_coef(output):
            logmix, mean, logstd = tf.split(output, 3, 1)
            logmix = logmix - tf.reduce_max(logmix, 1, keepdims=True)
            return logmix, mean, logstd
        out_logmix, out_mean, out_logstd = get_mdn_coef(output)
        self.out_logmix = out_logmix
        self.out_mean = out_mean
        self.out_logstd = out_logstd

        # Implementation the training operations (loss functions and optimizers)
        logSqrtTwoPi = np.log(np.sqrt(2.0 * np.pi))
        def tf_lognormal(y, mean, logstd):
            return 0.5 * tf.square((y - mean) / tf.exp(logstd)) - logstd - logSqrtTwoPi
        def tf_get_lossfunc(logmix, mean, logstd, y):
            v = logmix + tf_lognormal(y, mean, logstd)
            v = tf.reduce_logsumexp(v, 1, keepdims=True)
            return -tf.reduce_mean(v)
        flat_target_data = tf.reshape(self.output_x, [-1, 1])
        lossfunc = tf_get_lossfunc(out_logmix, out_mean, out_logstd, flat_target_data)
        self.cost = tf.reduce_mean(lossfunc)
        if self.hps.is_training:
            self.lr = tf.Variable(self.hps.learning_rate, trainable=False)
            self.optimizer = tf.train.AdamOptimizer(self.lr)
            gvs = self.optimizer.compute_gradients(self.cost)
            capped_gvs = [(tf.clip_by_value(grad, -self.hps.grad_clip, self.hps.grad_clip), var) for grad, var in gvs]
            self.train_op = self.optimizer.apply_gradients(capped_gvs, global_step=self.global_step, name='train_step')
            self.init = tf.global_variables_initializer()