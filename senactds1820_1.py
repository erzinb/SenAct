import mysql.connector
import datetime
import time
import RPi.GPIO as GPIO
import os
from w1thermsensor import W1ThermSensor
from w1thermsensor import UnsupportedUnitError
from w1thermsensor import NoSensorFoundError
from w1thermsensor import SensorNotReadyError

if os.path.exists('/var/www/SenAct/senactds1820.log'):
    os.rename('/var/www/SenAct/senactds1820.log','/var/www/SenAct/senactds1820.log.old')
 
f = open('senactds1820.log','w')

while 1:
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
        query = ("select sensorId,type from sensors where type!='RC'")
        result=cursor.execute(query)
#        ids="0"
        try:
            sensors = W1ThermSensor.get_available_sensors()
            for sensor in sensors:
                found = False
                print sensor.id
                for (sensorId,type) in cursor:
#                    ids=sensorId
                    print sensorId
                    print "sensorId: {}:{}".format(sensorId,sensor.id)
                    if sensor.id == sensorId:
                        found = True
                        update = ("update sensors set T="+str(sensor.get_temperature())+" where sensorId='"+sensorId+"'")
                        result=cursor1.execute(update)
                        break
                if not found:
                    insert = ("insert into sensors (T,sensorId,name,type,TL,TH) VALUES("+str(sensor.get_temperature())+",'"+sensor.id+"','TX','"+sensor.type_name+"',0,0)")
                    result=cursor1.execute(insert)
            for (sensorId,type) in cursor:
#                ids=sensorId
                found = False
                for sensor in sensors:
                    if sensor.id == sensorId:
                        found = True
                        break
                if not found:
                    delete = ("delete from sensors where sensorId="+sensorId)
                    result=cursor1.execute(delete)
        except UnsupportedUnitError:
            f.write("UnsupportedUnitError\n")
        except NoSensorFoundError:
#            update = ("update sensors set T=170.0 where sensorId="+ids)
#            result=cursor1.execute(update)
            f.write("NoSensorFoundError\n")
        except SensorNotReadyError:
#            update = ("update sensors set T=170.0 where sensorId="+ids)
#            result=cursor1.execute(update)
            f.write("SensorNotReadyError\n")
        f.flush()
    
        cnx.commit()
        
        cursor.close()
        cursor1.close()
        cnx.close()
        time.sleep(3)
f.close()        
