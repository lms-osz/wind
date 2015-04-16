import os
import ConfigParser

CONFIG_PATH = "config.cfg"

config_error = False
# if config does not exits
if os.path.isfile(CONFIG_PATH) == False:
    print ("config file does not exists! will be created")
    file = open(CONFIG_PATH, "w")
    file.write("""[server]\nport=80\n\n[ssl]\nssl=false\ncrt=\nkey=\n\n[settings]\npassword=foobar\n[database]\nfile=wind_data.db""")
    file.close()
    print ("Please check the config in '" + CONFIG_PATH + "'")


configParser = ConfigParser.RawConfigParser()
configParser.read(CONFIG_PATH)
try:
   port = configParser.get("server", "port")
   password = configParser.get("settings", "password")
   db_file = configParser.get("database", "file")
except:
    config_error = True
try:
    if configParser.get("ssl","ssl") == "true":
        ssl = True
    elif configParser.get("ssl","ssl") == "false":
        ssl = False
    else:
        print ("error at " + CONFIG_PATH + " error in ssl=" + configParser.get("ssl","ssl") + " only true or false!")
        ssl_options = {
            "certfile": configParser.get("ssl","crt"),
            "keyfile": configParser.get("ssl","key")
        }
except:
    ssl = False
