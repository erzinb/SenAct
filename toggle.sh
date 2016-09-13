#!/bin/bash
#res=(`mysql -h localhost -uboris senact -ptejkica00 -e "select type from activators where id="$1`);
#if [ ${res[1]} -eq 1 ]
#then
#date +"%F %T,%3N"
gpio write $2 1
sleep $4
gpio write $2 0
#date +"%F %T,%3N"
mysql -h localhost -uboris senact -ptejkica00 -e "update activators set state="$3" where id="$1;