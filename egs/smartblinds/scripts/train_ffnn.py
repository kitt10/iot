import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'        # shut up tensorflow debug messages

from yaml import full_load as yaml_full_load
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import ModelCheckpoint
from datetime import datetime
import h5py
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
    
    with h5py.File(cfg['data']['path_start']+'ffnn.h5', 'r') as fr:
        x, y = fr['x%s'%dataset_suffix][:], fr['y%s'%dataset_suffix][:]
        k_ = len(x)
        k = (k_//cfg['ffnn']['batch_size']) * cfg['ffnn']['batch_size']
        return x[:k], y[:k]

def train(X, Y, cfg, X_val = None, Y_val = None):
    """ Design the model and train the network """

    # Take now for this particular training phase
    now = datetime.now().isoformat().replace(':', '_').replace('.', '_')
    model_path = cfg['ffnn']['model_path_start']+now+'.h5'

    # Number of features / targets / samples
    n, m, k = X.shape[1], Y.shape[1], X.shape[0]
    H = cfg['ffnn']['hidden_neurons']
    log('Data: {} features, {} targets, {} samples'.format(n, m, k), cfg['verbose'])

    # Check if there is a validation dataset
    if X_val is None or Y_val is None:
        validation_data = None
    else:
        validation_data = (X_val, Y_val)

    # Initializie the model
    model = Sequential()

    # Input layer
    model.add(Dense(H[0], input_dim=n, activation='relu'))

    # Hidden layers
    for h in H[1:]:
        model.add(Dense(h, activation='relu'))    
    
    # Output layer
    model.add(Dense(m, activation='sigmoid'))

    # Compile the model
    model.compile(loss=cfg['ffnn']['loss'], optimizer='adam', metrics=cfg['ffnn']['metrics'])

    # Print the model summary
    log('Compiled model:', cfg['verbose'])
    model.summary()

    # Define callbacks
    callbacks = [ModelCheckpoint(model_path, 
                                 monitor=cfg['ffnn']['monitor'], 
                                 verbose=True, 
                                 save_best_only=True, 
                                 save_weights_only=False)]

    # Fit the model (train the network)
    history = model.fit(X, Y, validation_data = validation_data, epochs=cfg['ffnn']['epochs'], batch_size=cfg['ffnn']['batch_size'], callbacks=callbacks)

    if cfg['ffnn']['save_history']:
        with open(cfg['ffnn']['history_path_start']+now+'.pkl', 'wb') as file_pi:
            pickle.dump(history.history, file_pi)

if __name__ == '__main__':

    # Load config
    cfg = load_yml(file_path='cfg_train_nn.yml')

    # Load training data
    X, Y = load_data(cfg)

    # Load validation data
    X_val, Y_val = load_data(cfg, dataset_suffix = '_val')

    # Train the neural network
    # The best model is derived and saved with callbacks
    train(X, Y, cfg, X_val, Y_val)