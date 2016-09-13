#!/bin/bash
#from=`mysql -h localhost -uboris senact -ptejkica00 -e "select blocking from activators where id="$1`;
#date +"%F %T,%3N"
sleep $2
#date +"%F %T,%3N"
#to=`mysql -h localhost -uboris senact -ptejkica00 -e "update activators set blocking=0 where id="$1`;
mysql -h localhost -uboris senact -ptejkica00 -e "update activators set blocking=0 where id="$1;
#echo "For id="$1", "$from" changed to 0."

