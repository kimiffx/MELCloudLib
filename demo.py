# coding=utf-8
from optparse import OptionParser
from melcloudlib import mcloud
import pprint

if __name__ == '__main__':
    parser = OptionParser('usage: %prog [options]')

    parser.add_option("-u", "--username", type="string", dest="username", help="MelCloud username")
    parser.add_option("-p", "--password", type="string", dest="password", help="MelCloud password")
    parser.add_option("-d", "--debug", action="store_true", dest="debug", help="Enable debug mode")

    (options, args) = parser.parse_args()

    required="username password".split()

    for r in required:
        if options.__dict__[r] is None:
            parser.error("parameter %s required"%r)

    mc = mcloud(debug=options.debug)
    mc.login(options.username, options.password)

    paramNames = ['FanSpeed','RoomTemperature','SetTemperature']
    output = mc.getDeviceParams(paramNames)

    # Debug printout
    pp = pprint.PrettyPrinter()
    pp.pprint(output)

    print("RoomTemperature is " + str(output['RoomTemperature']))
