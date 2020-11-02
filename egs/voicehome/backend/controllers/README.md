### Voicehome Controller

A general way of how to control the behavior of your modules. It is based on Python ```socket``` module.

##### Keyboard Controller
1. Run the controller:
    ```
    $ conda activate iot    # (RPi: $ source activate iot)
    $ cd voicehome/backend/controllers
    $ python keyboard.py
    ```
2. Test your commands

> *Note*: If you set up the RPi's socket binding IP in the config.yml file, you can access it and control your modules from anywhere. 


##### VoiceKit Controller

Coming soon. Based on the same principle, except using ASR (Automatic Speech Recognition) and ASS (Automatic Speech Synthesis) instead of the keyboard.