# coding=utf-8
from requests import Session
from optparse import OptionParser
import json, pprint

class mcloud():
    session    = Session()
    sessionKey = None
    debugMode  = False

    URL_LOGIN        = "https://app.melcloud.com/Mitsubishi.Wifi.Client/Login/ClientLogin"
    URL_LIST_DEVICES = "https://app.melcloud.com/Mitsubishi.Wifi.Client/User/ListDevices"

    def __init__(self, debug=False):
        self.debugMode = debug

    def login(self, email, password):

        response = self.session.post(
            self.URL_LOGIN, data={
                "AppVersion": "1.9.3.0",
                "CaptchaChallenge": "",
                "CaptchaResponse": "",
                "Email": email,
                "Password": password,
                "Language": 0,  # 0=English
                "Persist": "true"
            }
        )

        if self.debugMode:
            print("Login response:\n")
            print(response.text + "\n")

        sessionKey = response.json()['LoginData']['ContextKey']

        self.session.headers['X-MitsContextKey'] = sessionKey

# MELCloud API outputs:
# In the top level there is a list of buildings
# Under each building there is Structure.Devices list
# Actual device parameters are in key 'Device' under Devices list item

# Get all devices of this account
    def getAllDevices(self, paramlist):
        response = self.session.get(self.URL_LIST_DEVICES)

        if self.debugMode:
            print("Device query response:\n")
            print(response.text + "\n")

        data = response.json()
        outDevices = []

        for building in data:
            for device in building['Structure']['Devices']:
                devicedata={}
                # Always return DeviceName
                devicedata['DeviceName'] = device['DeviceName']

                for param in paramlist:
                    devicedata[param] = device['Device'][param]

                outDevices.append(devicedata)

        return outDevices


# Get data of a single device identified by the index in array returned by MELCloud API.
# paramlist shall be list of strings referring to parameter names
    def getDeviceParams(self, paramlist, devindex=0):
        response = self.session.get(self.URL_LIST_DEVICES)

        if self.debugMode:
            parsed = json.loads(response.text)
            print(json.dumps(parsed, indent=2, sort_keys=True))

        data = response.json()
        devicelist = data[devindex]['Structure']['Devices']

        output = {}

        for param in paramlist:
            output[param] = devicelist[devindex]['Device'][param]

        return output

