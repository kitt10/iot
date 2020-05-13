### plot_prediction.py

#### args
> **-t** &nbsp;&nbsp;&nbsp; topic &nbsp;&nbsp;&nbsp; smarthome/room/illuminance

> **-df** &nbsp;&nbsp;&nbsp; date_from &nbsp;&nbsp;&nbsp; 2020-01-01

> **-dt** &nbsp;&nbsp;&nbsp; date_to &nbsp;&nbsp;&nbsp; 2020-04-15

> **-yl** &nbsp;&nbsp;&nbsp; ylim &nbsp;&nbsp;&nbsp; 0 450

> **-yb** &nbsp;&nbsp;&nbsp; ylabel &nbsp;&nbsp;&nbsp; lux

#### usage examples
```console
$ python plot_prediction.py -t smarthome/room/illuminance -df 2020-01-01 -dt 2020-04-30 -yb lux -yl 0 500

$ python plot_prediction.py -t smarthome/outside/temperature -df 2020-01-01 -dt 2020-01-15 -yb degC -yl -5 25

$ python plot_prediction.py -t smarthome/room/motion -df 2020-01-01 -dt 2020-01-01
```