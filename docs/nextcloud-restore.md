# Runbook: Nextcloud restore

Use this when Nextcloud data is lost, corrupted, or you are rebuilding the server from scratch.

**Estimated time:** 30-60 minutes depending on data size.

---

## Before you start

Confirm you have:
- A backup of the Nextcloud data directory
- A database dump (`nextcloud_db.sql`)
- The `.env` file with the original `MYSQL_PASSWORD` and `NEXTCLOUD_ADMIN_PASSWORD`

If you don't have all three, stop here. A partial restore will leave the instance in a broken state.

---

## Step 1: Stop the Nextcloud stack

```bash
cd /root/Gnode/apps/nextcloud
docker compose down
```

---

## Step 2: Restore the database

Start only the database container:

```bash
docker compose up -d nextcloud-db
```

Wait 10-15 seconds for MariaDB to finish initializing, then restore the dump:

```bash
docker exec -i nextcloud-db \
  mariadb -u nextcloud -p"${MYSQL_PASSWORD}" nextcloud \
  < /path/to/nextcloud_db.sql
```

Replace `/path/to/nextcloud_db.sql` with the actual path to your dump file.

---

## Step 3: Restore the data directory

The Nextcloud data directory maps to `./nextcloud-data` in the compose file. Copy your backup there:

```bash
rsync -av /path/to/backup/nextcloud-data/ \
  /root/Gnode/apps/nextcloud/nextcloud-data/
```

Make sure ownership is correct. Nextcloud runs as `www-data` (UID 33):

```bash
docker run --rm \
  -v /root/Gnode/apps/nextcloud/nextcloud-data:/data \
  alpine chown -R 33:33 /data
```

---

## Step 4: Start the full stack

```bash
docker compose up -d
```

Wait about 30 seconds for all containers to start.

---

## Step 5: Run the file scan

Nextcloud won't know about restored files until you run a scan:

```bash
docker exec -u www-data nextcloud \
  php occ files:scan --all
```

This can take several minutes if you have a large library.

---

## Step 6: Verify

Open Nextcloud in the browser and confirm:
- Files are visible
- Calendar and contacts sync (if you use them)
- No errors in Settings > Administration > Overview

Check logs for errors:

```bash
docker logs nextcloud --tail 50
```

---

## Maintenance mode

If you need to run the restore while the server is accessible, put Nextcloud in maintenance mode first:

```bash
docker exec -u www-data nextcloud php occ maintenance:mode --on
```

Turn it off after the restore:

```bash
docker exec -u www-data nextcloud php occ maintenance:mode --off
```

---

## Common problems

**Database connection error on startup**
The DB container may not be fully ready when Nextcloud starts. Run `docker compose restart nextcloud` and wait 30 seconds.

**Files show as 0 bytes**
The data directory ownership is wrong. Re-run the `chown` command from Step 3.

**"Integrity check failed" warning**
This is expected after a restore until you clear the cache:

```bash
docker exec -u www-data nextcloud php occ maintenance:repair
```
