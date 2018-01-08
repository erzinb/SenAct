#!/usr/bin/env python
import mysql.connector
import datetime
import time
#import RPi.GPIO as GPIO
#from subprocess import call
import requests
import os

def ugasni(k):
#    gpio=getgpio(k)
    global f
    f.write("Ugasam %d\n" % k)
    f.flush()
    r = requests.get('http://boris:bs@localhost/SenAct/activators.php?id='+str(k)+'&action=write&value=0&block=1')
    return

def prizgi(k):
#    gpio=getgpio(k)
    global f
    f.write("Prizigam %d\n" % k)
    f.flush()
    r = requests.get('http://boris:bs@localhost/SenAct/activators.php?id='+str(k)+'&action=write&value=1&block=1')
    return

def getgpio(id):
    global cnx
    cursor = cnx.cursor()
    query = ("select gpio FROM activators WHERE id=1")
    cursor.execute(query)
    data = cursor.fetchone()
    return data[0]

if os.path.exists('/var/www/SenAct/senactprog.log'):
    os.rename('/var/www/SenAct/senactprog.log','/var/www/SenAct/senactprog.log.old')

f = open('/var/www/SenAct/senactprog.log','w')

first=True

oldstates={}
while 1:
    try:
        cnx = mysql.connector.connect(user='boris', password='tejkica00',
                          host='127.0.0.1',
                          database='senact')
        cursor = cnx.cursor()
        cursor1 = cnx.cursor(buffered=True)
        if first:
            update = ("update senact_cntrl set senactprog_active=TRUE")
            try:
                result = cursor1.execute(update)
                cnx.commit()
            except:
                cnx.rollback()
    except KeyboardInterrupt:
        break
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            f.write("Something is wrong with your user name or password\n")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            f.write("Database does not exist\n")
        else:
            f.write(err+'\n')
        break
    else:
        states={}
        sensors={}
        Ts={}
        TONs={}
        TOFFs={}
#        query = ("select distinct a.name as ACTIVATOR, a.id as ID, case when c.sensorId = 'null' then 0 else a.state end as STATE, case when c.sensorId = 'null' then null else b.name end as SENSOR, case when c.sensorId = 'null' then null else b.T end as T, case when c.sensorId = 'null' then null else b.TL end as TON, case when c.sensorId = 'null' then null else b.TH end as TOFF, c.start_time as START, c.stop_time as STOP, c.month as MESEC, c.week as TEDEN, c.day as DAN, c.dayinweek as DANTEDNA from programs c,activators a, sensors b where c.start_time<TIME(NOW()) and c.stop_time>=TIME(NOW()) and (c.month is null or c.month=MONTH(NOW())) and (c.week is null or c.week=WEEKOFYEAR(now())) and (c.day is null or c.day=day(now())) and (c.dayinweek is null or c.dayinweek=dayofweek(now())) and (c.sensorId = 'null' or (a.state in (0,2) and (b.TL is null or b.T < b.TL)) or (a.state in (1,3) and (b.TH is null or b.T > b.TH))) and (c.activatorId=a.id) and (c.sensorId = 'null' or c.sensorId=b.id)")
        query = ("select distinct a.name as ACTIVATOR, a.id as ID, a.state as STATE, case when c.sensorId = 'null' then null else b.name end as SENSOR, case when c.sensorId = 'null' then null else b.T end as T, case when c.TON = 'null' then null else c.TON end as TON, case when c.TOFF = 'null' then null else c.TOFF end as TOFF, c.start_time as START, c.stop_time as STOP, c.month as MESEC, c.week as TEDEN, c.day as DAN, c.dayinweek as DANTEDNA from programs c,activators a, sensors b where c.start_time<TIME(NOW()) and c.stop_time>=TIME(NOW()) and (c.month is null or c.month=MONTH(NOW())) and (c.week is null or c.week=WEEKOFYEAR(now())) and (c.day is null or c.day=day(now())) and (c.dayinweek is null or c.dayinweek=dayofweek(now())) and (c.activatorId=a.id) and (c.sensorId = 'null' or c.sensorId=b.sensorId)")
        cursor.execute(query);
        for (ACTIVATOR, ID, STATE, SENSOR, T, TON, TOFF, START, STOP, MESEC, DAN, TEDEN, DANTEDNA) in cursor:
#            if SENSOR != None:
            states[ID]=STATE
            sensors[ID]=SENSOR
            Ts[ID]=T
            TONs[ID]=TON
            TOFFs[ID]=TOFF
#            else:
#                states[ID]=5
#            print SENSOR
#            print("{},{},{},{},{},{},{},{},{},{},{},{},{}".format(ACTIVATOR, ID, STATE, SENSOR, T, TON, TOFF, START, STOP, MESEC, DAN, TEDEN, DANTEDNA))

#        cnx.commit()

        if first:
            for k in states:
                if states[k]==1:
                    prizgi(k)

        for k in states:
            if states[k]==0:
                if sensors[k] != None:
                    if TOFFs[k] > TONs[k]:
                        if Ts[k] < TONs[k]:
#                        print("TUKAJ SEM")
                            prizgi(k)
                    else:
                        if Ts[k] > TONs[k]:
#                        print("TUKAJ SEM")
                            prizgi(k)
                else:
#                    print("TUKAJ SEM 1")
                    prizgi(k)
            else:
                if states[k]==3:
                    if sensors[k] != None:
                        if TOFFs[k] > TONs[k]:
                            if Ts[k] < TONs[k]:
                                prizgi(k)
                        else:
                            if Ts[k] > TONs[k]:
                                prizgi(k)
                    else:
                        prizgi(k)
                else:
                    if states[k]!=5:
                        if sensors[k] != None:
                            if TOFFs[k] > TONs[k]:
                                if Ts[k] > TOFFs[k]:
                                    ugasni(k)
                            else:
                                if Ts[k] < TOFFs[k]:
                                    ugasni(k)
#                        else:
#                            print "No sensor..."
#                    else:
#                        print "No sensor..."
#                        prizgi(k)


        for k in oldstates:
            if states.has_key(k)==False:
                ugasni(k)

        oldstates=states.copy()
        first=False

        query = ("select * from senact_cntrl")
        cursor.execute(query)
        StopWhile = False
        SampleTime = 5
        for (prog,sen,sampletime) in cursor:
            if not prog:
                StopWhile = True
                break
            SampleTime = sampletime
        cursor.close()
        cnx.close()
        if StopWhile:
            break

        time.sleep(SampleTime)
f.close()
