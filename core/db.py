from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from configparser import ConfigParser

file = 'settings.ini'
config = ConfigParser()
config.read(file)

def get_engine(user,passw,db,port,host):
    url = f'postgresql+psycopg2://{user}:{passw}@{host}:{port}/{db}'
    if not database_exists(url):
        create_database
    engine = create_engine(url)  
    return engine

def get_connection():
    return get_engine(config['database']['user'],
                        config['database']['passw'],
                        config['database']['db'],
                        config['database']['port'],
                        config['database']['host'])
