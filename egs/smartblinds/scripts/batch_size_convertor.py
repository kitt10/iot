import os
from keras.models import load_model, save_model
import sys

path = "../models"
def convert(filename):
    x = filename
    model = load_model(x)
    model_cfg = model.get_config()
    if(x.startswith("ffnn")):
        for i in range(2):
            model_cfg['layers'][i]['config']['batch_input_shape'] = (1,15)
            new_model = model.__class__.from_config(model_cfg)
            new_model.set_weights(model.get_weights())
            save_model(new_model, path+"/converted/"+x[:-29]+"pr_"+x[-29:])
    if(x.startswith("lstm")):
        for i in range(2):
            model_cfg['layers'][i]['config']['batch_input_shape'] = (1,64,15)
            new_model = model.__class__.from_config(model_cfg)
            new_model.set_weights(model.get_weights())
            save_model(new_model, path+"/converted/"+x[:-29]+"pr_"+x[-29:])

if len(sys.argv) > 1:
    for mdl in sys.argv[1:]:
        convert(mdl)
else:
    for x in os.listdir(path):
        if x.endswith(".h5") and ((x.startswith("ffnn_best_h") or x.startswith("lstm_best_h"))):
            convert(path+"/"+x)
