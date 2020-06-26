#!/bin/bash
A="$(pgrep -f auth_bot)"
if [ -z "$A" ]
then
        exit
else
        kill -9 $A
fi
if [ -z "$1" ]
then
        read -p "Enter config name to start authbot: " config_file
else
        config_file=$1
fi
if [ -z "$config_file" ]
then
    read -p "You have to enter a config name to start the bot... Exiting" A
    exit
else
    if [ -z "$2" ]
    then
        setsid nohup python3 auth_bot.py $config_file > ~/auth_bot/auth_bot.out &
        exit
    else
        setsid nohup python3 auth_bot.py $config_file $2 > ~/auth_bot/auth_bot.out &
        exit
    fi
fi