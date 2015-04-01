import os
import time

LOG_DIR = "logs/"

now = time.localtime()

if not os.path.isdir(LOG_DIR):
    os.mkdir(LOG_DIR)

tmplogfile_path = LOG_DIR + str(now.tm_year) + "-" +  str(now.tm_mon) + "-" + str(now.tm_mday);

i = 0
if os.path.isfile(tmplogfile_path + ".log"):
    i = i + 1
    while True:
        if os.path.isfile(tmplogfile_path + "-" + str(i) + ".log") == False:
            break
        i = i + 1
if i != 0:
    LOGFILE_PATH = tmplogfile_path + "-" + str(i) + ".log"
else:
    LOGFILE_PATH = tmplogfile_path + ".log"

print "logfile is located at \"" + LOGFILE_PATH + "\""


def info(text):
    print "[INFO]    " + text;
    logfile = open(LOGFILE_PATH, "a")
    logfile.write("[INFO]    " + text + "\n")
    logfile.close()

def error(text):
    print "[ERROR]   " + text;
    logfile = open(LOGFILE_PATH, "a")
    logfile.write("[ERROR]   " + text + "\n")
    logfile.close()

info("starting server...")