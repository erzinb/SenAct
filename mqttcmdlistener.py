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
    client.subscribe("berzinkl/senact/cmd/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global f
    cmd = msg.payload
    f.write(msg.topic+" "+cmd+"\n")
    f.flush()
    try:
        cnx = mysql.connector.connect(user='boris', password='tejkica00',
                          host='127.0.0.1',
                          database='senact')
        cursor = cnx.cursor()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            f.write("Something is wrong with your user name or password\n")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            f.write("Database does not exist\n")
        else:
            f.write(err+'\n')
    else:
        i = 0
        if cmd == "getPrograms":
            query = ("select distinct c.id as PROGID, a.name as ACTIVATOR, a.id as ID, a.state as STATE, case when c.sensorId = 'null' then null else b.name end as SENSOR, case when c.sensorId = 'null' then null else b.T end as T, case when c.TON = 'null' then null else c.TON end as TON, case when c.TOFF = 'null' then null else c.TOFF end as TOFF, c.start_time as START, c.stop_time as STOP, c.month as MESEC, c.week as TEDEN, c.day as DAN, c.dayinweek as DANTEDNA from programs c,activators a, sensors b where c.start_time<TIME(NOW()) and c.stop_time>=TIME(NOW()) and (c.month is null or c.month=MONTH(NOW())) and (c.week is null or c.week=WEEKOFYEAR(now())) and (c.day is null or c.day=day(now())) and (c.dayinweek is null or c.dayinweek=dayofweek(now())) and (c.activatorId=a.id) and (c.sensorId = 'null' or c.sensorId=b.sensorId)")
            cursor.execute(query);
            for (PROGID, ACTIVATOR, ID, STATE, SENSOR, T, TON, TOFF, START, STOP, MESEC, DAN, TEDEN, DANTEDNA) in cursor:
                client.publish("berzinkl/senact/"+socket.getfqdn()+"/program", payload=str(i)+";"+str(PROGID)+";"+ACTIVATOR+";"+str(ID)+";"+str(STATE)+";"+SENSOR+";"+str(T)+";"+str(TON)+";"+str(TOFF)+";"+str(START)+";"+str(STOP)+";"+str(MESEC)+";"+str(DAN)+";"+str(TEDEN)+";"+str(DANTEDNA), qos=0, retain=False)
                i += 1
        elif cmd == "getActivators":
            query = ("select id, gpio, name, type, toggle_time_ms, state, manual from activators")
            cursor.execute(query);
            for (id, gpio, name, type, toggle_time_ms, state, manual) in cursor:
                client.publish("berzinkl/senact/"+socket.getfqdn()+"/activator", payload=str(i)+";"+str(id)+";"+str(gpio)+";"+name+";"+str(type)+";"+str(toggle_time_ms)+";"+str(state)+";"+str(manual), qos=0, retain=False)
                i += 1
        elif cmd == "getSensors":
            query = ("select sensorId, name, T, last_change from sensors")
            cursor.execute(query);
            for (sensorId, name, T, last_change) in cursor:
                client.publish("berzinkl/senact/"+socket.getfqdn()+"/temperature", payload=str(i)+";"+name+";"+str(T)+";"+str(last_change)+";"+sensorId, qos=0, retain=False)
                i += 1
            
        cursor.close()
        cnx.close()


if os.path.exists('/var/www/SenAct/mqttcmdlistener.log'):
    os.rename('/var/www/SenAct/mqttcmdlistener.log','/var/www/SenAct/mqttcmdlistener.log.old')
 
f = open('mqttcmdlistener.log','w')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("iot.eclipse.org", 1883, 60)
try:
    client.loop_forever()
except KeyboardInterrupt:
    client.disconnect()

