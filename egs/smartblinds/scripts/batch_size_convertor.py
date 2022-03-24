import os
from keras.models import load_model, save_model
import sys

def convert(filename):
    if(x.startswith("ffnn_best_h")):
        for i in range(2):
            model_cfg['layers'][i]['config']['batch_input_shape'] = (1,15)
            new_model = model.__class__.from_config(model_cfg)
            new_model.set_weights(model.get_weights())
            save_model(new_model, path+"/converted/"+x[:22]+"pr_"+x[22:])
    if(x.startswith("lstm_best_h")):
        for i in range(2):
            model_cfg['layers'][i]['config']['batch_input_shape'] = (1,64,15)
            new_model = model.__class__.from_config(model_cfg)
            new_model.set_weights(model.get_weights())
            save_model(new_model, path+"/converted/"+x[:22]+"pr_"+x[22:])

path = "../models"
if len(sys.argv) > 1:
    for mdl in sys.argv[1:]:
        convert(mdl)
else:
    for x in os.listdir(path):
        if x.endswith(".h5"):
            model = load_model(path+"/"+x)
            model_cfg = model.get_config()
            if(x.startswith("ffnn_best_h") or x.startswith("lstm_best_h")):
                convert(x)
