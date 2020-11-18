### Voicehome Controller

A general way of how to control the behavior of your modules. It is based on the ```socket``` module.

##### Keyboard Controller
1. Run the controller:
    ```
    $ conda activate iot    # (RPi: $ source activate iot)
    $ cd voicehome/backend/controllers
    $ python keyboard.py
    ```
2. Test your commands

> *Note*: If you set up the RPi's socket binding IP in the config.yml file, you can access it and control your modules from anywhere. 


##### VoiceKit Controller ([Google AYI VoiceKit][1])

Based on the same principle, except using ASR (Automatic Speech Recognition) and ASS (Automatic Speech Synthesis) instead of the keyboard.

- connect the VoiceKit (data USB port) to your laptop
- wait for VoiceKit initialization (3-5 minutes)
- when initialized, check the status at ```voicekit.local:8889``` (the log)
- in ``` http://voicekit.local:8888/edit/voicekit_controller.py ``` set up the correct ```host``` (IP address) and sockets ```port``` of the engine, save ```voicekit_controller.py```
- start the dialog by pushing the button

[1]: https://aiyprojects.withgoogle.com/voice/