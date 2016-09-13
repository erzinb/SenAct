#!/bin/bash
for (( i=0; i<=16; i++ ))
do
	/usr/local/bin/gpio mode $i out
	/usr/local/bin/gpio write $i 0
#	echo "gpio "$i" set to out and 0..."
done
sudo python /var/www/SenAct/senactsen.py &
#sudo python /var/www/SenAct/senactds1820.py &
sudo python /var/www/SenAct/senactprog.py &
