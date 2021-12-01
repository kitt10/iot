import abc
from ._tools import dump_classifier_metadata

class Classifier(abc.ABC):
    
    def __init__(self, app, name, ind):
        self.app = app
        self.name = name
        self.ind = ind
        self.trainable = False
        self.train_time = 0
        self.control_time = 0
        self.last_trained = 0
        self.n_samples = 0
    
    @abc.abstractmethod
    def control(self, features):
        pass
    
    def train(self, (x_, y_)):
        pass
    
    def dump_metadata(self):
        task = self.app.task
        task['classifiers'][self.ind]['nSamples'] = self.n_samples
        task['classifiers'][self.ind]['retrained'] = self.last_trained
        task['classifiers'][self.ind]['trainTime'] = self.train_time
        task['classifiers'][self.ind]['controlTime'] = self.control_time
        dump_classifier_metadata(self.app.cfg, task)