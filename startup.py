#Imports the os library to find the running processes
import os
#imports subprocess library so I can run .sh
import subprocess
from botcore.config import screenName

#Scans for all running processes for that user
pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]


botRun = False
for pid in pids: #Goes through all the processes running for that user
    try:
		temp = open(os.path.join('/proc', pid, 'cmdline'), 'r').read().lower()
		if temp.find("%s" % screenName) != -1 and temp.find("screen") != -1:
			botRun = True
    except:
        continue

if not botRun:
	"""
	This can cause security errors but from what I understand
	it is only when it allows the users to enter their own input.
	Since this is only running from something that isn't visible on the webserver
	it shouldn't be an issue. If it please feel free to contact me anywhere to tell me so.
	"""
	subprocess.call("sh startBot.sh %s" % screenName, shell=True)