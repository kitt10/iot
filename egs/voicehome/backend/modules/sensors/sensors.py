from modules.voicehome_module import VoicehomeModule
import json
import os
import re


class Sensors(VoicehomeModule):

    def __init__(self, engine, dir_path):
        VoicehomeModule.__init__(self, engine, dir_path)
        self.pattern_value = re.compile("^[a-z]+(_value)$")
        self.sensorsList = {}
        self.reloadSensorsList()
        self.sensorsStatus = {}

    def get_current_temperature(self):
        payload = {
            'command': 'measure_now',
            'quantity': 'temperature'
        }
        self.mqtt_publish(topic='voicehome/sensors/commands', payload=payload)
        print('Module ' + self.id + ': command to measure temperature sent.')

    def on_mqtt_message(self, msg):
        msg = msg.payload.decode('utf8').replace("'", '"')
        msg = json.loads(msg)
        if "key" in msg.keys():
            if msg["key"] == "current_temperature":
                self.reply(message='Aktuální teplota je: ' + str(msg['value']))
                return
        else:
            for x in msg.keys():
                x_match = self.pattern_value.match(x)
                if (x_match):
                    self.sensorsStatus[msg['sensor_id'] + "-" + x_match.string.split("_")[0]] = {"status": msg['status'],
                                                                                               "timestamp": msg['timestamp'],
                                                                                               "quantity": msg["quantity"],
                                                                                               "sensor_id": msg["sensor_id"],
                                                                                               "location": msg["location"],
                                                                                               "value": msg[x_match.string]
                                                                                               }
                    # self.sensorsStatus[msg['sensor_id']+"_"+msg["quantity"]] = {"status": msg['status'],
                    #                                                             "timestamp": msg['timestamp']
                    #                                                             }
                    break

    def on_websocket_message(self, msg):
        print('Module ' + self.id + ": start sending websocket")
        print(msg)
        if msg['message'] == "whole_temperature_data":
            msg['reply'] = self.whole_temperature_data(msg)
            self.websocket_send(msg)
        if msg['message'] == "whole_pressure_data":
            msg['reply'] = self.whole_pressure_data(msg)
            self.websocket_send(msg)
        if msg['message'] == "whole_illuminance_data":
            msg['reply'] = self.whole_illuminance_data(msg)
            self.websocket_send(msg)
        if msg['message'] == "sensorsList":
            msg['reply'] = self.sensorsList
            self.websocket_send(msg)
        if msg['message'] == "sensorsStatus":
            msg['reply'] = self.sensorsStatus
            self.websocket_send(msg)
        print("Sensors: websocket sended")
        pass

    def reloadSensorsList(self):
        print('Module ' + self.id + ": sensorsList")
        # print(os.getcwd())
        with open('modules/sensors/sensorsList.json') as json_file:
            self.sensorsList = json.load(json_file)

    def whole_temperature_data(self, msg):
        print('Module ' + self.id + ": sending whole temperature data")
        query = {'key': 'voicehome/sensors/temperature'}
        res = self.search_mongo(self.id, query)
        buffer = []
        for res_i in res:
            # result_i = res_i["payload"].decode("utf8")
            result_i = res_i["payload"]
            buffer.append(json.loads(result_i))
        return buffer

    def whole_illuminance_data(self, msg):
        print('Module ' + self.id + ": sending whole illuminance data")
        query = {'key': 'voicehome/sensors/illuminance'}
        res = self.search_mongo(self.id, query)
        buffer = []
        for res_i in res:
            # result_i = res_i["payload"].decode("utf8")
            result_i = res_i["payload"]
            buffer.append(json.loads(result_i))
        return buffer

    # def whole_temperature_data(self, msg):
    #     print('Module '+self.id+": sending whole temperature data")
    #     sensorsListFile = self.sensorsList('')
    #     sensorsTemperatureList = sensorsListFile['temperature']
    #     roomList = []
    #     for i in sensorsTemperatureList:
    #         roomList.append(i['room'])
    #     maxRoomNum = sensorsListFile['max_room']
    #     query = {'key': 'voicehome/sensors/temperature'}
    #     pattern = re.compile("^(room_)(\d)+$")
    #     res = self.search_mongo(self.id, query)
    #     buffer = ''
    #     for res_i in res:
    #         result_i = res_i["payload"].decode("utf8")
    #         result_i = json.loads(res_i["payload"])
    #
    #         if result_i['status']=='error':
    #             continue
    #         loc = result_i['location']
    #         if not pattern.match(loc):
    #            continue
    #         loc = loc.replace('room_', '')
    #         loc = int(loc)
    #
    #         buffer= buffer + (result_i['timestamp'].replace('-', '/') + loc * ',' + str(result_i['temperature_value']) + (
    #                     maxRoomNum - loc) * ',' + '\n')
    #
    #     return buffer

    # def whole_illuminance_data(self, msg):
    #     print('Module '+self.id+": sending whole illuminance data")
    #     sensorsListFile = self.sensorsList('')
    #     sensorsIlluminanceList = sensorsListFile['illuminance']
    #     roomList = []
    #     for i in sensorsIlluminanceList:
    #         roomList.append(i['room'])
    #     maxRoomNum = sensorsListFile['max_room']
    #     query = {'key': 'voicehome/sensors/illuminance'}
    #     pattern = re.compile("^(room_)(\d)+$")
    #     res = self.search_mongo(self.id, query)
    #     buffer = ''
    #     for res_i in res:
    #         # result_i = res_i["payload"].decode("utf8")
    #         result_i = json.loads(res_i["payload"])
    #
    #         if result_i['status']=='error':
    #             continue
    #         loc = result_i['location']
    #         if not pattern.match(loc):
    #            continue
    #         loc = loc.replace('room_', '')
    #         loc = int(loc)
    #
    #         buffer= buffer + (result_i['timestamp'].replace('-', '/') + loc * ',' + str(result_i['illuminance_value']) + (
    #                     maxRoomNum - loc) * ',' + '\n')
    #
    #     return buffer

    def whole_pressure_data(self, msg):
        print('Module ' + self.id + ": sending whole pressure data")
        query = {'key': 'voicehome/sensors/pressure'}
        res = self.search_mongo(self.id, query)
        buffer = []
        for res_i in res:
            # result_i = res_i["payload"].decode("utf8")
            result_i = res_i["payload"]
            buffer.append(json.loads(result_i))
        return buffer

    # def whole_pressure_data(self, msg):
    #     print('Module '+self.id+": sending whole pressure data")
    #     sensorsListFile = self.sensorsList('')
    #     sensorsPressureList = sensorsListFile['pressure']
    #     roomList = []
    #     for i in sensorsPressureList:
    #         roomList.append(i['room'])
    #     maxRoomNum = sensorsListFile['max_room']
    #     query = {'key': 'voicehome/sensors/pressure'}
    #     pattern = re.compile("^(room_)(\d)+$")
    #     res = self.search_mongo(self.id, query)
    #     buffer = ''
    #     for res_i in res:
    #         # result_i = res_i["payload"].decode("utf8")
    #         result_i = json.loads(res_i["payload"])
    #
    #         if result_i['status']=='error':
    #             continue
    #         loc = result_i['location']
    #         if not pattern.match(loc):
    #            continue
    #         loc = loc.replace('room_', '')
    #         loc = int(loc)
    #
    #         buffer= buffer + (result_i['timestamp'].replace('-', '/') + loc * ',' + str(result_i['pressure_value']) + (
    #                     maxRoomNum - loc) * ',' + '\n')
    #
    #     return buffer
