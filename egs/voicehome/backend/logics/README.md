### Voicehome Logic

Defines the way how the commands from the controller are absorbed, evaluated and passed to modules.

#### BasicLogic ```basic.py```
* command ~ list of strings: ```s1 s2 s3``` (e.g. ```"turn" "led" "on"```)
* move activating calls ~ list of lists of strings:
    ```
    [[s11, s12, s13],
     [s21, s22],
     [s31, s32, s33, s34]
     [s41, s42, s43]]    
    ```
    e.g.
    ```
    [["switch", "led", "on"],
     ["light", "up"],
     ["turn", "the", "led", "on"],
     ["turn", "led", "on"]]    
    ```
* based on the **BasicLogic**, the move is activated if and only if one of the given call options, considered as a set of words, is a subset of the command (considered as a set of words).