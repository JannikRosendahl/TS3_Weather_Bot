import os
import configparser as configparser
import random
from datetime import datetime

from Weather import request_weather
from ts3API.TS3Connection import TS3Connection


API_KEY = None

server_address = None
server_query_port = None
default_bot_channel = None
server_query_username = None
server_query_password = None
server_virtual_id = None
bot_name = None
weather_channel_parent_identifier = None

ts3connection = None


def read_config():
    global API_KEY

    global server_address
    global server_query_port
    global default_bot_channel
    global server_query_username
    global server_query_password
    global server_virtual_id
    global bot_name
    global weather_channel_parent_identifier

    config = configparser.ConfigParser()
    script_directory = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(script_directory, 'config.ini')
    # config.read('config.ini')
    config.read(config_path)

    API_KEY = config['OPENWEATHERMAP'].get('api_key')

    server_address = config['TEAMSPEAK'].get('server_address')
    server_query_port = config['TEAMSPEAK'].get('server_query_port')
    default_bot_channel = config['TEAMSPEAK'].get('default_bot_channel')
    server_query_username = config['TEAMSPEAK'].get('server_query_username')
    server_query_password = config['TEAMSPEAK'].get('server_query_password')
    server_virtual_id = config['TEAMSPEAK'].get('server_virtual_id')
    bot_name = config['TEAMSPEAK'].get('bot_name')
    weather_channel_parent_identifier = config['TEAMSPEAK'].get('weather_channel_parent_identifier')


def connect_to_teamspeak():
    global ts3connection
    # connect to server, login and select virtual server
    ts3connection = TS3Connection(server_address, server_query_port)
    ts3connection.login(server_query_username, server_query_password)
    ts3connection.use(sid=server_virtual_id)

    # give the bot a name
    nick_name = bot_name + '_' + str(random.randint(0, 9999))
    ts3connection.clientupdate(["client_nickname=" + nick_name])

    # join the channel designated for bots
    if default_bot_channel is not None and not 'none':
        channel = ts3connection.channelfind(pattern=default_bot_channel)[0]["cid"]
        ts3connection.clientmove(channel, int(ts3connection.whoami()["client_id"]))


def update_weather_channels():
    channel_list = ts3connection.channellist()
    weather_parent_channel_ids = []
    successful_updates = 0

    for channel in channel_list:
        channel_name = channel['channel_name']
        channel_id = int(channel['cid'])
        channel_pid = int(channel['pid'])

        # check if we are a weather channel parent, if so, add our id to weather_parent_channel_ids
        if channel_name.lower().find(weather_channel_parent_identifier.lower()) != -1:
            weather_parent_channel_ids.append(channel_id)

        # check if we are a weather channel
        if weather_parent_channel_ids.count(channel_pid) > 0:
            # request weather data
            city_name = channel_name.split(' ')[0]
            weather = request_weather(API_KEY, city_name)

            # build new channel name, truncate string to len=40 (teamspeak hardcoded max channel length)
            new_channel_name = f'{city_name} {weather.weather}, {weather.temp}°C, {weather.wind_speed}km/h'
            new_channel_name = new_channel_name[:40]

            # check if we have to update channel name
            if new_channel_name != channel_name:
                try:
                    ts3connection.channeledit(cid=channel_id, channel_name=new_channel_name)
                    print(f'updated channel {channel_id} for city {city_name}')
                    print(f'\told channel name: {channel_name}')
                    print(f'\tnew channel name: {new_channel_name}')
                    successful_updates += 1
                except:
                    print(f'error updating channel {channel_id} for city {city_name}')
            else:
                print(f'did not update channel {channel_id} for city {city_name}, data has not changed')

    # if we updated channels update parent channels with date/time
    if successful_updates > 0:
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M")
        for channel_id in weather_parent_channel_ids:
            new_channel_name = '[cspacer]' + weather_channel_parent_identifier + '  ' + dt_string
            try:
                ts3connection.channeledit(cid=channel_id, channel_name=new_channel_name)
            except:
                print('error updating weather channel parent name')


read_config()
connect_to_teamspeak()
update_weather_channels()
ts3connection.quit()