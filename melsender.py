# coding=utf-8
from optparse import OptionParser
from melcloudlib import mcloud
import pprint

from influxdb import InfluxDBClient
import datetime

import my_config as conf

# This application pulls data from MELcloud and sends to InfluxDB database
# Configure credentials and InfluxDB host information in my_config.py

if __name__ == '__main__':
    parser = OptionParser('usage: %prog [options]')

    parser.add_option("-d", "--debug", action="store_true", dest="debug", help="Enable debug mode")

    (options, args) = parser.parse_args()

    client = InfluxDBClient(conf.INFLUXDB_HOST, conf.INFLUXDB_PORT, conf.INFLUXDB_USER, conf.INFLUXDB_PWD, conf.INFLUXDB_DATABASE, timeout=5)

    mc = mcloud(debug=options.debug)
    mc.login(conf.MELCLOUD_USER, conf.MELCLOUD_PWD)

    # In addition to the listed parameters, melcloudlib always returns DeviceName
    paramNames = ['FanSpeed','RoomTemperature','SetTemperature','ActualFanSpeed','CurrentEnergyConsumed','OperationMode']
    allDevices = mc.getAllDevices(paramNames)

    timestamp = datetime.datetime.utcnow()
    str_timestamp = timestamp.isoformat("T") + "Z"

    for device in allDevices:
        json_temp = [
            {
                "measurement": "mcloud",
                "tags": {
                    "DeviceName": device['DeviceName']
                },
                "time": str_timestamp,
                "fields": {
                    "RoomTemperature":       device['RoomTemperature'],
                    "SetTemperature":        device['SetTemperature'],
                    "FanSpeed":              device['FanSpeed'],
                    "ActualFanSpeed":        device['ActualFanSpeed'],
                    "CurrentEnergyConsumed": device['CurrentEnergyConsumed'],
                    "OperationMode":         device['OperationMode']
                }
            }
        ]

        client.write_points(json_temp)
