import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'        # shut up tensorflow debug messages

from yaml import full_load as yaml_full_load
from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.callbacks import ModelCheckpoint
from datetime import datetime
import h5py
import numpy as np
import pickle


def load_yml(file_path):
    with open(file_path, 'r') as fr:
        yml_data = yaml_full_load(fr)

    log('Yml file '+str(file_path)+' loaded.', True)
    return yml_data

def log(buf, verbose):
    if verbose:
        print('[LOG]:', buf)

def load_data(cfg, dataset_suffix=''):
    
    with h5py.File(cfg['data']['path_start']+'lstm.h5', 'r') as fr:
        x, y = fr['x%s'%dataset_suffix][:], fr['y%s'%dataset_suffix][:]
        k_ = len(x)
        k = (k_//cfg['lstm']['batch_size']) * cfg['lstm']['batch_size']
        return x[:k], y[:k]

def train(X, Y, cfg, X_val = None, Y_val = None):
    """ Design the model and train the network """

    # Take now for this particular training phase
    now = datetime.now().isoformat().replace(':', '_').replace('.', '_')
    model_path = cfg['lstm']['model_path_start']+now+'.h5'

    # Number of features / targets / samples
    k, t, n = X.shape
    m = Y.shape[1]
    H = cfg['lstm']['hidden_neurons']
    log('Data: {} features, {} targets, {} samples, {} timesteps'.format(n, m, k, t), cfg['verbose'])

    # Check if there is a validation dataset
    if X_val is None or Y_val is None:
        validation_data = None
    else:
        validation_data = (X_val, Y_val)

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
    history = model.fit(X, Y, validation_data = validation_data, epochs=cfg['lstm']['epochs'], batch_size=cfg['lstm']['batch_size'], callbacks=callbacks)

    if cfg['lstm']['save_history']:
        with open(cfg['lstm']['history_path_start']+now+'.pkl', 'wb') as file_pi:
            pickle.dump(history.history, file_pi)

if __name__ == '__main__':

    # Load config
    cfg = load_yml(file_path='cfg_train_nn.yml')

    # Load training data
    X, Y = load_data(cfg)

    # Load validation data
    X_val, Y_val = load_data(cfg, dataset_suffix = '_val')

    # Train the neural network, get the model
    train(X, Y, cfg, X_val, Y_val)