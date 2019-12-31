#!/bin/sh

clear

echo 'Cleaning old processes...'
str=`ps -Af | grep hosts_explor.py | grep -v "grep"`
arr=($(echo $str))
pid=${arr[1]}
kill -9 $pid

str=`ps -Af | grep hosts_enabler.py | grep -v "grep"`
arr=($(echo $str))
pid=${arr[1]}
kill -9 $pid

echo 'Done!'
echo 'Starting ...'
/usr/local/bin/python hosts_explor.py &
/usr/local/bin/python hosts_enabler.py &
echo 'Done!'

