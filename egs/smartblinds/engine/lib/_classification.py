import abc

class Classifier(abc.ABC):
    
    def __init__(self, app, name):
        self.app = app
        self.name = name
        self.trainable = False
        self.train_time = 0
        self.control_time = 0
        self.last_trained = 0
    
    @abc.abstractmethod
    def control(self, features):
        pass
    
    def train(self, data):
        pass
        