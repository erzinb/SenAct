import mysql.connector
import datetime
import time
import RPi.GPIO as GPIO
import os

def gpio_callback(channel):
    global t9
    global t11
    global T
    now=datetime.datetime.now()
    if channel == 9:
        delta=now-t9
        name="T1"
        id='1'
    else:
        delta=now-t11
        name="T2"
        id='2'
    K=k[id]
    N=n[id]
    T[id]=int(round(delta.microseconds/1000*K+N,2)*2.0)/2.0
#    print("gpio %s %s" % (channel, T[id]))
    GPIO.setup(channel, GPIO.OUT, pull_up_down = GPIO.PUD_OFF)
    GPIO.output(channel,0)
    time.sleep(0.5)
    GPIO.setup(channel, GPIO.IN, pull_up_down = GPIO.PUD_OFF)
    if channel == 9:
        t9=datetime.datetime.now()
    else:
        t11=datetime.datetime.now()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

channels = [2,3,4,17,27,22,10,9,11,7,8,25,24,23,18,15,14]
modes = [GPIO.OUT,GPIO.OUT,GPIO.OUT,GPIO.OUT,GPIO.OUT,GPIO.OUT,GPIO.OUT,GPIO.OUT,GPIO.OUT,GPIO.OUT,GPIO.OUT,GPIO.OUT,GPIO.OUT,GPIO.OUT,GPIO.OUT,GPIO.OUT,GPIO.OUT]
pulls = [GPIO.PUD_OFF,GPIO.PUD_OFF,GPIO.PUD_OFF,GPIO.PUD_OFF,GPIO.PUD_OFF,GPIO.PUD_OFF,GPIO.PUD_OFF,GPIO.PUD_OFF,GPIO.PUD_OFF,GPIO.PUD_OFF,GPIO.PUD_OFF,GPIO.PUD_OFF,GPIO.PUD_OFF,GPIO.PUD_OFF,GPIO.PUD_OFF,GPIO.PUD_OFF,GPIO.PUD_OFF]
values = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
GPIO.setup(channels, GPIO.OUT, pull_up_down = GPIO.PUD_OFF, initial = GPIO.LOW)

k={'1':0.255,'2':0.255}
n={'1':-58.0,'2':-58.0}
T={}


#GPIO13
GPIO.setup(9, GPIO.OUT, pull_up_down = GPIO.PUD_OFF)
GPIO.output(9,0)
time.sleep(0.5)
#GPIO.setup(9, GPIO.IN, pull_up_down = GPIO.PUD_OFF)
#GPIO.add_event_detect(9, GPIO.RISING, callback=gpio_callback, bouncetime=1)
t9=datetime.datetime.now()


#GPIO14
GPIO.setup(11, GPIO.OUT, pull_up_down = GPIO.PUD_OFF)
GPIO.output(11,0)
time.sleep(0.5)
#GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_OFF)
#GPIO.add_event_detect(11, GPIO.RISING, callback=gpio_callback, bouncetime=1)
t11=datetime.datetime.now()

if os.path.exists('/var/www/SenAct/senactsen.log'):
    os.rename('/var/www/SenAct/senactsen.log','/var/www/SenAct/senactsen.log.old')
 
f = open('senactsen.log','w')

while 1:
    try:
        cnx = mysql.connector.connect(user='boris', password='tejkica00',
                              host='127.0.0.1',
                              database='senact')
        cursor = cnx.cursor()
    except KeyboardInterrupt:
        break
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            f.write("MySQL: Something is wrong with your user name or password\n")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            f.write("MySQL: Database does not exist\n")
        else:
            f.write(err)
    else:
        query = ("select id,sensorId,k,n from sensors where type='RC'")
        cursor.execute(query)
        for (id,sensorId,kk,nn) in cursor:
            k[sensorId]=kk
            n[sensorId]=nn
#            print("{},{},{}".format(name,k,n))
#        print(k)
#        print(n)

        GPIO.setup(9, GPIO.IN, pull_up_down = GPIO.PUD_OFF)
        t9=datetime.datetime.now()
        GPIO.wait_for_edge(9,GPIO.RISING)
        delta=datetime.datetime.now()-t9
#        GPIO.add_event_detect(9, GPIO.RISING, callback=gpio_callback, bouncetime=1)
#        i = 0
#        while GPIO.input(9) == 0:
#            i+=1
#            delta=datetime.datetime.now()-t9
#            if delta.microseconds > 900000:
#                break
#        time.sleep(0.5)
        T['1']=int(round(delta.microseconds/1000*k['1']+n['1'],2)*2.0)/2.0
#        print("T1={} i={}".format(T[1],i))
        GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_OFF)
        t11=datetime.datetime.now()
#        GPIO.add_event_detect(11, GPIO.RISING, callback=gpio_callback, bouncetime=1)
        i = 0
        while GPIO.input(11) == 0:
            i+=1
            delta=datetime.datetime.now()-t11
            if delta.microseconds > 900000:
                break
#        time.sleep(0.5)
        T['2']=int(round(delta.microseconds/1000*k['2']+n['2'],2)*2.0)/2.0
#        print("T2={} i={}".format(T[2],i))
        for id in T:
            if T[id]>130:
                query = ("delete from sensors where sensorId="+id)
            else:
                query = ("update sensors set T="+str(T[id])+" where sensorId="+id)
#            print query
            result=cursor.execute(query)
#            print result
        GPIO.setup(9, GPIO.OUT, pull_up_down = GPIO.PUD_OFF)
        GPIO.output(9,0)
        GPIO.setup(11, GPIO.OUT, pull_up_down = GPIO.PUD_OFF)
        GPIO.output(11,0)

        cnx.commit()
        
        cursor.close()
        cnx.close()
        time.sleep(3)
f.close()        
GPIO.cleanup()
GPIO.setup(channels, GPIO.OUT, pull_up_down = GPIO.PUD_OFF, initial = GPIO.LOW)
