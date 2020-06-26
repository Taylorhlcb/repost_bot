#!/bin/bash
echo "Copy over the build."
rm -fr /home/gitlab-runner/auth_bot_deploy/
mkdir /home/gitlab-runner/auth_bot_deploy/
cp -r * /home/gitlab-runner/auth_bot_deploy/

#/etc/systemd/system/auth_bot.service
echo "Restarting service."
sudo systemctl restart auth_bot
echo "Checking service."
sudo systemctl status auth_bot