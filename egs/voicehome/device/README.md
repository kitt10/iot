# Physical Devices

All the code running peripheries of this project.

- ESP -

## Folders

**esp_sub&pub** - (is old version!) In esp_sub&pub folder is code for esp to able esp sub and pub concurrently. It is including pub of bme280, ds18b20, tsl2591 sensors. It will be use like template for following building.


##esp*
All esp waiting a few seconds during boot for user input whether is need to cancel script and use esp manualy
All esp sending led and lights states to raspberry after boot
All esp sync time immediately after boot

To change wifi, password, topics or other parameters that are sensing to raspberry pi go to the config.py

To change frequency of sending a data -> change line in main.py
```if(mqtt_client.last_minute_sent != mqtt_client.get_min() and mqtt_client.get_sec() in range(20, 23))```


To-do list to add new sensor into a script

In mqttclient.py:

- initialize sensor in __init__ constructior of Client class
- change function send2broker for sending data to raspberry pi
- change function send2broker_measure_now for measuring data now and send it to raspberry pi
- change subscription topics in function sub_cb 

###**esp1**
 - In esp1 folder is code for first eps connected to bme280 sensor.

###**esp2** 
- In esp2 folder is code for second eps connected to ds12b20 sensor.

###**esp3** 
- In esp3 folder is code for third eps connected to tsl2591 sensor

