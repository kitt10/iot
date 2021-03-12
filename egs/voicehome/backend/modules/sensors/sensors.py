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
        self.sensorsState = {}

        self.voicekit_asked_current_measure_for_quantity = []

    def get_current_temperature(self):
        self.sensorMeasureNow('ds18b20_1','temperature', 'voicekit')
        self.voicekit_asked_current_measure_for_quantity.append('temperature')

    def get_current_pressure(self):
        self.sensorMeasureNow('bme280_1','pressure', 'voicekit')
        self.voicekit_asked_current_measure_for_quantity.append('pressure')

    def get_current_humidity(self):
        self.sensorMeasureNow('bme280_1','humidity', 'voicekit')
        self.voicekit_asked_current_measure_for_quantity.append('humidity')

    def get_current_illuminance(self):
        self.sensorMeasureNow('tsl2591_1','illuminance', 'voicekit')
        self.voicekit_asked_current_measure_for_quantity.append('illuminance')




    def sensorMeasureNow(self, SENSOR_ID,quantity_type, who_asking):
        payload = {
            'command': 'measure_now',
            'sensor_ID': SENSOR_ID,
            'quantity_type': quantity_type,
            'who_asking': who_asking
        }
        self.mqtt_publish(topic='voicehome/sensors/command', payload=payload)
        print('Module ' + self.id + ': command to measure sent for '+ SENSOR_ID+ 'sensor.')

    def on_mqtt_message(self, msg):
        topic = msg.topic
        # if msg.topic == 'voicehome/sensors/command':
        try:
            msg = msg.payload.decode('utf8')
        except:
            msg = msg.payload #.replace("'", '"')
            pass
        # msg = msg.payload

        msg = json.loads(msg)
        if topic == 'voicehome/sensors/command':
            if "command" in msg.keys():
                if msg["command"] == "measure_now":
                    if msg['who_asking'] == 'voicekit':
                        for x in msg.keys():
                            x_match = self.pattern_value.match(x)
                            if (x_match):

                                if x_match.string.split('_')[0] == 'temperature' and 'temperature' in self.voicekit_asked_current_measure_for_quantity:
                                    self.reply(message='Aktuální teplota je: ' + str(msg[x_match.string]))
                                    self.voicekit_asked_current_measure_for_quantity = list(filter(lambda a: a != 'temperature', self.voicekit_asked_current_measure_for_quantity))
                                    break
                                elif x_match.string.split('_')[0] == 'pressure' and 'pressure' in self.voicekit_asked_current_measure_for_quantity:
                                    self.reply(message='Aktuální tlak je: ' + str(msg[x_match.string]))
                                    self.voicekit_asked_current_measure_for_quantity = list(filter(lambda a: a != 'pressure',
                                                self.voicekit_asked_current_measure_for_quantity))
                                    break
                                elif x_match.string.split('_')[0] == 'humidity' and 'humidity' in self.voicekit_asked_current_measure_for_quantity:
                                    self.reply(message='Aktuální vlhkost je: ' + str(msg[x_match.string]))
                                    self.voicekit_asked_current_measure_for_quantity = list(filter(lambda a: a != 'humidity',
                                                self.voicekit_asked_current_measure_for_quantity))
                                    break
                                elif x_match.string.split('_')[0] == 'illuminance' and 'illuminance' in self.voicekit_asked_current_measure_for_quantity:
                                    self.reply(message='Aktuální intenzita světla je: ' + str(msg[x_match.string]))
                                    self.voicekit_asked_current_measure_for_quantity = list(filter(lambda a: a != 'illuminance',
                                                self.voicekit_asked_current_measure_for_quantity))
                                    break
                        return
        for x in msg.keys():
            x_match = self.pattern_value.match(x)
            if (x_match):
                self.sensorsState[msg['sensor_id'] + "-" + x_match.string.split("_")[0]] = {"state": msg['state'],
                                                                                           "timestamp": msg['timestamp'],
                                                                                           "sensor_id": msg["sensor_id"],
                                                                                           "location": msg["location"],
                                                                                           "value": msg[x_match.string]
                                                                                           }
                # self.sensorsState[msg['sensor_id']+"_"+msg["quantity"]] = {"state": msg['state'],
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
        if msg['message'] == "sensorsState":
            msg['reply'] = self.sensorsState
            self.websocket_send(msg)
        print("Sensors: websocket sended")
        pass

    def reloadSensorsList(self):
        print('Module ' + self.id + ": reloadSensorsList")
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
    #         if result_i['state']=='error':
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
    #         if result_i['state']=='error':
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
    #         if result_i['state']=='error':
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
