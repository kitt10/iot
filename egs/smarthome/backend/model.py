from sys import version as py_version
from argparse import ArgumentParser
from config import Config
from sklearn.ensemble import IsolationForest
from pickle import dump as pickle_dump
from json import load as load_json, dump as dump_json
from data import get_samples

def parse_arguments():  
    parser = ArgumentParser(description='Smarthome sensory system - model')
    parser.add_argument('-c', '--cfg_path', type=str, default='config.cfg',
                        help='Path to the config file.')
    parser.add_argument('-m', '--mode', type=str, default='', choices=['', 'init'],
                        help='Mode of this script.')

    return parser.parse_args()

def load_config(args):
    print('\n\n')
    print(py_version)
    print('Config file:', args.cfg_path)
    print('------------------------------------------------')
    with open(args.cfg_path, 'r') as f:
        return Config(f)

def train_and_save_clf(samples, dim, model_name, cfg):
    # Form the training data
    if dim == 1:
        X_train = [[sample.secOfDay] for sample in samples]
    elif dim == 2:
        X_train = [[sample.secOfDay, sample.value] for sample in samples]

    # Init and train the classifier
    clf = IsolationForest(random_state=0, 
                          contamination=cfg.sklearn.isolation_forest.contamination).fit(X_train)

    # Save the trained classifier
    with open('models/'+model_name+'.clf', 'wb') as f:
        pickle_dump(clf, f)


def init_models(cfg, owners=['pn']):
    
    models = {}
    for owner in owners:
        models[owner] = {}
        for location in cfg.project.keys():
            models[owner][location] = {}
            for quantity in cfg.project[location].keys():
                sensors = cfg.project[location][quantity].sensors.data
                dim = cfg.project[location][quantity].dim

                # Init quantity
                models[owner][location][quantity] = {
                    'active': '',
                    'available': {},
                    'sensors': sensors,
                    'dim': dim
                }

                # Get samples for training
                date_from = '2019-12-20'
                date_to = '2019-12-31'
                model_name = owner+':'+location+':'+quantity+':'+'&'.join(sensors)
                model_name += ':'+date_from+'&'+date_to

                samples = get_samples(topic='smarthome/'+location+'/'+quantity,
                                      date_from=date_from,
                                      date_to=date_to,
                                      sensors=sensors,
                                      owners=owners,
                                      cfg=cfg)

                # Train and save the default classifier
                train_and_save_clf(samples, dim, model_name, cfg)

                # Register the classifier to models.json
                clf_metadata = {
                    'sensors': sensors,
                    'n_samples': len(X_train),
                    'date_from': date_from,
                    'date_to': date_to
                }

                models[owner][location][quantity]['active'] = model_name
                models[owner][location][quantity]['available'][model_name] = clf_metadata

    # Save the models metadata
    with open('models.json', 'w') as f:
        dump_json(models, f)

if __name__ == '__main__':
    
    # Parse arguments
    args = parse_arguments()

    # Print Python version, load project configuration
    cfg = load_config(args)

    if args.mode == 'init':
        init_models(cfg)