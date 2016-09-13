#!/bin/bash
echo `ps -ef | grep senactprog.py | grep -v grep | grep -v sudo | grep -v start | wc -l`
if [ `ps -ef | grep senactprog.py | grep -v grep | grep -v sudo | grep -v start | wc -l` -eq 0 ]
then
	echo "starting"
	sudo python /var/www/SenAct/senactprog.py > /dev/null 2>&1 &
fi