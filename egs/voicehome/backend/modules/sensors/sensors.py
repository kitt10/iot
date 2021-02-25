from modules.voicehome_module import VoicehomeModule
import json
import os
import re


class Sensors(VoicehomeModule):

    def __init__(self, engine, dir_path):
        VoicehomeModule.__init__(self, engine, dir_path)

    def get_current_temperature(self):
        payload = {
            'command': 'measure_now',
            'quantity': 'temperature'
        }
        self.mqtt_publish(topic='voicehome/sensors/commands', payload=payload)
        print('Module '+self.id+': command to measure temperature sent.')

    def on_mqtt_message(self, msg):
        print("ted")
        msg=msg.payload.decode('utf8').replace("'", '"')
        msg=json.loads(msg)
        if msg["key"] == "current_temperature":
            self.reply(message='Aktuální teplota je: '+str(msg['value']))

    def on_websocket_message(self, msg):
        print('Module '+self.id+": start sending websocket")
        print(msg)
        if msg['message'] == "whole_temperature_data":
            msg['reply'] = self.whole_temperature_data(msg)
            self.websocket_send(msg)
        if msg['message'] == "whole_pressure_data":
            msg['reply'] = self.whole_pressure_data(msg)
            self.websocket_send(msg)
        if msg['message'] == "sensorsList":
            msg['reply'] = self.sensorsList(msg)
            self.websocket_send(msg)
        print("Sensors: websocket sended")
        pass

    # call function from string in json
    # def omg():
    #     print("hi")
    # test = eval("omg")
    # test()

    def sensorsList(self, msg):
        print('Module '+self.id+": sensorsList")
        # print(os.getcwd())
        with open('modules/sensors/sensorsList.json') as json_file:
            data = json.load(json_file)
            print(data)
        return data
        # return 1

    # def whole_temperature_data(self, msg):
    #     print('Module '+self.id+": sending whole temperature data")
    #     query = {'key': 'voicehome/sensors/temperature'}
    #     res = self.search_mongo(self.id, query)
    #     buffer = []
    #     for res_i in res:
    #         # result_i = res_i["payload"].decode("utf8")
    #         result_i = res_i["payload"]
    #         buffer.append(json.loads(result_i))
    #     return buffer

    def whole_temperature_data(self, msg):
        print('Module '+self.id+": sending whole temperature data")
        sensorsListFile = self.sensorsList('')
        sensorsTemperatureList = sensorsListFile['temperature']
        roomList = []
        for i in sensorsTemperatureList:
            roomList.append(i['room'])
        maxRoomNum = sensorsListFile['max_room']
        query = {'key': 'voicehome/sensors/temperature'}
        pattern = re.compile("^(room_)(\d)+$")
        res = self.search_mongo(self.id, query)
        buffer = ''
        for res_i in res:
            # result_i = res_i["payload"].decode("utf8")
            result_i = json.loads(res_i["payload"])

            loc = result_i['location']
            if not pattern.match(loc):
               continue
            loc = loc.replace('room_', '')
            loc = int(loc)

            buffer= buffer + (result_i['timestamp'].replace('-', '/') + loc * ',' + str(result_i['temperature_value']) + (
                        maxRoomNum - loc) * ',' + '\n')

        return buffer

    def whole_pressure_data(self, msg):
        print('Module '+self.id+": sending whole pressure data")
        query = {'key': 'voicehome/sensors/pressure'}
        res = self.search_mongo(self.id, query)
        buffer = []
        for res_i in res:
            # result_i = res_i["payload"].decode("utf8")
            result_i = res_i["payload"]
            buffer.append(json.loads(result_i))
        return buffer
