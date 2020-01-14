from pymongo import MongoClient
from datetime import datetime, date, time as dtTime
from json import loads as loads_json
import time
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


def get_samples(topic, date_from, date_to, sensors, owners, cfg):

    mongoClient = MongoClient(cfg.mongo.host, cfg.mongo.port)
    db = mongoClient.smarthome   # database
    db_collection = db.testing   # collection

    today = date.today()
    days_ago_start = (today - datetime.strptime(date_from, '%Y-%m-%d').date()).days
    days_ago_end = (today - datetime.strptime(date_to, '%Y-%m-%d').date()).days

    _, location, quantity = topic.split('/')

    if 'illuminance' in topic:
        topic_clean = topic+'/'
    else:
        topic_clean = topic

    samples = list()
    for item in db_collection.find({'topic': topic_clean}):
        sample = Sample(data=loads_json(item['payload']), today=today)
        if sample.status == 'ok' \
            and days_ago_end <= sample.daysAgo <= days_ago_start \
                and sample.sensor_id in sensors \
                    and sample.owner in owners:
            samples.append(sample)

    return samples

def get_today_samples(topic, sensor, cfg, owners=['pn']):
    today = datetime.today().strftime('%Y-%m-%d')
    return get_samples(topic=topic, date_from=today, date_to=today, sensors=[sensor], owners=owners, cfg=cfg)