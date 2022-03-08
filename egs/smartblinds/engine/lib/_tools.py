from yaml import full_load as yaml_full_load, dump as yaml_dump
import numpy as np

def load_config(cfg_file):
    with open(cfg_file, 'r') as fr:
        cfg = yaml_full_load(fr)

    return cfg


def load_task(cfg):
    with open(cfg['classification']['task_file'], 'r') as fr:
        task = yaml_full_load(fr)

    return task


def dump_task(cfg, task):
    with open(cfg['classification']['task_file'], 'w') as fw:
        yaml_dump(task, fw, default_flow_style=False)


def format_secs(s):
    if s < 1e-6:
        return str(round(s*1e6, 4))+' ns'
    elif s < 1e-3:
        return str(round(s*1e3, 4))+' ms'
    elif s > 60:
        return str(round(s/60, 4))+' min'
    else:
        return str(round(s, 4))+' s'

def trim(val, minimum=0, maximum=100):
    return min(maximum, max(minimum, val))

def make_vector(data, taskInfo):
    return [norm(data[name], *info) for name, info in taskInfo.items()]

def make_matrix(data, key, taskInfo):
    return np.array([make_vector(obs[key], taskInfo) for obs in data])

def norm(value, a_type, a_min, a_max):
    if a_type == 'boolean':
        return int(value)
    else:
        return (value-a_min)/(a_max-a_min)