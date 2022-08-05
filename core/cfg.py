from configparser import ConfigParser

file = 'settings.ini'

config = ConfigParser()
config.read(file)

TOKEN = config['config']['token']
