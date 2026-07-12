# Gnode-Platform

Production-grade self-hosted infrastructure platform — built, operated, and automated by a single engineer.

![CI](https://github.com/A-Ghanima/Gnode-Platform/actions/workflows/yamllint.yml/badge.svg)
![Security](https://github.com/A-Ghanima/Gnode-Platform/actions/workflows/security-scan.yml/badge.svg)
![Trivy](https://github.com/A-Ghanima/Gnode-Platform/actions/workflows/trivy.yml/badge.svg)

## Overview

Gnode-Platform is the infrastructure-as-code repository for **gnode** — a self-hosted homelab server running on Alpine Linux, operated since 2023 with high uptime and ~27 Docker containers across multiple stacks.

The goal of this project is to operate the homelab the way a real company would: with automated provisioning, secrets management, observability, security scanning, and GitOps practices — not just a collection of docker-compose files.

This repository contains everything needed to rebuild the entire platform from scratch with a single command.

## Platform Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        gnode server                         │
│                        Alpine Linux                         │
│                                                             │
│  ┌──────────┐  ┌──────────┐   ┌──────────────────────────┐  │
│  │ Security │  │ Network  │   │      Applications        │  │
│  │ CrowdSec │  │  NPM     │   │  Nextcloud               │  │
│  │          │  │  DDNS    │   │  Immich                  │  │
│  └──────────┘  └──────────┘   │  Vaultwarden             │  │
│                               └──────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Monitoring (PLG Stack)                 │    │
│  │  Prometheus · Loki · Grafana · Alertmanager         │    │
│  │  Node Exporter · cAdvisor · Promtail                │    │
│  │  Blackbox · smartctl · mariadb · nginx exporters    │    │
│  └─────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              DevOps Dashboard                       │    │
│  │  FastAPI backend · React + TypeScript frontend      │    │
│  │  JWT auth · Docker stats · Prometheus metrics       │    │
│  │  Live at: dash.thegnode.space                       │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│              Docker Network: main_net                       │
│              Subnet: 10.5.0.0/24                            │
└─────────────────────────────────────────────────────────────┘
```

## Tech Stack

| Layer | Technology | Why |
|---|---|---|
| OS | Alpine Linux | Minimal footprint, ideal for servers |
| Containerization | Docker + Compose | Industry standard, portable |
| Reverse Proxy | Nginx Proxy Manager | SSL termination, easy routing |
| DNS | Cloudflare DDNS | Dynamic IP management |
| Security | CrowdSec | Collaborative IPS, modern alternative to Fail2ban |
| Secrets | SOPS + age | Encrypted secrets in Git — no plaintext credentials ever |
| Observability | Prometheus + Loki + Grafana | Production-grade PLG stack |
| Alerting | Alertmanager + Telegram | Real-time incident notifications |
| Uptime Probing | Blackbox Exporter | Domain-level HTTP monitoring |
| Provisioning | Ansible | Full server rebuild automation |
| CI/CD | GitHub Actions | YAML linting, secret scanning, CVE detection on every push |
| Dashboard | FastAPI + React + TypeScript | Internal DevOps control plane |
| Backups | Python + Telegram Bot API | Automated daily DB backups with delivery |

## Repository Structure

```
Gnode-Platform/
├── ansible/                    # Server provisioning automation
│   ├── inventory/              # Host definitions + group_vars
│   ├── playbooks/              # bootstrap.yml — full server rebuild
│   ├── roles/                  # docker, networking, security, monitoring
│   └── ansible.cfg
├── apps/                       # Self-hosted applications
│   ├── immich/                 # Photo library (PostgreSQL + pgvector)
│   ├── nextcloud/              # File sync + collaboration (MariaDB)
│   └── vaultwarden/            # Password manager (SQLite)
├── bots/
│   └── telegram/
│       └── db-backup/          # Automated DB backup bot (Telegram delivery)
├── dashboard/                  # DevOps dashboard — live at dash.thegnode.space
│   ├── backend/                # FastAPI REST API with JWT auth + Docker stats
│   └── frontend/               # React + TypeScript + Tailwind
├── infrastructure/             # Core platform services
│   ├── network/                # NPM + Cloudflare DDNS
│   └── security/               # CrowdSec IPS
├── monitoring/                 # PLG observability stack
│   ├── prometheus/             # Metrics + alerting rules
│   ├── loki/                   # Log storage
│   ├── promtail/               # Log shipping
│   ├── alertmanager/           # Alert routing (Telegram)
│   ├── grafana/                # Dashboards
│   └── exporters/              # Blackbox, MariaDB, nginx, smartctl
├── docs/                       # Architecture docs, runbooks, postmortems
├── scripts/                    # Utility scripts
├── .github/
│   ├── workflows/              # CI: yamllint, gitleaks, trivy
│   ├── ISSUE_TEMPLATE/         # Incident + change request templates
│   └── PULL_REQUEST_TEMPLATE.md
├── .sops.yaml                  # SOPS encryption config (age)
├── .yamllint.yml               # YAML linting rules
└── Makefile                    # make help, make status
```

## Services & IP Map

| Service | Container | IP |
|---|---|---|
| Nginx Proxy Manager | proxy | 10.5.0.10 |
| CrowdSec | crowdsec | 10.5.0.12 |
| Nextcloud DB | nextcloud_database | 10.5.0.20 |
| Nextcloud Redis | nextcloud_redis | 10.5.0.21 |
| Nextcloud Cron | nextcloud-cron | 10.5.0.22 |
| Immich ML | immich-ml | 10.5.0.23 |
| Immich Redis | immich-redis | 10.5.0.24 |
| Immich DB | immich-database | 10.5.0.25 |
| Vaultwarden | vaultwarden | 10.5.0.50 |
| Nextcloud | nextcloud | 10.5.0.51 |
| Immich Server | immich-server | 10.5.0.52 |
| DB Backup Bot | gnode-db-backup | 10.5.0.70 |
| Node Exporter | node-exporter | 10.5.0.80 |
| cAdvisor | cadvisor | 10.5.0.81 |
| Prometheus | prometheus | 10.5.0.82 |
| Loki | loki | 10.5.0.83 |
| Promtail | promtail | 10.5.0.84 |
| Grafana | grafana | 10.5.0.85 |
| Alertmanager | alertmanager | 10.5.0.86 |
| Blackbox Exporter | blackbox | 10.5.0.87 |
| nginx Exporter | nginx-exporter | 10.5.0.88 |
| smartctl Exporter | smartctl-exporter | 10.5.0.90 |
| MariaDB Exporter | mariadb-exporter | 10.5.0.93 |
| Dashboard Backend | gnode-dashboard-backend | 10.5.0.100 |
| Dashboard Frontend | gnode-dashboard-frontend | 10.5.0.101 |

## Dashboard

The Gnode DevOps Dashboard is a production-grade internal control plane built from scratch:

- **Authentication**: JWT with bcrypt password hashing
- **Container Management**: Start, stop, restart any container
- **Real-time Metrics**: Per-container CPU and RAM via Docker stats API (concurrent collection)
- **Host Metrics**: CPU, RAM, disk usage from Prometheus + Node Exporter
- **Grouped View**: Containers organized by group using Docker labels
- **Auto-refresh**: Container status every 10s, metrics every 30s

**Tech**: FastAPI (Python) · React + TypeScript · Tailwind CSS · Docker multi-stage build · Nginx

> **Security note**: The Docker socket is mounted with `:rw` access — a known risk. Production hardening would involve a Docker Socket Proxy to restrict API surface.

## Quick Start

### Prerequisites

- Alpine Linux server (or any Linux distro)
- Docker + Docker Compose installed
- Ansible 2.18+
- `age` + `SOPS` installed
- `community.docker` Ansible collection

### 1. Clone the repository

```bash
git clone https://github.com/A-Ghanima/Gnode-Platform.git
cd Gnode-Platform
```

### 2. Set up secrets

```bash
age-keygen -o ~/.age-key.txt
cp apps/nextcloud/.env.example apps/nextcloud/.env
cp apps/immich/.env.example apps/immich/.env
cp apps/vaultwarden/.env.example apps/vaultwarden/.env
cp infrastructure/network/.env.example infrastructure/network/.env
cp monitoring/.env.example monitoring/.env
cp dashboard/backend/.env.example dashboard/backend/.env
```

### 3. Bootstrap the platform

```bash
cd ansible
ansible-playbook -i inventory/hosts.yml playbooks/bootstrap.yml
```

## Secrets Management

All secrets are managed with **SOPS + age**. No plaintext credentials exist in this repository.

- `.env` files are gitignored — copy from `.env.example` and populate locally
- Sensitive values that need to be in Git are encrypted with SOPS before committing
- A Gitleaks pre-commit hook blocks any commit containing unencrypted secrets
- The `security-scan.yml` GitHub Actions workflow runs Gitleaks on every push to main

## CI/CD

| Workflow | Trigger | Purpose |
|---|---|---|
| `yamllint.yml` | Push to main | Validates all YAML files |
| `security-scan.yml` | Push to main | Scans for leaked secrets (Gitleaks) |
| `trivy.yml` | Push to main | CVE scanning for Docker images |

## Roadmap

- [x] Complete bots/ stack — automated DB backup bot with Telegram delivery
- [x] DevOps dashboard with container management and real-time metrics
- [ ] Add shellcheck workflow for shell scripts
- [ ] Docker Socket Proxy to harden dashboard security
- [ ] Complete documentation (runbooks, disaster recovery, postmortems)
- [ ] Kubernetes migration path

## License

MIT © Ahmed Ghanima
