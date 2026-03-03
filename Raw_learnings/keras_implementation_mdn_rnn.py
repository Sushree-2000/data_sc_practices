# Building the MDN-RNN model

# Importing the libraries
import math
import numpy as np
from keras.layers import Input, LSTM, Dense
from keras.models import Model
from keras import backend as K
from keras.callbacks import EarlyStopping

# Setting the dimensions of the latent vectors
Z_DIM = 32

# Setting the number of actions
ACTION_DIM = 3

# Setting the number of LSTM units
HIDDEN_UNITS = 256

# Setting the number of gaussian mixture outputs
GAUSSIAN_MIXTURES = 5

# Setting the batch size and number of epochs
BATCH_SIZE =32
EPOCHS = 20

# Getting the gaussian mixture coeficients
def get_mixture_coef(y_pred):
    d = GAUSSIAN_MIXTURES * Z_DIM
    rollout_length = K.shape(y_pred)[1]
    pi = y_pred[:,:,:d]
    mu = y_pred[:,:,d:(2*d)]
    log_sigma = y_pred[:,:,(2*d):(3*d)]
    pi = K.reshape(pi, [-1, rollout_length, GAUSSIAN_MIXTURES, Z_DIM])
    mu = K.reshape(mu, [-1, rollout_length, GAUSSIAN_MIXTURES, Z_DIM])
    log_sigma = K.reshape(log_sigma, [-1, rollout_length, GAUSSIAN_MIXTURES, Z_DIM])
    pi = K.exp(pi) / K.sum(K.exp(pi), axis=2, keepdims=True)
    sigma = K.exp(log_sigma)
    return pi, mu, sigma

# Normalizing the target values
def tf_normal(y_true, mu, sigma, pi):
    rollout_length = K.shape(y_true)[1]
    y_true = K.tile(y_true,(1,1,GAUSSIAN_MIXTURES))
    y_true = K.reshape(y_true, [-1, rollout_length, GAUSSIAN_MIXTURES,Z_DIM])
    oneDivSqrtTwoPI = 1 / math.sqrt(2*math.pi)
    result = y_true - mu
    result = result * (1 / (sigma + 1e-8))
    result = -K.square(result)/2
    result = K.exp(result) * (1/(sigma + 1e-8))*oneDivSqrtTwoPI
    result = result * pi
    result = K.sum(result, axis=2)
    return result

# Building the MDN-RNN model within a class

class MDNRNN():

    # Initializing all the parameters and variables of the MDNRNN class
    def __init__(self):
        self.models = self._build()
        self.model = self.models[0]
        self.forward = self.models[1]
        self.z_dim = Z_DIM
        self.action_dim = ACTION_DIM
        self.hidden_units = HIDDEN_UNITS
        self.gaussian_mixtures = GAUSSIAN_MIXTURES

    # Building the model
    def _build(self):
        # Defining the Inputs of the RNN (latent vector space + action space)
        rnn_x = Input(shape=(None, Z_DIM + ACTION_DIM))
        # Defining the LSTM layer that returns the output weights and cell states
        lstm = LSTM(HIDDEN_UNITS, return_sequences=True, return_state = True)
        # Getting the real outputs from the LSTM
        lstm_output, _ , _ = lstm(rnn_x)
        # Getting the gaussian mixture outputs
        mdn = Dense(GAUSSIAN_MIXTURES * (3*Z_DIM))(lstm_output)
        # Getting the training model
        rnn = Model(rnn_x, mdn)
        # Getting the hidden state and cell state inputs
        state_input_h = Input(shape=(HIDDEN_UNITS,))
        state_input_c = Input(shape=(HIDDEN_UNITS,))
        # Grouping them
        state_inputs = [state_input_h, state_input_c]
        # Getting outputs new state and new cell state from the LSTM
        _ , state_h, state_c = lstm(rnn_x, initial_state = [state_input_h, state_input_c])
        # Defining the forward propagation for inference only
        forward = Model([rnn_x] + state_inputs, [state_h, state_c])
        # Implementing the training operations
        def rnn_r_loss(y_true, y_pred):
            # Defining the negative log loss over all the gausian mixtures
            pi, mu, sigma = get_mixture_coef(y_pred)
            result = tf_normal(y_true, mu, sigma, pi)
            result = -K.log(result + 1e-8)
            result = K.mean(result, axis = (1,2))
            return result
        # Defining the KL divergence loss, the same as in the VAE, only over normalized outputs
        def rnn_kl_loss(y_true, y_pred):
            pi, mu, sigma = get_mixture_coef(y_pred)
            kl_loss = - 0.5 * K.mean(1 + K.log(K.square(sigma)) - K.square(mu) - K.square(sigma), axis = [1,2,3])
            return kl_loss
        # Defining the RNN loss
        def rnn_loss(y_true, y_pred):
            return rnn_r_loss(y_true, y_pred)
        # Compiling the RNN model with the RNN loss and the RMSProp optimizer
        rnn.compile(loss=rnn_loss, optimizer='rmsprop', metrics = [rnn_r_loss, rnn_kl_loss])
        return (rnn,forward)

    # Loading the weights of the model
    def set_weights(self, filepath):
        self.model.load_weights(filepath)

    # Creating early stopping callbacks to prevent overfitting
    def train(self, rnn_input, rnn_output, validation_split = 0.2):
        earlystop = EarlyStopping(monitor='val_loss', min_delta=0.0001, patience=5, verbose=1, mode='auto')
        callbacks_list = [earlystop]
        # Fitting the model to the RNN inputs and targets
        self.model.fit(rnn_input, rnn_output,
            shuffle=True,
            epochs=EPOCHS,
            batch_size=BATCH_SIZE,
            validation_split=validation_split,
            callbacks=callbacks_list)
        # Saving the model after the training is done
        self.model.save_weights('rnn/weights.h5')

    # Separating the function used to save the model (usefull if the model is retrained)
    def save_weights(self, filepath):
        self.model.save_weights(filepath)