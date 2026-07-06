# Gnode-Platform

> Production-grade self-hosted infrastructure platform — built, operated, and automated by a single engineer.

![CI](https://github.com/A-Ghanima/Gnode-Platform/actions/workflows/yamllint.yml/badge.svg)
![Security](https://github.com/A-Ghanima/Gnode-Platform/actions/workflows/security-scan.yml/badge.svg)
![Trivy](https://github.com/A-Ghanima/Gnode-Platform/actions/workflows/trivy.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

---

## Overview

Gnode-Platform is the infrastructure-as-code repository for **gnode** — a self-hosted homelab server running on Alpine Linux, operated since 2023 with high uptime and ~25 Docker containers across multiple stacks.

The goal of this project is to operate the homelab the way a real company would: with automated provisioning, secrets management, observability, security scanning, and GitOps practices — not just a collection of docker-compose files.

This repository contains everything needed to rebuild the entire platform from scratch with a single command.

---

## Platform Architecture

```
┌─────────────────────────────────────────────────────┐
│                    gnode server                     │
│                    Alpine Linux                     │
│                                                     │
│  ┌──────────┐  ┌──────────┐   ┌──────────────────┐  │
│  │ Security │  │ Network  │   │  Applications    │  │
│  │ CrowdSec │  │  NPM     │   │  Nextcloud       │  │
│  │          │  │  DDNS    │   │  Immich          │  │
│  └──────────┘  └──────────┘   │  Vaultwarden     │  │
│                               └──────────────────┘  │
│  ┌─────────────────────────────────────────────┐    │
│  │              Monitoring (PLG Stack)         │    │
│  │  Prometheus · Loki · Grafana · Alertmanager │    │
│  │  Node Exporter · cAdvisor · Promtail        │    │
│  │  Blackbox Exporter                          │    │
│  └─────────────────────────────────────────────┘    │
│                                                     │
│              Docker Network: main_net               │
│              Subnet: 10.5.0.0/24                    │
└─────────────────────────────────────────────────────┘
```

All services communicate over a single flat Docker bridge network (`main_net`, `10.5.0.0/24`) with static IP assignments per container.

---

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

---

## Repository Structure

```
Gnode-Platform/
├── ansible/                    # Server provisioning automation
│   ├── inventory/              # Host definitions
│   ├── playbooks/              # bootstrap.yml — full server rebuild
│   ├── roles/                  # docker, networking, security, monitoring
│   └── ansible.cfg
├── apps/                       # Self-hosted applications
│   ├── immich/                 # Photo library
│   ├── nextcloud/              # File sync + collaboration
│   └── vaultwarden/            # Password manager
├── infrastructure/             # Core platform services
│   ├── network/                # NPM + Cloudflare DDNS
│   └── security/               # CrowdSec IPS
├── monitoring/                 # PLG observability stack
│   ├── prometheus/             # Metrics + alerting rules
│   ├── loki/                   # Log storage
│   ├── promtail/               # Log shipping
│   ├── alertmanager/           # Alert routing (Telegram)
│   ├── grafana/                # Dashboards
│   └── exporters/              # Blackbox exporter config
├── bots/                       # Automation bots (in progress)
├── dashboard/                  # Internal DevOps dashboard (separate repo)
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

---

## Services & IP Map

| Service | Container | IP |
|---|---|---|
| Nginx Proxy Manager | `proxy` | `10.5.0.10` |
| Nextcloud DB | `nextcloud-db` | `10.5.0.20` |
| Nextcloud Redis | `nextcloud-redis` | `10.5.0.21` |
| Immich Redis | `immich-redis` | `10.5.0.23` |
| Immich DB | `immich-db` | `10.5.0.24` |
| Immich Server | `immich-server` | `10.5.0.32` |
| Immich ML | `immich-ml` | `10.5.0.33` |
| Vaultwarden | `vaultwarden` | `10.5.0.50` |
| CrowdSec | `crowdsec` | `10.5.0.12` |
| Node Exporter | `node-exporter` | `10.5.0.80` |
| cAdvisor | `cadvisor` | `10.5.0.81` |
| Prometheus | `prometheus` | `10.5.0.82` |
| Loki | `loki` | `10.5.0.83` |
| Promtail | `promtail` | `10.5.0.84` |
| Grafana | `grafana` | `10.5.0.85` |
| Alertmanager | `alertmanager` | `10.5.0.86` |
| Blackbox Exporter | `blackbox` | `10.5.0.87` |

---

## Quick Start

### Prerequisites

- Alpine Linux server (or any Linux distro)
- Docker + Docker Compose installed
- Ansible 2.18+
- age + SOPS installed
- `community.docker` Ansible collection

### 1. Clone the repository

```bash
git clone https://github.com/A-Ghanima/Gnode-Platform.git
cd Gnode-Platform
```

### 2. Set up secrets

```bash
# Generate age key
age-keygen -o ~/.age-key.txt

# Copy and populate .env files
cp apps/nextcloud/.env.example apps/nextcloud/.env
cp apps/immich/.env.example apps/immich/.env
cp apps/vaultwarden/.env.example apps/vaultwarden/.env
cp infrastructure/network/.env.example infrastructure/network/.env
cp monitoring/.env.example monitoring/.env
```

### 3. Create Docker network

```bash
# This is handled automatically by Ansible, but can be run manually
docker network create --driver bridge --subnet 10.5.0.0/24 main_net
```

### 4. Bootstrap the entire platform

```bash
cd ansible
ansible-playbook -i inventory/hosts.yml playbooks/bootstrap.yml
```

This single command will:
- Install and configure Docker
- Create the `main_net` network
- Deploy CrowdSec
- Deploy the full PLG monitoring stack

---

## Secrets Management

All secrets are managed with **SOPS + age**. No plaintext credentials exist in this repository.

- `.env` files are gitignored — copy from `.env.example` and populate locally
- Sensitive values that need to be in Git are encrypted with SOPS before committing
- A **Gitleaks** pre-commit hook blocks any commit containing unencrypted secrets
- The `security-scan.yml` GitHub Actions workflow runs Gitleaks on every push to `main`

---

## CI/CD

| Workflow | Trigger | Purpose |
|---|---|---|
| `yamllint.yml` | Push to `main` | Validates all YAML files |
| `security-scan.yml` | Push to `main` | Scans for leaked secrets (Gitleaks) |
| `trivy.yml` | Push to `main` | CVE scanning for Docker images |

---

## Roadmap

- [ ] Complete `bots/` stack 
- [ ] Add `shellcheck` workflow once shell scripts are added
- [ ] Add Docker build + GHCR publish workflow for custom images
- [ ] Complete documentation (runbooks, disaster recovery, postmortems)

---

## License

MIT © [Ahmed Ghanima](https://github.com/A-Ghanima)
