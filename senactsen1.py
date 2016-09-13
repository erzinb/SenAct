import mysql.connector
import datetime
import time
import RPi.GPIO as GPIO
import os
from w1thermsensor import W1ThermSensor
from w1thermsensor import UnsupportedUnitError
from w1thermsensor import NoSensorFoundError
from w1thermsensor import SensorNotReadyError

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
#    GPIO.setup(channel, GPIO.OUT, pull_up_down = GPIO.PUD_OFF)
#    GPIO.output(channel,0)
#    time.sleep(0.5)
#    GPIO.setup(channel, GPIO.IN, pull_up_down = GPIO.PUD_OFF)
#    if channel == 9:
#        t9=datetime.datetime.now()
#    else:
#        t11=datetime.datetime.now()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

channels = [2,3,4,17,27,22,10,9,11,7,8,25,24,23,18,15,14]
GPIO.setup(channels, GPIO.OUT, pull_up_down = GPIO.PUD_OFF, initial = GPIO.LOW)

k={'1':0.255,'2':0.255}
n={'1':-58.0,'2':-58.0}
T={}


#GPIO13
GPIO.setup(9, GPIO.OUT, pull_up_down = GPIO.PUD_OFF)
GPIO.output(9,0)
time.sleep(0.5)
#GPIO.add_event_detect(9, GPIO.RISING, callback=gpio_callback, bouncetime=1)


#GPIO14
GPIO.setup(11, GPIO.OUT, pull_up_down = GPIO.PUD_OFF)
GPIO.output(11,0)
time.sleep(0.5)
#GPIO.add_event_detect(11, GPIO.RISING, callback=gpio_callback, bouncetime=1)

if os.path.exists('/var/www/SenAct/senactsen.log'):
    os.rename('/var/www/SenAct/senactsen.log','/var/www/SenAct/senactsen.log.old')
 
f = open('senactsen.log','w')

while 1:
# ---------------------------------RC section --------------------------------------------------------
    tt=datetime.datetime.now()
    try:
        cnx = mysql.connector.connect(user='boris', password='tejkica00',
                              host='127.0.0.1',
                              database='senact')
        cursor = cnx.cursor(buffered=True)
        cursor1 = cnx.cursor(buffered=True)
    except KeyboardInterrupt:
        break
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            f.write("MySQL: Something is wrong with your user name or password\n")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            f.write("MySQL: Database does not exist\n")
        else:
            f.write(err)
        f.flush()
    else:
        query = ("select sensorId,T,k,n from sensors where type='RC'")
        cursor.execute(query)
        sensorsDB=[]
        for (sensorId,T1,k1,n1) in cursor:
            sensorDB={}
            sensorDB["sensorId"]=sensorId
            sensorDB["T"]=T1
            sensorDB["k"]=k1
            sensorDB["n"]=n1
            sensorsDB.append(sensorDB)
#        print cursor.rowcount
        if cursor.rowcount == 0:
            t=dateime.datetime.now().isoformat()
            insert = ("insert into sensors (sensorId,name,k,n,T,TL,TH,type,last_change) VALUES('1','T1',0.255,-58,20,20,20,'RC','"+t+"')")
            cursor1.execute(insert)
            insert = ("insert into sensors (sensorId,name,k,n,T,TL,TH,type,last_change) VALUES('2','T2',0.255,-58,20,20,20,'RC','"+t+"')")
            cursor1.execute(insert)
            cnx.commit()
            
        for sensorDB in sensorsDB:
            k[sensorDB["sensorId"]]=sensorDB["k"]
            n[sensorDB["sensorId"]]=sensorDB["n"]
            T[sensorDB["sensorId"]]=sensorDB["T"]

        GPIO.setup(9, GPIO.IN, pull_up_down = GPIO.PUD_OFF)
        t9=datetime.datetime.now()
        GPIO.add_event_detect(9, GPIO.RISING, callback=gpio_callback, bouncetime=200)
#        i = 0
#        while GPIO.input(9) == 0:
#            i+=1
#            delta=datetime.datetime.now()-t9
#            if delta.microseconds > 900000:
#                break
        T['1']=170.0
        time.sleep(0.5)
#        print (datetime.datetime.now()-t9).microseconds
#        T['1']=int(round(delta.microseconds/1000*k['1']+n['1'],2)*2.0)/2.0
#        print("T1={}".format(T['1']))
        GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_OFF)
        t11=datetime.datetime.now()
        GPIO.add_event_detect(11, GPIO.RISING, callback=gpio_callback, bouncetime=200)
#        i = 0
#        while GPIO.input(11) == 0:
#            i+=1
#            delta=datetime.datetime.now()-t11
#            if delta.microseconds > 900000:
#                break
        T['2']=170.0
        time.sleep(0.5)
#        print (datetime.datetime.now()-t11).microseconds
#        T['2']=int(round(delta.microseconds/1000*k['2']+n['2'],2)*2.0)/2.0
#        print("T2={}".format(T['2']))
        for id in T:
            if id=='1':
                t=t9.isoformat()
            elif id=='2':
                t=t11.isoformat()
            else:
                t=dateime.datetime.now().isoformat()
            if T[id]>130:
                update = ("update sensors set T=null,last_change='"+t+"' where sensorId="+id)
            else:
                update = ("update sensors set T="+str(T[id])+",last_change='"+t+"' where sensorId="+id)
            result=cursor1.execute(update)
            insert = ("insert into sensors_history (T,sensorId,sampleTime) VALUES("+str(T[id])+",'"+id+"','"+t+"')")
            result=cursor1.execute(insert)
        GPIO.remove_event_detect(9)
        GPIO.setup(9, GPIO.OUT, pull_up_down = GPIO.PUD_OFF)
        GPIO.output(9,0)
        GPIO.remove_event_detect(11)
        GPIO.setup(11, GPIO.OUT, pull_up_down = GPIO.PUD_OFF)
        GPIO.output(11,0)
# ---------------------------------- RC section END ----------------------------------------------

# ---------------------------------- DS18x20 section ---------------------------------------------
        query = ("select sensorId,name,type,TL,TH from sensors where type!='RC'")
        result=cursor.execute(query)
        sensorsDB=[]
        for (sensorId,name,type,TL,TH) in cursor:
            sensorDB={}
            sensorDB["sensorId"]=sensorId
            sensorDB["name"]=name
            sensorDB["type"]=type
            sensorDB["TL"]=TL
            sensorDB["TH"]=TH
            sensorsDB.append(sensorDB)
   
        ids="0"
        try:
            sensors = W1ThermSensor.get_available_sensors()
            for sensor in sensors:
                found = False
                ids = sensor.id
                temperature = sensor.get_temperature()
                t=datetime.datetime.now().isoformat()
                for sensorDB in sensorsDB:
#                for (sensorId,name,type,TL,TH) in cursor:
                    if sensor.id == sensorDB["sensorId"]:
                        found = True
                        update = ("update sensors set T="+str(temperature)+",last_change='"+t+"' where sensorId='"+sensorDB["sensorId"]+"'")
                        result=cursor1.execute(update)
                        break
                if not found:
                    insert = ("insert into sensors (T,sensorId,name,type,TL,TH,last_change) VALUES("+str(temperature)+",'"+sensor.id+"','TX','"+sensor.type_name+"',0,0"+",'"+t+"')")
                    result=cursor1.execute(insert)
                insert = ("insert into sensors_history (T,sensorId,sampleTime) VALUES("+str(temperature)+",'"+sensor.id+"','"+t+"')")
                result=cursor1.execute(insert)
            for sensorDB in sensorsDB:
                ids=sensorDB["sensorId"]
                found = False
                for sensor in sensors:
                    if sensor.id == sensorDB["sensorId"]:
                        found = True
                        break
                if not found:
                    update = ("update sensors set T=null where sensorId='"+sensorDB["sensorId"]+"'")
                    result=cursor1.execute(update)
        except UnsupportedUnitError:
            f.write("UnsupportedUnitError\n")
            f.flush()
        except NoSensorFoundError:
            update = ("update sensors set T=null where sensorId="+ids)
            result=cursor1.execute(update)
            f.write("NoSensorFoundError\n")
            f.flush()
        except SensorNotReadyError:
            update = ("update sensors set T=null where sensorId="+ids)
            result=cursor1.execute(update)
            f.write("SensorNotReadyError\n")
            f.flush()
# ------------------------------------ DS18x20 section END -------------------------------------------

        cnx.commit()
        
        cursor.close()
        cursor1.close()
        cnx.close()
        delta=datetime.datetime.now()-tt-datetime.timedelta(seconds=5)+datetime.timedelta(microseconds=4100)
#        print -delta.total_seconds()
        if delta.total_seconds()<0:
            time.sleep(-delta.total_seconds())
#        print datetime.datetime.now()-tt
f.close()        
GPIO.cleanup()
GPIO.setup(channels, GPIO.OUT, pull_up_down = GPIO.PUD_OFF, initial = GPIO.LOW)
