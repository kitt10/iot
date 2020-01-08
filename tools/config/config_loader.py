from sys import version as py_version
from argparse import ArgumentParser
from config import Config

def parse_arguments():  
    parser = ArgumentParser(description='mqtt2ws')
    parser.add_argument('-c', '--cfg_path', type=str, default='config.cfg',
                        help='Path to the config file.')

    return parser.parse_args()

def load_config():
    args = parse_arguments()
    print('\n\n')
    print(py_version)
    print('Config file:', args.cfg_path)
    print('------------------------------------------------')
    with open(args.cfg_path, 'r') as f:
        return Config(f)

if __name__ == '__main__':
    
    # Print Python version, load project configuration
    cfg = load_config()

    # Use configuration (dot notation)
    print(cfg)
    print('MQTT host:', cfg.mqtt.host)
    print('Tornado webserver port:', cfg.tornado.port)
