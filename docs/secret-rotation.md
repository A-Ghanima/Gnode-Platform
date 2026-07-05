# Runbook: Secret rotation

Use this when a secret is compromised, expired, or needs to be rotated as part of routine maintenance.

---

## Types of secrets in this repo

| Secret type | Where it lives | How it's managed |
|---|---|---|
| Service passwords (DB, admin) | `.env` files | Gitignored, populated manually |
| API tokens (Cloudflare, Telegram) | `.env` files | Gitignored, populated manually |
| Encrypted secrets (e.g. Vaultwarden domain) | `secrets.enc.yaml` | Encrypted with SOPS + age, committed to Git |
| age private key | `~/.age-key.txt` | Never committed, stored only on server |

---

## Rotating a `.env` secret

### 1. Update the value in the `.env` file

```bash
nano /root/Gnode/apps/<service>/.env
```

Change the relevant variable to the new value.

### 2. Restart the affected service

```bash
cd /root/Gnode/apps/<service>
docker compose up -d
```

Docker Compose re-reads the `.env` file on `up`. A restart is enough; you don't need to recreate the container unless the variable is baked into an image build.

### 3. Verify the service is healthy

```bash
docker ps | grep <container-name>
docker logs <container-name> --tail 20
```

---

## Rotating a SOPS-encrypted secret

### 1. Decrypt the file

```bash
export SOPS_AGE_KEY_FILE=~/.age-key.txt
sops --decrypt apps/vaultwarden/secrets.enc.yaml > /tmp/secrets.yaml
```

### 2. Edit the decrypted file

```bash
nano /tmp/secrets.yaml
```

Update the value.

### 3. Re-encrypt and replace the original

```bash
sops --encrypt /tmp/secrets.yaml > apps/vaultwarden/secrets.enc.yaml
rm /tmp/secrets.yaml
```

### 4. Commit the updated encrypted file

```bash
git add apps/vaultwarden/secrets.enc.yaml
git commit -m "chore: rotate <secret-name>"
git push
```

The Gitleaks pre-commit hook will scan the staged file. If it fires, the plaintext version leaked somewhere — check `/tmp` and your shell history.

---

## Rotating the age key

Only do this if the private key at `~/.age-key.txt` is compromised or lost.

### 1. Generate a new key

```bash
age-keygen -o ~/.age-key-new.txt
```

Note the new public key printed to stdout.

### 2. Update `.sops.yaml`

```bash
nano /root/Gnode/.sops.yaml
```

Replace the old `age` public key with the new one.

### 3. Re-encrypt all SOPS files with the new key

For each encrypted file in the repo:

```bash
export SOPS_AGE_KEY_FILE=~/.age-key.txt  # old key, still needed to decrypt

sops --decrypt apps/vaultwarden/secrets.enc.yaml > /tmp/s.yaml

export SOPS_AGE_KEY_FILE=~/.age-key-new.txt  # new key for re-encryption
sops --encrypt /tmp/s.yaml > apps/vaultwarden/secrets.enc.yaml

rm /tmp/s.yaml
```

Repeat for every `*.enc.yaml` file.

### 4. Replace the old key file

```bash
mv ~/.age-key-new.txt ~/.age-key.txt
chmod 600 ~/.age-key.txt
```

### 5. Commit and push

```bash
git add .sops.yaml apps/**/secrets.enc.yaml
git commit -m "chore: rotate age encryption key"
git push
```

---

## After any rotation

Check Grafana and Alertmanager are still receiving data. A wrong Telegram bot token will silently break alerting — send a test alert to confirm:

```bash
curl -X POST http://10.5.0.86/-/reload
```

Then trigger a test alert or check the Alertmanager UI at `http://10.5.0.86:9093`.
