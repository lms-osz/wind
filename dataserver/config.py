import os
import ConfigParser

CONFIG_PATH = "config.cfg"

# if config does not exits
if os.path.isfile(CONFIG_PATH) == False:
    print ("\'" + CONFIG_PATH + "\' is missing, it will be created with the default content!")
    file = open(CONFIG_PATH, "w")
    file.write("""[server]\nurl=ws://127.0.0.1/datasocket\n\n[settings]\ndelay=1000\ntimes=4\n\npassword=foobar\n\n[channels]\nwind=\nUbatt=\nIbatt=""")
    file.close()
    print ("Please check the config in '" + CONFIG_PATH + "'")
    exit()


configParser = ConfigParser.RawConfigParser()
configParser.read(CONFIG_PATH)

url = configParser.get("server", "url")
password = configParser.get("settings", "password")
delay = (float(configParser.get("settings", "delay")) / 1000)
times = int(configParser.get("settings", "times"))

windChannel = int(configParser.get("channels", "wind"))
UbattChannel = int(configParser.get("channels", "Ubatt"))
IbattChannel = int(configParser.get("channels", "Ibatt"))
