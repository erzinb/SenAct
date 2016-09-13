#!/usr/bin/env python
import mysql.connector
import datetime
import time
#import RPi.GPIO as GPIO
from subprocess import Popen, PIPE
import requests
import os

if os.path.exists('/var/www/SenAct/senactlicence.log'):
    os.rename('/var/www/SenAct/senactlicence.log','/var/www/SenAct/senactlicence.log.old')
 
f = open('/var/www/SenAct/senactlicence.log','w')

cmd = "ifconfig eth0 | grep HWaddr"
p = Popen(cmd , shell=True, stdout=PIPE, stderr=PIPE)
out, err = p.communicate()
f.write(datetime.datetime.now().isoformat(' ')+" | ");
f.write("Return code: %d | " % p.returncode)
f.write("Error: %s | " % err.rstrip())
mac = out.rstrip()[-17:]
f.write("MAC: %s | " % mac)
payload = {'data': mac}
r = requests.post('http://boris:bs@www.erzin.si/SenAct/licencecheck.php?data=', payload)
f.write("Status code: %d | %s" % (r.status_code, r.text))
f.flush()

print bool(int(r.text))

try:
    cnx = mysql.connector.connect(user='boris', password='tejkica00', host='127.0.0.1', database='senact')
    cursor = cnx.cursor()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        f.write("Something is wrong with your user name or password\n")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        f.write("Database does not exist\n")
    else:
        f.write(err+'\n')
else:
    cursor.close()
    cnx.close()

f.close()
