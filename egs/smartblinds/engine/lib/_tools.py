from yaml import full_load as yaml_full_load


def load_config(cfg_file):
    with open(cfg_file, 'r') as fr:
        cfg = yaml_full_load(fr)

    return cfg


def load_task(cfg):
    with open(cfg['classification']['task_file'], 'r') as fr:
        task = yaml_full_load(fr)

    return task