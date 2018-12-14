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
            parsed = json.loads(response.text)
            print(json.dumps(parsed, indent=2, sort_keys=True))

        sessionKey = response.json()['LoginData']['ContextKey']

        self.session.headers['X-MitsContextKey'] = sessionKey

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

