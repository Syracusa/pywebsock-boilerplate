import configparser

appconf = None
if appconf == None:
    appconf = configparser.ConfigParser()
    appconf.read('app.config')
    for k in appconf['DEFAULT']:
        print('' + k + ' ' + appconf['DEFAULT'][k])