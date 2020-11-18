### Installation

``` $ git clone https://github.com/kitt10/iot.git ```

#### Mac

``` 
$ cd iot
$ conda env create -f iotenv.yml
$ conda activate iot
```

> *Note*: Might need to install some packages not included in ```iotenv.yml```, the default needs are: ```paho-mqtt```, ```python-box```, ```pymongo```, ```tornado```

#### RPi

##### Conda installation

```
$ wget http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-armv7l.sh
$ sudo /bin/bash Miniconda3-latest-Linux-armv7l.sh    # -> change default directory to /home/<user>/miniconda3
$ sudo nano /home/<user>/.bashrc    # -> add: export PATH="/home/pi/miniconda3/bin:$PATH"
$ sudo chown -R <user> /home/<user>/miniconda3    # if needed
```

##### Project packages installation

```
$ conda config --add channels rpi
$ conda create -n iot python=3.6    # highest supported on RPi
$ source activate iot
(iot) $ python -m easy_install paho-mqtt
(iot) $ python -m easy_install python-box
(iot) $ python -m easy_install pymongo
(iot) $ python -m easy_install tornado
```

##### Config file ```config.yml```

- on RPi set up the IP for socket binding ```socket.host: 147.228.124.230```

### Run

##### Run engine
```
$ conda activate iot    # (RPi: $ source activate iot)
(iot) $ cd iot/egs/voicehome/backend
(iot) $ python engine.py
```

##### Run controller

- keyboard controller (from anywhere): 
```
$ conda activate iot    # (RPi: $ source activate iot)
(iot) $ cd iot/egs/voicehome/backend/controllers
(iot) $ python keyboard.py
```

- VoiceKit controller (from anywhere): 

    - connect the VoiceKit (data USB port) to your laptop
    - wait for VoiceKit initialization (3-5 minutes)
    - when initialized, check the status at ```voicekit.local:8889``` (the log)
    - in ``` http://voicekit.local:8888/edit/voicekit_controller.py ``` set up the correct ```host``` (IP address) and sockets ```port``` of the engine, save ```voicekit_controller.py```
    - start the dialog by pushing the button
    
##### Web GUI Access

- Your PC: ```localhost:8881```
- RPi (from anywhere): ```147.228.124.230:8881```

### Development - project extension

- **Frontend**: see ```voicehome/frontend/README.md```
- **Modules**: see ```voicehome/backend/modules/README.md```
- **Logic**: see ```voicehome/backend/logics/README.md```

