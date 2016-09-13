#!/bin/bash
sudo python /var/www/SenAct/senactini.py
sudo python /var/www/SenAct/senactsen.py &
sudo python /var/www/SenAct/senactprog.py &
sudo /var/www/SenAct/network-monitor.sh &
