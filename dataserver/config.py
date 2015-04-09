import os
import ConfigParser

CONFIG_PATH = "config.cfg"

# if config does not exits
if os.path.isfile(CONFIG_PATH) == False:
    print ("Because no config file exits, a config file will be created")
    file = open(CONFIG_PATH, "w")
    file.write("""[server]\nurl=ws://127.0.0.1/datasocket\n\n[settings]\ndelay=1\npassword=foobar\n""")
    file.close()
    print ("Please check the config in '" + CONFIG_PATH + "'")


configParser = ConfigParser.RawConfigParser()
configParser.read(CONFIG_PATH)

url = configParser.get("server", "url")
password = configParser.get("settings", "password")
delay = configParser.get("settings", "delay")
