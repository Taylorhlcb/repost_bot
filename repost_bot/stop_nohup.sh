#!/bin/bash
A="$(pgrep -f auth_bot)"
if [ -z "$A" ]
then
        exit
else
        kill -9 $A
fi