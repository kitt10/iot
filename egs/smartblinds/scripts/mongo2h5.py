from yaml import full_load as yaml_full_load
from pymongo import MongoClient
from collections import OrderedDict
from datetime import datetime
from time import mktime
import numpy as np
import h5py
import random
from random import shuffle


class Mongo:

    def __init__(self, cfg):
        self.cfg = cfg
        self.mongoClient = MongoClient(self.cfg['mongo']['host'], self.cfg['mongo']['port'])
        self.database = self.mongoClient[self.cfg['mongo']['database']]
        self.collection = self.database[self.cfg['mongo']['collection']]

    def read(self, query, where_str):
        # read and sort by timestamp, apply where string

        return self.collection.find(query).sort('timestamp', -1).where(where_str)

    def log(self, buf):
        if self.cfg['verbose']:
            print('[MONGO LOG]:', buf)


def load_yml(file_path):
    with open(file_path, 'r') as fr:
        yml_data = yaml_full_load(fr)

    log('Yml file '+str(file_path)+' loaded.', True)
    return yml_data

def log(buf, verbose):
    if verbose:
        print('[LOG]:', buf)

def load_task(cfg):
    task_all = load_yml(cfg['data']['task_file_path'])
    taskF = OrderedDict()
    taskT = OrderedDict()

    for feature in task_all['features']:
        taskF[feature['name']] = (feature['type'], feature['min'], feature['max'])

    for target in task_all['targets']:
        taskT[target['name']] = (target['type'], target['min'], target['max'])

    return taskF, taskT

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def norm(value, a_type, a_min, a_max):
    if a_type == 'boolean':
        return int(value)
    else:
        return (value-a_min)/(a_max-a_min)

def make_vector(data, taskInfo):
    return [norm(data[name], *info) for name, info in taskInfo.items()]

def make_matrix(data, key, taskInfo):
    return np.array([make_vector(obs[key], taskInfo) for obs in data])

def ratios2ranges(length, ratios, batch_size):
    points_rel = list([0, ratios[0]])
    for i in range(1, len(ratios)):
        points_rel.append(ratios[i] + points_rel[i])
    points = [int(length * point_rel / batch_size) * batch_size for point_rel in points_rel]
    return [[points[i], points[i+1]] for i in range(len(points)-1)]

def split_data(X, Y, cfg, cfgnn, shuffle_data = True):
    log("Splitting data", cfg['verbose'])
    if shuffle_data:
        seed = random.random()
        random.seed(seed)
        shuffle(X)
        random.seed(seed)
        shuffle(Y)

    split_ranges = ratios2ranges(len(X), cfg['data']['split_ratios'], cfgnn['batch_size'])
    split = dict(zip(cfg['data']['split_name_suffixes'], split_ranges))

    X_split = dict()
    Y_split = dict()
    for suff in split:
        X_split[suff] = np.array(X[split[suff][0]:split[suff][1]])
        Y_split[suff] = np.array(Y[split[suff][0]:split[suff][1]])
    
    return X_split, Y_split

def save2h5(X_split, Y_split, cfg, nn):
    log('Saving data', cfg['verbose'])
    # Save datasets to a .h5 file
    # Datasets are dictionaries with suffixes as keys ('' for train, '_val' for validation and '_test' for testing)

    # Make file path
    out_file = cfg['data']['out_path']+cfg['data']['from']+'_'+cfg['data']['until']+'_%s.h5' % nn

    with h5py.File(out_file, 'w') as fw:
        for suff in X_split:
            fw.create_dataset('x%s'%suff, data=X_split[suff])
            fw.create_dataset('y%s'%suff, data=Y_split[suff])

    log('Data saved to '+out_file, cfg['verbose'])
    log('Number of samples '+str(len(X_split[''])), cfg['verbose'])

def main(mongo, task, cfg, cfgnn, include_periodical=True, include_events=True):

    # Parse date to timestamp
    ts_from = mktime(datetime.strptime(cfg['data']['from'], "%d-%m-%Y").timetuple())
    ts_until = mktime(datetime.strptime(cfg['data']['until'], "%d-%m-%Y").timetuple())

    # Data search query
    query = {'timestamp': { "$gte" : ts_from, "$lte" : ts_until}}

    # Data restrictions

    per = 'false'
    evnt = 'false'
    testing_restr = ''
    if include_periodical: per = 'true'
    if include_events: evnt = 'true'
    if cfg["data"]["skip_testing"]: testing_restr = "&& !this.testing"

    where_str = '((this.periodical && %s) || (!this.periodical && %s))%s' % (per, evnt, testing_restr)

    log('Querying raw data', cfg['verbose'])
    # Read data from MongoDB
    data = list(mongo.read(query, where_str))
    log('Data queried', cfg['verbose'])

    # Limits
    taskF = task[0]
    taskT = task[1]

    n = len(taskF) # num of features
    t = cfgnn['lstm']['timesteps']

    X_ffnn = list()
    Y_ffnn = list()

    X_lstm = list()
    Y_lstm = list()

    k_ = len(data)

    b_ffnn = k_ // cfgnn['ffnn']['batch_size']
    k_ffnn = cfgnn['ffnn']['batch_size'] * b_ffnn

    b_lstm = k_ // cfgnn['lstm']['batch_size']
    k_lstm = cfgnn['lstm']['batch_size'] * b_lstm - t

    for i, item in enumerate(data):
        if cfg['verbose']: 
            printProgressBar(i, k_)
        if i<=k_ffnn:
            X_ffnn.append(make_vector(item['features'], taskF))
            Y_ffnn.append(make_vector(item['targets'], taskT))

        if i<=k_lstm:
            X_lstm.append(make_matrix(data[i:i+t], 'features', taskF))
            Y_lstm.append(make_vector(data[i+t-1]['targets'], taskT))
    log("", cfg['verbose'])

    data_prep = dict()
    data_prep['ffnn'] = (X_ffnn, Y_ffnn)
    data_prep['lstm'] = (X_lstm, Y_lstm)

    for nn in data_prep:
        X, Y = data_prep[nn]
        X_split, Y_split = split_data(X, Y, cfg, cfgnn[nn])
        save2h5(X_split, Y_split, cfg, nn)


if __name__ == '__main__':

    # Load config
    cfg = load_yml(file_path='cfg_mongo2h5.yml')
    cfgnn = load_yml(file_path='cfg_train_nn.yml')

    # Init MongoDB
    mongo = Mongo(cfg)

    # Load features / targets limits
    task = load_task(cfg)

    # Load and save data
    main(mongo, task, cfg, cfgnn)
