#!/bin/bash
mysql -h localhost -uboris senact -ptejkica00 -e "delete from sensors_history where TIMESTAMPDIFF(DAY,sampleTime,NOW())>=1;"
