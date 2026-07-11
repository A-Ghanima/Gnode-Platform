#!/bin/sh

# Add cron job — runs at 2am daily
echo "0 2 * * * cd /app && sh backup.sh && python upload.py >> /var/log/backup.log 2>&1" | crontab -

# Run once immediately on startup to test
echo "Running initial backup..."
sh backup.sh && python upload.py

# Start cron daemon
echo "Starting cron daemon..."
crond -f -l 2
