import abc
from ._tools import dump_task
from collections import OrderedDict
from keras.models import load_model

class Classifier(abc.ABC):
    
    def __init__(self, app, name, trainable, ind):
        self.app = app
        self.name = name
        self.ind = ind
        self.trainable = False
        self.train_time = 0
        self.control_time = 0
        self.last_trained = 0
        self.n_samples = 0
        self.trainable = trainable

        # Load trained model
        if trainable:
            self.model = load_model(app.cfg['classification'][name + '_model'])
            print(name.upper() + ' model loaded.')
            self.model.summary()

        # Prepare env
        self.taskF = OrderedDict()
        self.taskT = OrderedDict()
        self.get_task_info()
    
    @abc.abstractmethod
    def control(self, features):
        pass
    
    def train(self, data):
        pass
    
    def dump_metadata(self):
        task = self.app.task
        task['classifiers'][self.ind]['nSamples'] = self.n_samples
        task['classifiers'][self.ind]['retrained'] = self.last_trained
        task['classifiers'][self.ind]['trainTime'] = self.train_time
        task['classifiers'][self.ind]['controlTime'] = self.control_time
        dump_task(self.app.cfg, task)

    def get_task_info(self):
        for feature in self.app.task['features']:
            self.taskF[feature['name']] = (feature['type'], feature['min'], feature['max'])

        for target in self.app.task['targets']:
            self.taskT[target['name']] = (target['type'], target['min'], target['max'])