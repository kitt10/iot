import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'        # shut up tensorflow debug messages

from yaml import full_load as yaml_full_load
from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.callbacks import ModelCheckpoint
from datetime import datetime
import h5py
import numpy as np


def load_yml(file_path):
    with open(file_path, 'r') as fr:
        yml_data = yaml_full_load(fr)

    log('Yml file '+str(file_path)+' loaded.', True)
    return yml_data

def log(buf, verbose):
    if verbose:
        print('[LOG]:', buf)

def load_data(cfg):
    
    with h5py.File(cfg['data']['path'], 'r') as fr:
        return fr['x'][:], fr['y'][:]

def resample(X_, Y_, cfg):
    t = cfg['lstm']['timesteps']
    k_, n = X_.shape
    b = k_ // cfg['lstm']['batch_size']
    k = cfg['lstm']['batch_size'] * b

    X = list()
    Y = list()

    for ki, x in enumerate(X_[:k]):
        X.append(np.zeros(shape=(t, n)))
        offset = max(0, t-ki-1)
        X[-1][offset:, :] = X_[max(0, ki+1-t):ki+1]
        Y.append(Y_[ki])

    return np.array(X), np.array(Y)

def train(X, Y, cfg):
    """ Design the model and train the network """

    # Take now for this particular training phase
    now = datetime.now().isoformat().replace(':', '_').replace('.', '_')
    model_path = cfg['lstm']['model_path_start']+now+'.h5'

    # Number of features / targets / samples
    k, t, n = X.shape
    m = Y.shape[1]
    H = cfg['lstm']['hidden_neurons']
    log('Data: {} features, {} targets, {} samples, {} timesteps'.format(n, m, k, t), cfg['verbose'])

    # Initializie the model
    model = Sequential()
    
    # Input layer
    model.add(LSTM(units=H[0], input_shape=(t, n), batch_size=cfg['lstm']['batch_size'],
                   return_sequences=True, stateful=True))

    # Hidden layers (-1)
    for h in H[1:-1]:
        model.add(LSTM(units=h, return_sequences=True, stateful=True))
    
    # Last hidden recurrent layer
    model.add(LSTM(units=H[-1], return_sequences=False, stateful=True))

    # Output layer
    model.add(Dense(units=m, activation='sigmoid'))

    # Compile the model
    model.compile(loss=cfg['lstm']['loss'], optimizer='adam', metrics=cfg['lstm']['metrics'])

    # Print the model summary
    log('Compiled model:', cfg['verbose'])
    model.summary()

    # Define callbacks
    callbacks = [ModelCheckpoint(model_path, 
                                 monitor=cfg['lstm']['monitor'], 
                                 verbose=True, 
                                 save_best_only=True, 
                                 save_weights_only=False)]

    # Fit the model (train the network)
    model.fit(X, Y, epochs=cfg['lstm']['epochs'], batch_size=cfg['lstm']['batch_size'], callbacks=callbacks)

if __name__ == '__main__':

    # Load config
    cfg = load_yml(file_path='cfg_train_nn.yml')

    # Load training data
    X_, Y_ = load_data(cfg)

    # Adjust for RNN learning
    X, Y = resample(X_, Y_, cfg)

    # Train the neural network, get the model
    train(X, Y, cfg)