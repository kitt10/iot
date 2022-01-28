from yaml import full_load as yaml_full_load
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import ModelCheckpoint
from datetime import datetime
import h5py


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

def train(X, Y, cfg):
    """ Design the model and train the network """

    # Take now for this particular training phase
    now = datetime.now().isoformat().replace(':', '_').replace('.', '_')
    model_path = cfg['ffnn']['model_path_start']+now+'.h5'

    # Number of features / targets / samples
    n, m, k = X.shape[1], Y.shape[1], X.shape[0]
    H = cfg['ffnn']['hidden_neurons']
    log('Data: {} features, {} targets, {} samples'.format(n, m, k), cfg['verbose'])

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
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy', 'cosine_similarity'])

    # Print the model summary
    model.summary()

    # Define callbacks
    callbacks = [ModelCheckpoint(model_path, monitor='losss', verbose=True, save_best_only=True, save_weights_only=False)]

    # Fit the model (train the network)
    model.fit(X, Y, epochs=cfg['ffnn']['epochs'], batch_size=cfg['ffnn']['batch_size'], callbacks=callbacks)

if __name__ == '__main__':

    # Load config
    cfg = load_yml(file_path='cfg_train_nn.yml')

    # Load training data
    X, Y = load_data(cfg)

    # Train the neural network, get the model
    model = train(X, Y, cfg)