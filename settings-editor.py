from settings import Settings



settings = Settings('wifi.dat')

conf = {}

print('Enter your wifi network ssid')
conf["ssid"] = input()
print('Enter wifi passphrase')
conf["pass"] = input ()

settings.save_settings(conf)

print('Settings saved')
print(settings.get_settings())