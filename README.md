# TS3_Weather_Bot
This script can be used to update a Teamspeak 3 server's channel names with weather data. <br>
Depends on Murgyeye's [teamspeak3-python-api](https://github.com/Murgeye/teamspeak3-python-api). <br>
Uses the [openweathermap-api](https://openweathermap.org/current) <br>
Run as a cron job for automatic updates every x sec/min/hr.

![alt text](https://raw.githubusercontent.com/JannikRosendahl/assets/master/TS3_Weather_Bot_Screenshot.PNG?token=AJENESPL5RK6DGWWB2QHDYC7KERKG)

To mark a channel on your server as a 'weather'-channel, it has to be a sub-channel of a channel containing the [TEAMSPEAK][weather_channel_parent_identifier]
specified in your config.ini. <br>
A weather channel's name has be a location.

**config.ini:** <br>
`api_key`: you must provide a valid api key, get a free one [here](https://openweathermap.org/price)<br>
`server_address`: ip/domain of your teamspeak server<br>
`server_query_port`: server query port, default is 10011, 10022 with ssh<br>
`default_bot_channel`: channel name the bot will join, set to 'none' if the bot should not move<br>

`server_query_username`: server query username<br>
`server_query_password`: server query password<br>
`server_virtual_id`: virtual server id, default is 1<br>

`bot_name`: name of the bot<br>

`weather_channel_parent_identifier`: identifier for the parent weather channel<br>
