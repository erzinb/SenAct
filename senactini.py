import mysql.connector
import datetime
import time
import RPi.GPIO as GPIO
import os

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

channels = [2,3,4,17,27,22,10,9,11,29,31,30,28,7,8,25,24,23,18,15,14]
gpio = [8,9,7,0,2,3,12,13,14,18,20,19,17,11,10,6,5,4,1,16,15]
GPIO.setup(channels, GPIO.OUT, pull_up_down = GPIO.PUD_OFF)
GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_OFF)

gpiotochannel = {}
for index in range(len(gpio)):
    gpiotochannel[gpio[index]]=channels[index]

if os.path.exists('/var/www/SenAct/senactini.log'):
    os.rename('/var/www/SenAct/senactini.log','/var/www/SenAct/senactini.log.old')
 
f = open('/var/www/SenAct/senactini.log','w')

try:
    cnx = mysql.connector.connect(user='boris', password='tejkica00', host='127.0.0.1', database='senact')
    cursor = cnx.cursor()
except KeyboardInterrupt:
    f.write('Keybord interrupted connection!\n')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        f.write("Something is wrong with your user name or password\n")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        f.write("Database does not exist\n")
    else:
        f.write(err+'\n')
else:
    query = ("select gpio, state from activators")
    cursor.execute(query)
    for (gpio, state) in cursor:
        GPIO.output(gpiotochannel[gpio], state)
    cursor.close()
    cnx.close()
f.close()
