from yaml import full_load as yaml_full_load
from pymongo import MongoClient
from collections import OrderedDict
from datetime import datetime
from time import mktime
import numpy as np
import h5py


class Mongo:

    def __init__(self, cfg):
        self.cfg = cfg
        self.mongoClient = MongoClient(self.cfg['mongo']['host'], self.cfg['mongo']['port'])
        self.database = self.mongoClient[self.cfg['mongo']['database']]
        self.collection = self.database[self.cfg['mongo']['collection']]

    def read(self, query):
        # read and sort by timestamp

        return self.collection.find(query).sort('timestamp', -1)

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

def norm(value, a_type, a_min, a_max):
    if a_type == 'boolean':
        return int(value)
    else:
        return (value-a_min)/(a_max-a_min)

def make_vector(data, taskInfo):
    return [norm(data[name], *info) for name, info in taskInfo.items()]

def save2h5(X, Y, cfg):
    # Save dataset to a .h5 file

    # Make file path
    out_file = cfg['data']['out_path']+cfg['data']['from']+'_'+cfg['data']['until']+'.h5'

    with h5py.File(out_file, 'w') as fw:
        fw.create_dataset('X', data=np.array(X))
        fw.create_dataset('Y', data=np.array(Y))

    log('Data saved to '+out_file, cfg['verbose'])
    log('Number of samples '+str(len(X)), cfg['verbose'])

def main(mongo, task, cfg, include_periodical=True, include_events=True, skip_testing=True):

    # Parse date to timestamp
    ts_from = mktime(datetime.strptime(cfg['data']['from'], "%d-%m-%Y").timetuple())
    ts_until = mktime(datetime.strptime(cfg['data']['until'], "%d-%m-%Y").timetuple())

    # Data search query
    query = {'timestamp': { "$gte" : ts_from, "$lte" : ts_until}}

    # Read data from MongoDB
    data = mongo.read(query)

    # Limits
    taskF = task[0]
    taskT = task[1]

    X = list()
    Y = list()
    for item in data:
        if item['testing'] and skip_testing:
            continue

        if (item['periodical'] and include_periodical) or (not item['periodical'] and include_events):
            X.append(make_vector(item['features'], taskF))
            Y.append(make_vector(item['targets'], taskT))

    save2h5(X, Y, cfg)


if __name__ == '__main__':

    # Load config
    cfg = load_yml(file_path='cfg_mongo2h5.yml')

    # Init MongoDB
    mongo = Mongo(cfg)

    # Load features / targets limits
    task = load_task(cfg)

    # Load and save data
    main(mongo, task, cfg)
