import paho.mqtt.client as mqtt
import mysql.connector
import datetime
import time
import RPi.GPIO as GPIO
import os
from w1thermsensor import W1ThermSensor
from w1thermsensor import UnsupportedUnitError
from w1thermsensor import NoSensorFoundError
from w1thermsensor import SensorNotReadyError
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import smtplib
import socket


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    global f
    f.write("Connected with result code "+str(rc)+"\n")
    f.flush()
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
#    client.subscribe("$SYS/#")
    client.subscribe("berzinkl/senact/cmd/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global f
    global cnx
    try:
        cnx = get_mysql_connection()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            f.write("%s: MySQL: Something is wrong with your user name or password\n" % (datetime.datetime.now()))
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            f.write("%s: MySQL: Database does not exist\n" % (datetime.datetime.now()))
        else:
            f.write(err)
        f.flush()
    else:    
        cursor = cnx.cursor()
        cmd = msg.payload
        f.write("%s: %s %s\n" % (datetime.datetime.now(), msg.topic, cmd))
        i = 0
        topic = "berzinkl/senact/"+socket.getfqdn()
        if cmd == "getPrograms":
            topic += "/program";
            query = ("select distinct c.id as PROGID, a.name as ACTIVATOR, a.id as ID, a.state as STATE, case when c.sensorId = 'null' then null else b.name end as SENSOR, case when c.sensorId = 'null' then null else b.T end as T, case when c.TON = 'null' then null else c.TON end as TON, case when c.TOFF = 'null' then null else c.TOFF end as TOFF, c.start_time as START, c.stop_time as STOP, c.month as MESEC, c.week as TEDEN, c.day as DAN, c.dayinweek as DANTEDNA from programs c,activators a, sensors b where c.start_time<TIME(NOW()) and c.stop_time>=TIME(NOW()) and (c.month is null or c.month=MONTH(NOW())) and (c.week is null or c.week=WEEKOFYEAR(now())) and (c.day is null or c.day=day(now())) and (c.dayinweek is null or c.dayinweek=dayofweek(now())) and (c.activatorId=a.id) and (c.sensorId = 'null' or c.sensorId=b.sensorId)")
            cursor.execute(query);
            for (PROGID, ACTIVATOR, ID, STATE, SENSOR, T, TON, TOFF, START, STOP, MESEC, DAN, TEDEN, DANTEDNA) in cursor:
                data = str(i)+";"+str(PROGID)+";"+ACTIVATOR+";"+str(ID)+";"+str(STATE)+";"+SENSOR+";"+str(T)+";"+str(TON)+";"+str(TOFF)+";"+str(START)+";"+str(STOP)+";"+str(MESEC)+";"+str(DAN)+";"+str(TEDEN)+";"+str(DANTEDNA)
                client.publish(topic, payload=data, qos=0, retain=False)
                f.write("%s: Topic: %s Data: %s\n" % (datetime.datetime.now(), topic, data))
                i += 1
        elif cmd == "getActivators":
            topic += "/activator";
            query = ("select id, gpio, name, type, toggle_time_ms, state, manual from activators")
            cursor.execute(query);
            for (id, gpio, name, type, toggle_time_ms, state, manual) in cursor:
                data = str(i)+";"+str(id)+";"+str(gpio)+";"+name+";"+str(type)+";"+str(toggle_time_ms)+";"+str(state)+";"+str(manual)
                client.publish(topic, payload=data, qos=0, retain=False)
                f.write("%s: Topic: %s Data: %s\n" % (datetime.datetime.now(), topic, data))
                i += 1
        elif cmd == "getSensors":
            topic += "/temperature";
            query = ("select sensorId, name, T, last_change from sensors")
            cursor.execute(query);
            for (sensorId, name, T, last_change) in cursor:
                data = str(i)+";"+name+";"+str(T)+";"+str(last_change)+";"+sensorId
                client.publish(topic, payload=data, qos=0, retain=False)
                f.write("%s: Topic: %s Data: %s\n" % (datetime.datetime.now(), topic, data))
                i += 1
        f.flush()
        
def get_mysql_connection():
    global cnx
    try:
        if 'cnx' not in globals() or not cnx.is_connected():
            cnx = mysql.connector.connect(user='boris', password='tejkica00', host='127.0.0.1', database='senact')
            print "Connection to mysql renewed..."
            print cnx
    except mysql.connector.Error as err:
        cnx = None
        raise err
    else:
        return cnx

def gpio_error(channel):
    if GPIO.input(18):     # if port 18 == 1  
        msg = MIMEMultipart()
        msg["Subject"] = "Alarm!"
        msg["From"] = "Andrej.Franza@gmail.com"
        msg["To"] = "Andrej.Franza@gmail.com"
        msg["Cc"] = "Boris.Erzin@gmail.com"
        body = MIMEText("Zaznan signal 24 V!")
        msg.attach(body)
        smtp = smtplib.SMTP("localhost", 25)
        smtp.sendmail(msg["From"], msg["To"].split(",") + msg["Cc"].split(","), msg.as_string())
        smtp.quit()  
    else:                  # if port 18 != 1  
        msg = MIMEMultipart()
        msg["Subject"] = "Konec alarma!"
        msg["From"] = "Andrej.Franza@gmail.com"
        msg["To"] = "Andrej.Franza@gmail.com"
        msg["Cc"] = "Boris.Erzin@gmail.com"
        body = MIMEText("Signala 24 V ni vec!")
        msg.attach(body)
        smtp = smtplib.SMTP("localhost", 25)
        smtp.sendmail(msg["From"], msg["To"].split(",") + msg["Cc"].split(","), msg.as_string())
        smtp.quit()  
    
def gpio_callback(channel):
    global t9
    global t11
    global T
    now=datetime.datetime.now()
    if channel == 9:
        delta=now-t9
        name="T1"
        id='1'
    elif channel == 11:
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

k={'1':0.255,'2':0.255}
n={'1':-58.0,'2':-58.0}
T={}

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

channels = [2,3,4,17,27,22,10,9,11,7,8,25,24,23,15,14]
GPIO.setup(channels, GPIO.OUT, pull_up_down = GPIO.PUD_OFF)
GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_OFF)
GPIO.add_event_detect(18, GPIO.BOTH, callback=gpio_error, bouncetime=5)

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
 
f = open('/var/www/SenAct/senactsen.log','w')

#cnx = mysql.connector.connect(user='boris', password='tejkica00', host='127.0.0.1', database='senact')
#cnx = get_mysql_connection()

first = True
#cnx = None
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("iot.eclipse.org", 1883, 60)
client.loop_start()

while 1:
# ---------------------------------RC section --------------------------------------------------------
    tt=datetime.datetime.now()
    try:
        cnx = get_mysql_connection()
        cursor = cnx.cursor(buffered=True)
        cursor1 = cnx.cursor(buffered=True)
        if first:
            update = "update senact_cntrl set senactsen_active=TRUE"
        try:
            result = cursor1.execute(update)
            cnx.commit()
            first = False
        except:
            cnx.rollback()
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
        query = "select sensorId,T,k,n from sensors where type='RC'"
        cursor.execute(query)
        T={}
#	k={}
#	n={}
        sensorsDB={}
        for (sensorId,T1,k1,n1) in cursor:
            sensorDB={}
            sensorDB["sensorId"] = str(sensorId)
            sensorDB["T"]=T1
            sensorDB["k"]=k1
            sensorDB["n"]=n1
#            sensorsDB.append(sensorDB)
            sensorsDB[str(sensorId)] = sensorDB           

        sensorsRC = cursor.rowcount
        
#        print cursor.rowcount
#        if cursor.rowcount == 0:
#            t=dateime.datetime.now().isoformat()
#            insert = ("insert into sensors (sensorId,name,k,n,T,TL,TH,type,last_change) VALUES('1','T1',0.255,-58,20,20,20,'RC','"+t+"')")
#            cursor1.execute(insert)
#            insert = ("insert into sensors (sensorId,name,k,n,T,TL,TH,type,last_change) VALUES('2','T2',0.255,-58,20,20,20,'RC','"+t+"')")
#	     try:
#                cursor1.execute(insert)
#                cnx.commit()
#            except:
#      		 cnx.rollback()

        for id, sensorDB in sensorsDB.items():
            k[id] = sensorDB["k"]
            n[id] = sensorDB["n"]
            T[id] = sensorDB["T"]

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
                t=datetime.datetime.now().isoformat()
            if T[id]>130:
                if id in sensorsDB.keys():
                    update = ("delete from sensors where sensorId="+id)
                    try:
                        result=cursor1.execute(update)
                        cnx.commit()
                    except:
                        cnx.rollback()
#                update = ("update sensors set T=null,last_change='"+t+"' where sensorId="+id)
            else:
                if id not in sensorsDB.keys():
                    t=datetime.datetime.now().isoformat()
                    insert = ("insert into sensors (sensorId,name,k,n,T,TL,TH,type,last_change) VALUES("+id+",'T"+id+"',0.255,-58,"+str(T[id])+",20,20,'RC','"+t+"')")
                    try:
                        cursor1.execute(insert)
                        cnx.commit()
                    except:
                        cnx.rollback()
                else:
                    update = ("update sensors set T="+str(T[id])+",last_change='"+t+"' where sensorId="+id)
                    try:
                        result=cursor1.execute(update)
                        cnx.commit()
                    except:
                        cnx.rollback()
                    insert = ("insert into sensors_history (T,sensorId,sampleTime) VALUES("+str(T[id])+",'"+id+"','"+t+"')")
                    try:
                        result=cursor1.execute(insert)
                        cnx.commit()
                    except:
                        cnx.rollback()
        GPIO.remove_event_detect(9)
        GPIO.setup(9, GPIO.OUT, pull_up_down = GPIO.PUD_OFF)
        GPIO.output(9,0)
        GPIO.remove_event_detect(11)
        GPIO.setup(11, GPIO.OUT, pull_up_down = GPIO.PUD_OFF)
        GPIO.output(11,0)
# ---------------------------------- RC section END ----------------------------------------------

# ---------------------------------- DS18x20 section ---------------------------------------------
        query = "select sensorId,name,type,TL,TH from sensors where type!='RC'"
        result=cursor.execute(query)
        sensorsDB=[]
        id = 0
        for (sensorId,name,type,TL,TH) in cursor:
            sensorDB={}
            sensorDB["id"]=str(id)
            sensorDB["sensorId"]=sensorId
            sensorDB["name"]=name
            sensorDB["type"]=type
            sensorDB["TL"]=TL
            sensorDB["TH"]=TH
            sensorsDB.append(sensorDB)
            id += 1
   
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
#                        if temperature != 
                        client.publish("berzinkl/senact/"+socket.getfqdn()+"/temperature", payload=sensorDB["id"]+";"+sensorDB["name"]+";"+str(temperature)+";"+t+";"+ids, qos=0, retain=False)
                        update = ("update sensors set T="+str(temperature)+",last_change='"+t+"' where sensorId='"+sensorDB["sensorId"]+"'")
                        try:
                            result=cursor1.execute(update)
                            cnx.commit()
                        except:
                            cnx.rollback()
                        break
                if not found:
                    client.publish("berzinkl/senact/"+socket.getfqdn()+"/temperature", payload=sensorDB["id"]+";"+"TX;"+str(temperature)+";"+t+";"+ids, qos=0, retain=False)
                    insert = ("insert into sensors (T,sensorId,name,type,TL,TH,last_change) VALUES("+str(temperature)+",'"+sensor.id+"','TX','"+sensor.type_name+"',0,0"+",'"+t+"')")
                    try:
                        result=cursor1.execute(insert)
                        cnx.commit()
                    except:
                        cnx.rollback()
                    insert = ("insert into sensors_history (T,sensorId,sampleTime) VALUES("+str(temperature)+",'"+sensor.id+"','"+t+"')")
                    try:
                        result=cursor1.execute(insert)
                        cnx.commit()
                    except:
                        cnx.rollback()
            for sensorDB in sensorsDB:
                ids=sensorDB["sensorId"]
                found = False
                for sensor in sensors:
                    if sensor.id == sensorDB["sensorId"]:
                        found = True
                        break
                if not found:
                    update = ("update sensors set T=null where sensorId='"+sensorDB["sensorId"]+"'")
                    try:
                        result=cursor1.execute(update)
                        cnx.commit()
                    except:
                        cnx.rollback()
        except UnsupportedUnitError:
            f.write("UnsupportedUnitError\n")
            f.flush()
        except NoSensorFoundError:
            update = ("update sensors set T=null where sensorId="+ids)
            try:
                result=cursor1.execute(update)
                cnx.commit()
            except:
                cnx.rollback()
            f.write("NoSensorFoundError\n")
            f.flush()
        except SensorNotReadyError:
            update = ("update sensors set T=null where sensorId="+ids)
            try:
                result=cursor1.execute(update)
                cnx.commit()
            except:
                cnx.rollback()
            f.write("SensorNotReadyError\n")
            f.flush()
# ------------------------------------ DS18x20 section END -------------------------------------------

#        cnx.commit()
        
        query = "select * from senact_cntrl"
        cursor.execute(query)
        StopWhile = False
        SampleTime = 5
        for (prog,sen,sampletime) in cursor:
            if not sen:
                StopWhile = True
                break
            SampleTime = sampletime
#        cursor.close()
#        cursor1.close()
#        cnx.close()
        if StopWhile:
            break
        delta=datetime.datetime.now()-tt-datetime.timedelta(seconds=SampleTime)+datetime.timedelta(microseconds=4100)
#        print -delta.total_seconds()
        if delta.total_seconds()<0:
            time.sleep(-delta.total_seconds())
#        print datetime.datetime.now()-tt
client.loop_stop()
client.disconnect()
f.close()        
#GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(channels, GPIO.OUT, pull_up_down = GPIO.PUD_OFF, initial = GPIO.LOW)
GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_OFF)
