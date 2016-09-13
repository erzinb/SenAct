#!/bin/bash
if [ `ps -ef | grep $1 | grep -v grep | grep -v sudo | wc -l` -eq 0 ]
then
	echo "starting"
	sudo "python /var/www/SenAct/"$1"  > /dev/null 2>&1 &"
fi