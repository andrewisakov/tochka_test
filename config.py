import os
import sys
import yaml

SERVICE_ROOT_DIR = os.path.dirname(__file__)
sys.path.append(SERVICE_ROOT_DIR)

CONFIG = yaml.safe_load(open(os.path.join(SERVICE_ROOT_DIR, 'config.yaml')))
DSN = CONFIG.get('dsn', {})
host = DSN.get('host', 'localhost')
port = DSN.get('port', 5432)
database = DSN.get('database')
user = DSN.get('user', 'postgres')
password = DSN.get('password', 'postgres')
BIND = f'postgresql://{user}:{password}@{host}:{port}/{database}'
REFRESH_HOLDS_SLEEP = CONFIG.get('api', {}).get('refresh_holds', 600)
HOST = CONFIG.get('api', {}).get('host', '0.0.0.0')
PORT = CONFIG.get('api', {}).get('port', '8080')
