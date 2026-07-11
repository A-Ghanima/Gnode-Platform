#!/bin/sh
set -e

TIMESTAMP=$(date +%Y%m%dT%H%M%S)
mkdir -p $BACKUP_DIR

echo "Starting backups at $TIMESTAMP"

# Nextcloud MariaDB
echo "Backing up Nextcloud database..."
mysqldump --no-defaults --ssl=false \
  -h $NEXTCLOUD_DB_HOST \
  -u $NEXTCLOUD_DB_USER \
  -p$NEXTCLOUD_DB_PASSWORD \
  $NEXTCLOUD_DB_NAME \
  | gzip > $BACKUP_DIR/nextcloud-db-$TIMESTAMP.sql.gz
echo "Nextcloud DB done."

# Immich PostgreSQL
echo "Backing up Immich database..."
PGPASSWORD=$IMMICH_DB_PASSWORD pg_dump \
  -h $IMMICH_DB_HOST \
  -U $IMMICH_DB_USER \
  $IMMICH_DB_NAME \
  | gzip > $BACKUP_DIR/immich-db-$TIMESTAMP.sql.gz
echo "Immich DB done."

# Vaultwarden SQLite
echo "Backing up Vaultwarden..."
cp /vaultwarden-data/db.sqlite3 $BACKUP_DIR/vaultwarden-$TIMESTAMP.sqlite3
gzip $BACKUP_DIR/vaultwarden-$TIMESTAMP.sqlite3
echo "Vaultwarden done."

echo "All backups complete."
