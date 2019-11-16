# coding=utf-8
from optparse import OptionParser
from melcloudlib import mcloud
import pprint

from influxdb import InfluxDBClient
import datetime

import mel_config as conf

# This application pulls data from MELcloud and sends to InfluxDB database
# Configure credentials and InfluxDB host information in mel_config.py

if __name__ == '__main__':
    parser = OptionParser('usage: %prog [options]')

    parser.add_option("-d", "--debug", action="store_true", dest="debug", help="Enable debug mode")

    (options, args) = parser.parse_args()

    mc = mcloud(debug=options.debug)
    mc.login(conf.MELCLOUD_USER, conf.MELCLOUD_PWD)

    paramNames = ['FanSpeed','RoomTemperature','SetTemperature']
    output = mc.getDeviceParams(paramNames)

    timestamp = datetime.datetime.utcnow()
    str_timestamp = timestamp.isoformat("T") + "Z"

    json_temp = [
        {
            "measurement": "mcloud",
            "time": str_timestamp,
            "fields": {
               "RoomTemperature": output['RoomTemperature'],
               "SetTemperature": output['SetTemperature'],
               "FanSpeed": output['FanSpeed']
            }
        }
    ]

    client = InfluxDBClient(conf.INFLUXDB_HOST, conf.INFLUXDB_PORT, conf.INFLUXDB_USER, conf.INFLUXDB_PWD, conf.INFLUXDB_DATABASE, timeout=5)

    client.write_points(json_temp)
