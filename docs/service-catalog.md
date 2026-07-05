# Service catalog

All services run on the `main_net` Docker bridge network (`10.5.0.0/24`). Each service has a static IP assigned in its compose file.

---

## Infrastructure

### Nginx Proxy Manager
- **Container:** `proxy`
- **IP:** `10.5.0.10`
- **Image:** `jc21/nginx-proxy-manager:latest`
- **Ports:** 80, 443 (public), 81 (admin UI, internal only)
- **Purpose:** Reverse proxy and SSL termination for all public-facing services. Certificates are managed automatically via Let's Encrypt.
- **Compose:** `infrastructure/network/docker-compose.yml`

### Cloudflare DDNS
- **Container:** `ddns`
- **Image:** `favonia/cloudflare-ddns:latest`
- **Network mode:** host
- **Purpose:** Updates Cloudflare DNS records every hour with the server's current public IP. Runs in host network mode so it can read the correct external IP without NAT interference.
- **Compose:** `infrastructure/network/docker-compose.yml`

### CrowdSec
- **Container:** `crowdsec`
- **IP:** `10.5.0.12`
- **Image:** `crowdsecurity/crowdsec:latest`
- **Purpose:** Intrusion prevention. Parses logs from the host, Nginx Proxy Manager, and the Docker socket. Shares threat intelligence with the CrowdSec network.
- **Active collections:** `crowdsecurity/linux`, `crowdsecurity/nginx-proxy-manager`, `crowdsecurity/http-cve`, `crowdsecurity/whitelist-good-actors`
- **Compose:** `infrastructure/security/docker-compose.yml`

---

## Applications

### Nextcloud
- **Containers:** `nextcloud`, `nextcloud-db` (MariaDB 10.11), `nextcloud-redis`, `nextcloud-cron`
- **IPs:** app at `10.5.0.20` (DB), `10.5.0.21` (Redis), `10.5.0.22` (cron)
- **Image:** `nextcloud:latest`
- **Purpose:** File sync, calendar, and contacts. The cron container runs Nextcloud's background jobs on a schedule instead of relying on web-triggered cron.
- **Compose:** `apps/nextcloud/docker-compose.yml`

### Immich
- **Containers:** `immich-server`, `immich-ml`, `immich-redis`, `immich-db` (Postgres)
- **IPs:** `10.5.0.32` (server), `10.5.0.33` (ML), `10.5.0.23` (Redis), `10.5.0.24` (DB)
- **Image:** `ghcr.io/immich-app/immich-server:release`
- **Purpose:** Photo and video library with automatic facial recognition and CLIP-based search. The ML container runs the inference workloads separately so the main server stays responsive.
- **Compose:** `apps/immich/docker-compose.yml`

### Vaultwarden
- **Container:** `vaultwarden`
- **IP:** `10.5.0.50`
- **Image:** `vaultwarden/server:latest`
- **Purpose:** Bitwarden-compatible password manager. Signups are disabled; the instance is for personal use only.
- **Compose:** `apps/vaultwarden/docker-compose.yml`

---

## Monitoring

All monitoring services are defined in `monitoring/docker-compose.yml`.

### Node Exporter
- **Container:** `node-exporter`
- **IP:** `10.5.0.80`
- **Purpose:** Exposes host-level metrics (CPU, memory, disk, network) to Prometheus. Mounts `/proc`, `/sys`, and `/` read-only.

### cAdvisor
- **Container:** `cadvisor`
- **IP:** `10.5.0.81`
- **Purpose:** Per-container resource metrics. Prometheus scrapes it at `10.5.0.81:8080`.

### Prometheus
- **Container:** `prometheus`
- **IP:** `10.5.0.82`
- **Config:** `monitoring/prometheus/prometheus.yml`
- **Retention:** 30 days
- **Purpose:** Scrapes Node Exporter, cAdvisor, Blackbox Exporter, and Alertmanager every 15 seconds.

### Loki
- **Container:** `loki`
- **IP:** `10.5.0.83`
- **Config:** `monitoring/loki/loki.yml`
- **Retention:** 7 days
- **Purpose:** Log aggregation backend. Stores logs shipped by Promtail.

### Promtail
- **Container:** `promtail`
- **IP:** `10.5.0.84`
- **Config:** `monitoring/promtail/promtail.yml`
- **Purpose:** Tails the Docker socket and `/var/log`, labels log streams by container name, and ships them to Loki.

### Grafana
- **Container:** `grafana`
- **IP:** `10.5.0.85`
- **Purpose:** Dashboard and log exploration UI. Connects to both Prometheus (metrics) and Loki (logs) as data sources.

### Alertmanager
- **Container:** `alertmanager`
- **IP:** `10.5.0.86`
- **Config:** `monitoring/alertmanager/alertmanager.yml`
- **Purpose:** Receives alerts from Prometheus and routes them to a Telegram bot. Current alert rules: disk usage >80%, RAM >85%, container restart loop.

### Blackbox Exporter
- **Container:** `blackbox`
- **IP:** `10.5.0.87`
- **Config:** `monitoring/exporters/blackbox.yml`
- **Purpose:** HTTP probing for public domains. Prometheus scrapes it with target URLs as parameters, and Alertmanager fires if a probe fails.

---

