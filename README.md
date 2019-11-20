# MELCloudLib
Library to interact with Mitsubishi Electric MELCloud.

Currently supports only reading device parameters, see demo.py for example.
Works with both python2.7 and python3.

``python3 demo.py -u user@demo.com -p mypassword``

Add switch -d to enable debug mode. Then you will see all the parameters that API returns and know what can be queried from your device, or know how to modify the code to work in your environment.
