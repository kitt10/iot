import train_lstm
import train_ffnn
from yaml import full_load as yaml_full_load


def load_yml(file_path):
    with open(file_path, 'r') as fr:
        yml_data = yaml_full_load(fr)

    log('Yml file '+str(file_path)+' loaded.', True)
    return yml_data

def log(buf, verbose):
    if verbose:
        print('[LOG]:', buf)

if __name__ == '__main__':
    cfg = load_yml("cfg_train_hyper.yml")

    nns = ['ffnn', 'lstm']
    training_scripts={}
    training_scripts['ffnn'] = train_ffnn
    training_scripts['lstm'] = train_lstm

    for nn in nns:
        props = cfg[nn]
        print(props)
        for h, hidden_neurons in enumerate(props['hidden_neurons']):
            for e, epochs in enumerate(props['epochs']):
                for b, batch_size in enumerate(props['batch_size']):
                    for l, loss in enumerate(props['loss']):
                        settings = {}
                        settings['data'] = cfg['data']
                        settings[nn] = {
                            "hidden_neurons": hidden_neurons,
                            "epochs": epochs,
                            "batch_size": batch_size,
                            "model_path_start": props['model_path_start']+f'h{h}_e{e}_b{b}_l{l}_',
                            "loss": loss,
                            "metrics": props['metrics'],
                            "monitor": f'val_{loss}',
                            "save_history": props['save_history'],
                            "history_path_start": props['history_path_start']+f'h{h}_e{e}_b{b}_l{l}_'
                        }
                        settings['verbose'] = cfg['verbose']

                        # Load training data
                        X, Y = training_scripts[nn].load_data(settings)

                        # Load validation data
                        X_val, Y_val = training_scripts[nn].load_data(settings, dataset_suffix = '_val')

                        # Train the neural network
                        # The best model is derived and saved with callbacks
                        log(f'Training {nn} with settings: {settings[nn]}', settings['verbose'])
                        training_scripts[nn].train(X, Y, settings, X_val, Y_val)