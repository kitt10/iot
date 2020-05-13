from pymongo import MongoClient
from json import loads as json_loads
from datetime import datetime, date, time as dtTime
from argparse import ArgumentParser
from sklearn.ensemble import IsolationForest
from matplotlib import pyplot as plt
import time
import numpy as np
import matplotlib as mpl
mpl.rcParams['axes.labelsize'] = 13
mpl.rcParams['xtick.labelsize'] = 13
mpl.rcParams['ytick.labelsize'] = 13
mpl.rcParams['legend.fontsize'] = 13
mpl.rcParams['axes.titlesize'] = 13
mpl.rcParams['axes.titlepad'] = 7

quantity2dim = {
    'temperature': 2,
    'illuminance': 2,
    'humidity': 2,
    'pressure': 2,
    'motion': 1,
    'door_open': 1,
    'window_open': 1
}

class Sample:
    
    def __init__(self, data, today):
        self.status = data['status']
        self.quantity = data['quantity']
        self.sensor_id = data['sensor_id']
        self.timestamp = data['timestamp']
        self.sec1970 = int(time.mktime(datetime.strptime(self.timestamp, '%Y-%m-%d %H:%M:%S').timetuple()))
        self.date = datetime.fromtimestamp(self.sec1970).date()
        self.daysAgo = (today - self.date).days
        #self.secOfDay = self.sec1970 - datetime.combine(self.date, dtTime.min).timestamp()
        tmp = datetime.combine(self.date, dtTime.min)
        self.secOfDay = self.sec1970 - int((time.mktime(tmp.timetuple())+tmp.microsecond/1000000.0))
        self.value = float(data['value'])
        self.owner = data['owner']
        self.location = data['location']


def parse_arguments():
    parser = ArgumentParser(description='Train classifier and plot quantity prediction.')
    parser.add_argument('-df', '--date_from', type=str, required=False, default='2020-04-01',
                        help='Starting date for data collection.')
    parser.add_argument('-dt', '--date_to', type=str, required=False, default='2020-04-30',
                        help='Ending date for data collection.')
    parser.add_argument('-t', '--topic', type=str, required=False, default='smarthome/room/temperature',
                        help='MQTT topic')
    parser.add_argument('-yl', '--ylim', type=int, nargs='+', required=False, default=[10, 30],
                        help='Plot y limit')
    parser.add_argument('-yb', '--ylabel', type=str, required=False, default='deg C',
                        help='Plot y label')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    mongoClient = MongoClient('localhost', 27017)
    db = mongoClient.smarthome   # database
    db_collection = db.testing   # collection

    today = date.today()
    days_ago_start = (today - datetime.strptime(args.date_from, '%Y-%m-%d').date()).days
    days_ago_end = (today - datetime.strptime(args.date_to, '%Y-%m-%d').date()).days

    project, location, quantity = args.topic.split('/')
    owners = ('pn',)
    out_file_name_base = args.topic.replace('/', '_')+':'+args.date_from.replace('-', '_')+':'+args.date_to.replace('-', '_')

    # collect data
    if 'illuminance' in args.topic:
        topic_clean = args.topic+'/'
    else:
        topic_clean = args.topic

    samples = list()
    for item in db_collection.find({'topic': topic_clean}):
        try:
            d = json_loads(item['payload'].decode('utf-8'))
        except AttributeError:
            d = json_loads(item['payload'])

        sample = Sample(data=d, today=today)
        if sample.status == 'ok' \
            and days_ago_end <= sample.daysAgo <= days_ago_start \
                and sample.owner in owners:
            samples.append(sample)

    if not samples:
        print('No samples for this settings.')
        exit()

    # form the training data
    if quantity2dim[quantity] == 1:
        X_train = [[sample.secOfDay] for sample in samples if sample.value == 1]
    elif quantity2dim[quantity] == 2:
        X_train = [[sample.secOfDay, sample.value] for sample in samples]

    # train a classifier
    clf = IsolationForest(random_state=0, contamination=0.1).fit(X_train)

    # get predictions and plot it all
    plt.figure(figsize=(10, 4))
    plt.title(args.topic+' | '+args.date_from+' ~ '+args.date_to+' | '+str(len(samples))+' samples', loc='center')
    if quantity2dim[quantity] == 1:
        xx = np.linspace(0, 86400)
        scores = clf.decision_function([[xxx] for xxx in xx]).reshape(xx.shape)
        plt.plot(xx, scores)
        plt.ylabel('anomaly score')
        plt.grid()

    elif quantity2dim[quantity] == 2:
        xx, yy = np.meshgrid(np.linspace(0, 86400), np.linspace(args.ylim[0], args.ylim[1]))
        scores = clf.decision_function(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
        plt.contourf(xx, yy, scores, cmap=plt.cm.rainbow)
        cb = plt.colorbar()
        cb.ax.set_ylabel('anomaly score')
        plt.ylabel(args.ylabel)
    
    plt.xticks([h*3600 for h in range(25) if h%2==0], [h for h in range(25) if h%2==0])
    plt.xlabel('time of day [h]')
    plt.tight_layout()

    # save the plot
    plt.savefig('../plots/'+out_file_name_base+'.png', pad_inches='tight')
    plt.show()
    
    # save an info file
    with open('../plots/'+out_file_name_base+'.info', 'w') as f:
        f.write('topic: '+args.topic+'\n')
        f.write('date from: '+args.date_from+'\n')
        f.write('date to: '+args.date_to+'\n')
        f.write('project: '+project+'\n')
        f.write('location: '+location+'\n')
        f.write('quantity: '+quantity+'\n')
        f.write('owners: '+str(owners)+'\n')
        f.write('dim: '+str(quantity2dim[quantity])+'\n')
        f.write('n samples: '+str(len(samples))+'\n')
