# Disaster recovery playbook

This covers a full server rebuild: hardware failure, OS corruption, or migration to a new machine. The goal is to get all services back up from a clean Alpine Linux install.

**Estimated time:** 1-2 hours depending on data restore size.

---

## Prerequisites

Before you can recover, you need:

- A fresh Alpine Linux install with network access and SSH enabled
- The Gnode-Platform git repository (or a local copy)
- Your age private key (`~/.age-key.txt`) — backed up somewhere outside the server
- Backups of all persistent data volumes (see the backup locations table below)

If you don't have the age key, you cannot decrypt SOPS secrets. You will need to recreate those values manually and re-encrypt them.

---

## Backup locations

| Data | Location |
|---|---|
| Nextcloud files | `apps/nextcloud/nextcloud-data/` |
| Nextcloud DB | Backup dump: `nextcloud_db.sql` |
| Immich library | `apps/immich/library/` |
| Immich DB | Backup dump: `immich_db.sql` |
| Vaultwarden vault | `apps/vaultwarden/vaultwarden/` |
| CrowdSec config | `infrastructure/security/config/` (gitignored) |
| Prometheus data | Docker volume `monitoring_prometheus_data` |
| Loki data | Docker volume `monitoring_loki_data` |
| Grafana data | Docker volume `monitoring_grafana_data` |

Prometheus, Loki, and Grafana data are not critical to restore — they will repopulate over time. Everything else should be backed up before any planned maintenance.

---

## Step 1: Base system setup

On the fresh Alpine install:

```bash
# Update and install base packages
apk update && apk upgrade
apk add git curl nano openssh

# Enable SSH on boot
rc-update add sshd
service sshd start
```

---

## Step 2: Restore the age key

Copy your age key from your backup storage to the new server:

```bash
mkdir -p ~/.age-key.txt
# scp or paste the key content
chmod 600 ~/.age-key.txt
```

---

## Step 3: Install Ansible dependencies

```bash
apk add python3 py3-pip ansible
pip install --break-system-packages ansible

ansible-galaxy collection install community.docker
```

---

## Step 4: Clone the repository

```bash
git clone https://github.com/A-Ghanima/Gnode-Platform.git /root/Gnode
cd /root/Gnode
```

---

## Step 5: Populate secrets

Copy `.env` files from your backup or recreate them from the `.env.example` files:

```bash
cp apps/nextcloud/.env.example apps/nextcloud/.env
cp apps/immich/.env.example apps/immich/.env
cp apps/vaultwarden/.env.example apps/vaultwarden/.env
cp infrastructure/network/.env.example infrastructure/network/.env
cp monitoring/.env.example monitoring/.env
```

Edit each file with the real values. If you have a backup of the original `.env` files, copy those instead.

---

## Step 6: Run the Ansible bootstrap

```bash
cd /root/Gnode/ansible
ansible-playbook -i inventory/hosts.yml playbooks/bootstrap.yml
```

This installs Docker, creates `main_net`, deploys CrowdSec, and deploys the monitoring stack.

---

## Step 7: Restore application data

### Nextcloud

Follow `docs/runbooks/nextcloud-restore.md` in full.

### Immich

```bash
# Restore the library files
rsync -av /path/to/backup/immich-library/ \
  /root/Gnode/apps/immich/library/

# Start the DB container first
cd /root/Gnode/apps/immich
docker compose up -d database

# Wait 15 seconds, then restore the DB dump
docker exec -i immich_postgres \
  psql -U postgres immich \
  < /path/to/immich_db.sql

# Start the rest
docker compose up -d
```

### Vaultwarden

```bash
rsync -av /path/to/backup/vaultwarden/ \
  /root/Gnode/apps/vaultwarden/vaultwarden/

cd /root/Gnode/apps/vaultwarden
docker compose up -d
```

---

## Step 8: Deploy remaining stacks

```bash
cd /root/Gnode/apps/nextcloud && docker compose up -d
cd /root/Gnode/apps/immich && docker compose up -d
cd /root/Gnode/apps/vaultwarden && docker compose up -d
cd /root/Gnode/infrastructure/network && docker compose up -d
```

---

## Step 9: Verify

Check all containers are running:

```bash
docker ps --format "table {{.Names}}\t{{.Status}}"
```

Every container should show `Up`. Any container in `Restarting` or `Exited` state needs investigation before you consider the recovery done.

Open Grafana at `http://10.5.0.85:3000` and confirm metrics are flowing from Node Exporter and cAdvisor. Check Loki has logs from the running containers.

Send a test message to confirm Telegram alerting works — trigger a manual alert or temporarily lower a threshold in the alerting rules.

---

## RTO and RPO estimates

| Metric | Estimate |
|---|---|
| RTO (time to recover) | 1-2 hours |
| RPO (data loss window) | Depends on backup frequency — aim for daily |

These are estimates based on a manual recovery. Automating the data backup step would reduce both significantly.
