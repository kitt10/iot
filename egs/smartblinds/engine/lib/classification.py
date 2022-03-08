from .cl_ifelse import CL_Ifelse
from .cl_ffnn import CL_Ffnn
from .cl_lstm import CL_Lstm
from ._tools import dump_task, format_secs, norm as normalize
from time import time
from datetime import datetime

class Classification:
    
    def __init__(self, app):
        self.app = app
        self.cfg = app.cfg
        self.verbose = self.cfg['classification']['verbose']
        
        self.features = {f['name']:f for f in self.app.task['features']}
        self.targets = {t['name']:t for t in self.app.task['targets']}
        
        self.next_training = 0
        self.data_load_time = 0
        
        self.classifiers = {
            'ifelse': CL_Ifelse(app=self.app),
            'ffnn': CL_Ffnn(app=self.app),
            'lstm': CL_Lstm(app=self.app)
        }
        
    def get_control(self, classifier_name, features):
        cl = self.classifiers[classifier_name]
        t0 = time()
        position, tilt = cl.control(features)
        cl.control_time = time() - t0
        cl.dump_metadata()
        
        return {'status': 'ok', 'targets': {'position': position, 'tilt': tilt}, 'controlTime': cl.control_time}

    def predict(self, classifier_name, data):
        cl = self.classifiers[classifier_name]
        t0 = time()
        timestamps, predictions = cl.predict(data)
        predict_time = time() - t0
        positions = predictions[:, 0]
        tilts = predictions[:, 1]
        cl.dump_metadata()

        return {'predictions': [{'timestamp': t, 'targets': {'position': p, 'tilt': s}} for t,p,s in zip(timestamps, positions, tilts)]}
    
    def do_train(self, classifier_name, data):
        cl = self.classifiers[classifier_name]
        if cl.trainable:
            t0 = time()
            cl.train(data)
            cl.last_trained = time()
            cl.train_time = cl.last_trained - t0
            cl.n_samples = len(data[0])
            cl.dump_metadata()
            
            return {'status': 'ok', 'trainTime': cl.train_time, 'lastTrained': cl.last_trained, 'nSamples': cl.n_samples}
        else:
            return {'status': 'bad'}
        
    def train_now(self):
        self.retrain_all(plan_next=False)
        return {'classifierInfo': {cl.name:{'lastTrained': cl.last_trained, 'trainTime': cl.train_time, 'nSamples': cl.n_samples} for cl in self.classifiers.values()}}
        
    def retrain_all(self, plan_next=True):
        t0 = time()
        training_data = self.load_training_data()
        self.data_load_time = time()-t0
        self.log('Data loaded in '+format_secs(self.data_load_time)+' ('+str(len(training_data[0]))+' samples)')
        self.log('Retraining all classifiers...')
        for classifier in self.classifiers.values():
            if classifier.trainable:
                #self.do_train(classifier.name, training_data)      # TODO
                self.log('Classifier '+classifier.name+' retrained in '+str(round(classifier.train_time, 4))+' s ('+str(classifier.n_samples)+').')
        
        if plan_next:
            self.app.ws.plan_next_training()
        
    def load_training_data(self):
        raw_data = self.app.db.get_data()
        x_ = []
        y_ = []
        for sample in raw_data:
            x_.append([self.normalize(xi, self.features[f_name]['min'], self.features[f_name]['max'], self.features[f_name]['type']) for f_name, xi in sample['features'].items()])
            y_.append([self.normalize(yi, self.targets[t_name]['min'], self.targets[t_name]['max'], self.targets[t_name]['type']) for t_name, yi in sample['targets'].items()])
            
        return x_, y_
    
    def set_next_training(self, next_training):
        self.next_training = next_training
        self.app.task['taskInfo']['nextTraining'] = self.next_training
        dump_task(self.app.cfg, self.app.task)
        
    def log(self, buf):
        if self.verbose:
            print(datetime.now(), 'CL LOG:', buf)
        