import configparser as configparser


API_KEY = None

server_address = None
server_port = None
server_query_port = None
default_bot_channel = None
server_query_username = None
server_query_password = None


def read_config():
    global API_KEY

    global server_address
    global server_port
    global server_query_port
    global default_bot_channel
    global server_query_username
    global server_query_password

    config = configparser.ConfigParser()
    config.read('config.ini')

    API_KEY = config['OPENWEATHERMAP'].get('api_key')

    server_address = config['TEAMSPEAK'].get('server_address')
    server_port = config['TEAMSPEAK'].get('server_port')
    server_query_port = config['TEAMSPEAK'].get('server_query_port')
    default_bot_channel = config['TEAMSPEAK'].get('default_bot_channel')
    server_query_username = config['TEAMSPEAK'].get('server_query_username')
    server_query_password = config['TEAMSPEAK'].get('server_query_password')



