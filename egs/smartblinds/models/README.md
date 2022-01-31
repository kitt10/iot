## Smartblinds: Models

Saved .h5 Keras models (see https://keras.io).

Parameters in CFG file: ```/scripts/cfg_train_nn.yml```

---

### FeedForward model (```ffnn_best_<ts>.h5```)

Input: ```vector (n x 1)```
- ```n```: number of features (```n = 15```)

Output: ```vector (m x 1)```
- ```m```: number of targets (```m = 2```)

Script for training:  ```/scripts/train_ffnn.py```

---

### Recurrent (LSTM) model (```lstm_best_<ts>.h5```)

Input: ```matrix (n x t)```

- ```n```: number of features (```n = 15```), 
- ```t```: number of timesteps - history context considered (by default ```t = 64 ~ 64 x 5 minutes ~ 5-6 hours```)

Output: ```vector (m x 1)```
- ```m```: number of targets (```m = 2```)

Script for training:  ```/scripts/train_lstm.py```

---

#### Features order: 
```
[
    'year_day', 
    'week_day', 
    'day_secs', 
    'home', 
    'temp_in', 
    'temp_out', 
    'lum_in', 
    'lum_out', 
    'owm_temp_max', 
    'owm_temp_1h', 
    'owm_temp_2h', 
    'owm_temp_3h', 
    'owm_code', 
    'owm_wind_speed', 
    'owm_wind_heading'
]
```

#### Targets order: 
```
[
    'position', 
    'tilt'
]
```
