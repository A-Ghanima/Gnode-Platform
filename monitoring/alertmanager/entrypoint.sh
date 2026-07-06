#!/bin/sh
set -e
cp /etc/alertmanager/alertmanager.template.yml /tmp/alertmanager.yml
sed -i "s|\${TELEGRAM_BOT_TOKEN}|${TELEGRAM_BOT_TOKEN}|g" /tmp/alertmanager.yml
sed -i "s|\${TELEGRAM_CHAT_ID}|${TELEGRAM_CHAT_ID}|g" /tmp/alertmanager.yml
exec /bin/alertmanager --config.file=/tmp/alertmanager.yml
