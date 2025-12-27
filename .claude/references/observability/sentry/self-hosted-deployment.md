---
author: unknown
category: observability
contributors: []
description: Comprehensive deployment guide for self-hosted Sentry with Docker Compose
last_updated: '2025-08-16'
related:
- opentelemetry-best-practices.md
- ../arize/docker-compose-deployment.md
sources:
- name: Sentry Self-Hosted GitHub
  url: https://github.com/getsentry/self-hosted
- name: Sentry Self-Hosted Documentation
  url: https://develop.sentry.dev/self-hosted/
- name: Sentry Release Documentation
  url: https://develop.sentry.dev/self-hosted/releases/
- name: Sentry Configuration Guide
  url: https://develop.sentry.dev/self-hosted/configuration/
- name: Sentry Backup Guide
  url: https://develop.sentry.dev/self-hosted/backup/
- name: Sentry Troubleshooting
  url: https://develop.sentry.dev/self-hosted/troubleshooting/
- name: Sentry Docker Compose
  url: https://github.com/getsentry/self-hosted/blob/master/docker-compose.yml
- name: Sentry SSO Configuration
  url: https://develop.sentry.dev/self-hosted/sso/
- name: Sentry Email Configuration
  url: https://develop.sentry.dev/self-hosted/email/
- name: Sentry Relay Documentation
  url: https://docs.sentry.io/product/relay/
- name: Snuba GitHub Repository
  url: https://github.com/getsentry/snuba
status: stable
subcategory: sentry
tags:
- sentry
- docker
- observability
- error-tracking
- self-hosted
- docker-compose
- monitoring
title: Sentry Self-Hosted Deployment
type: deployment-guide
version: 25.10.0
---

# Sentry Self-Hosted Deployment Guide

Comprehensive guide for deploying and managing self-hosted Sentry error tracking and application monitoring platform using Docker Compose.

## Overview

Sentry self-hosted is "feature-complete and packaged up for low-volume deployments and proofs-of-concept," designed for organizations processing less than approximately 1 million events per month ([GitHub Repository][1]). The deployment uses Docker Compose to orchestrate 40+ microservices including PostgreSQL, Redis, Kafka, ClickHouse, and various processing workers.

**Current Version**: 25.10.0 (October 2025) ([Releases][2])

**License**: Functional Source License (FSL) - free to deploy but cannot resell commercially ([Self-Hosted Docs][3])

---

## System Requirements

Self-hosted Sentry demands substantial resources regardless of traffic volume ([Self-Hosted Docs][3]):

### Minimum Requirements

- **CPU**: 4 cores minimum
- **RAM**: 16 GB + 16 GB swap (32 GB RAM recommended)
- **Disk**: 20 GB free space minimum
- **Docker**: Version 19.03.6 or later
- **Docker Compose**: Version 2.32.2 or later

### Operating System Compatibility

- **Preferred**: Debian/Ubuntu-based distributions
- **Problematic**: RHEL-based systems (CentOS, Rocky Linux, Alma Linux) with SELinux
- **Limited Support**: Amazon Linux 2023
- **Unsupported**: Alpine Linux ([Self-Hosted Docs][3])

---

## Quick Start Installation

### Basic Installation

The standard installation process uses the provided installation script ([Self-Hosted Docs][3]):

```bash
# Clone the repository (latest release recommended)
git clone https://github.com/getsentry/self-hosted.git
cd self-hosted

# Run the installation script
./install.sh

# Start all services
docker compose up --wait
```

**Default Port**: Sentry binds to port 9000 by default ([Self-Hosted Docs][3])

**Access**: http://localhost:9000

### Installation Script Details

The `install.sh` script performs comprehensive setup automation ([Install Script][4]):

**Pre-flight Checks**:
- Validates system environment (rejects MSYS2/Git Bash, recommends WSL)
- Detects Docker Compose version
- Checks minimum system requirements
- Verifies latest commit status

**Configuration Steps**:
- Docker image updates and builds
- ClickHouse database upgrade procedures
- PostgreSQL database migration
- Secret key generation
- Relay credential setup
- Memcached backend verification
- S3 nodestore initialization

**Service Initialization**:
- Creates Docker volumes
- Starts necessary containers
- Runs database migrations
- Initializes Snuba analytics engine
- Configures GeoIP database
- Prepares JavaScript SDK assets

---

## Architecture Overview

### Core Infrastructure Services

Self-hosted Sentry deploys a comprehensive microservices architecture with 40+ containers ([Docker Compose][5]):

#### Database Layer

- **PostgreSQL 14.19**: Primary relational database for configuration, users, organizations, projects ([Docker Compose][5])
- **ClickHouse 25.3.6**: Column-oriented database for events, time-series data, and analytics ([Docker Compose][5])
- **Redis 6.2.20**: Caching layer and temporary data storage ([Docker Compose][5])
- **PgBouncer v1.24.1**: Connection pooling with transaction mode, max 10,000 client connections ([Docker Compose][5])

#### Message Queue

- **Kafka 7.6.6**: Confluent platform with KRaft mode for event streaming ([Docker Compose][5])
  - Multiple listeners: PLAINTEXT, INTERNAL, EXTERNAL, CONTROLLER
  - Single partition topics with 24-hour log retention
  - Handles high-throughput event ingestion

#### Application Services

- **Sentry Web**: Main application server with Django framework, runs on port 9000 ([Docker Compose][5])
- **Relay**: Event ingestion service that acts as "a middle layer between your application and sentry.io" for data privacy and performance ([Relay Docs][6])
- **Nginx 1.29.1**: Reverse proxy listening on configurable `SENTRY_BIND` port ([Docker Compose][5])

#### Analytics & Query Layer

- **Snuba**: "A rich data model on top of Clickhouse together with a fast ingestion consumer and a query optimizer" ([Snuba Repository][7])
  - Provides database connectivity to ClickHouse
  - Implements SnQL query language (SQL-like)
  - Supports multi-tenancy with separate datasets
  - Multiple consumer groups for events, outcomes, transactions, profiles, metrics

#### Storage Services

- **SeaweedFS 3.96**: S3-compatible object storage with master, volume, filer, and S3 gateway roles ([Docker Compose][5])
- **Symbolicator**: Debug symbol resolution with hourly cleanup job ([Docker Compose][5])

#### Task Processing

- **TaskBroker & TaskScheduler**: Distributed task management with SQLite persistence ([Docker Compose][5])
- **TaskWorker**: 4 concurrent workers with health checks ([Docker Compose][5])

#### Specialized Workers

- **Vroom**: Profile and occurrence processing ([Docker Compose][5])
- **Uptime Checker**: Synthetic monitoring with configurable retry logic ([Docker Compose][5])
- **40+ Kafka Consumers**: Specialized consumers for errors, transactions, replays, metrics, profiles, subscriptions ([Docker Compose][5])

### Network Architecture

All services communicate via Docker's internal bridge network. Only Nginx exposes external ports on `SENTRY_BIND` (default: 9000) ([Docker Compose][5]).

### Persistent Volumes

External persistent volumes ([Docker Compose][5]):
- `sentry-data`: Application data and configurations
- `sentry-postgres`: PostgreSQL database files
- `sentry-redis`: Redis persistence
- `sentry-kafka`: Kafka logs and topics
- `sentry-clickhouse`: ClickHouse tables and data
- `sentry-seaweedfs`: Object storage files

---

## Configuration

### Primary Configuration Files

#### 1. sentry/config.yml

Main configuration file generated from `config.example.yml` ([Configuration Guide][8]):

**Key Settings**:
- `system.url-prefix`: "The accessible URL of your self-hosted Sentry installation" ([Configuration Guide][8])
- Mail configuration (`mail.*`)
- Third-party integrations (GitHub, Slack, etc.)

**Example**:
```yaml
system.url-prefix: "https://sentry.example.com"

mail.from: "sentry@example.com"
mail.host: "smtp"
mail.port: 25
mail.username: ""
mail.password: ""
mail.use-tls: false
mail.use-ssl: false

# GitHub App credentials
github-app.id: 123456
github-app.name: "my-sentry-app"
github-app.client-id: "abc123"
github-app.client-secret: "secret123"
github-app.private-key: |
  -----BEGIN RSA PRIVATE KEY-----
  ...
  -----END RSA PRIVATE KEY-----

# Google OAuth
auth-google.client-id: "client-id"
auth-google.client-secret: "client-secret"
```

#### 2. sentry/sentry.conf.py

Advanced configuration parameters beyond basic settings ([Configuration Guide][8]):

**Common Settings**:
```python
# Air-gapped deployment
SENTRY_AIR_GAP = True

# Disable usage reporting beacon
SENTRY_BEACON = False

# Event retention (also configurable via env var)
SENTRY_RETENTION_DAYS = 90

# SSL/TLS settings (prevent CSRF errors behind load balancer)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# GeoIP database path
GEOIP_PATH_MMDB = '/path/to/GeoLite2-City.mmdb'
```

#### 3. .env and .env.custom

Environment variables configuration ([Environment Variables][9]):

**Core Variables**:
- `COMPOSE_PROJECT_NAME`: Docker Compose project name (default: `sentry-self-hosted`)
- `COMPOSE_PROFILES`: Feature sets - `feature-complete` or `errors-only` (default: `feature-complete`)
- `SENTRY_EVENT_RETENTION_DAYS`: Event retention period (default: `90`)
- `SENTRY_BIND`: Port or IP:PORT for Sentry access (default: `9000`)
- `SENTRY_MAIL_HOST`: FQDN for email functionality (must be configured)
- `SENTRY_IMAGE`: Main application image version (default: `nightly`)

**Best Practice**: Create `.env.custom` for system-specific overrides to avoid Git conflicts ([Configuration Guide][8]):

```bash
# .env.custom
SENTRY_BIND=8080
SENTRY_EVENT_RETENTION_DAYS=30
SENTRY_MAIL_HOST=sentry.example.com
SENTRY_IMAGE=ghcr.io/getsentry/sentry:25.10.0
```

**Usage**:
```bash
docker compose --env-file .env.custom up --wait
```

#### 4. sentry/enhance-image.sh

Customizes the Sentry base image for plugins and dependencies ([Configuration Guide][8]):

```bash
#!/bin/bash
# Install custom plugins
pip install sentry-plugins
pip install custom-integration

# Install system dependencies
apt-get update
apt-get install -y custom-package
```

**After modifying, re-run**:
```bash
./install.sh
```

### Important Configuration Notes

Always re-run `./install.sh` after configuration changes rather than `docker compose restart` to ensure migrations and feature toggles apply correctly ([Configuration Guide][8]).

---

## Authentication & SSO

### Supported Authentication Methods

Self-hosted Sentry implements SSO through two approaches ([SSO Configuration][10]):

1. **Middleware proxy authentication**: Upstream proxy determines authenticated user
2. **Third-party service authentication**: External services manage authentication

### OAuth Configuration

#### Google Authentication

Since Sentry 9.1, Google Auth is natively supported ([SSO Configuration][10]):

**Setup**:
1. Obtain OAuth credentials from Google Developer Console
2. Add to `sentry/config.yaml`:

```yaml
auth-google.client-id: "123456789.apps.googleusercontent.com"
auth-google.client-secret: "GOCSPX-abc123..."
```

#### GitHub Authentication

Since Sentry 10, GitHub Auth is built-in ([SSO Configuration][10]):

**Setup**:
1. Create a GitHub App (name cannot contain spaces)
2. Configure URLs: homepage, callback endpoints, webhook settings
3. Request minimal permissions: read-only organization/user data, read/write issues/PRs/webhooks
4. Add to `sentry/config.yaml`:

```yaml
github-app.id: 123456
github-app.name: "sentry-integration"
github-app.client-id: "Iv1.abc123"
github-app.client-secret: "secret123"
github-app.webhook-secret: "webhook-secret"
github-app.private-key: |
  -----BEGIN RSA PRIVATE KEY-----
  ...
  -----END RSA PRIVATE KEY-----
```

### SAML2 Support

"As of Sentry 20.6.0, self-hosted Sentry comes with built-in support for SAML2" authentication ([SSO Configuration][10]). Older versions require manually adding the SAML2 package.

### Post-Configuration

After modifying authentication configuration, rerun the installation script to rebuild and restart containers ([SSO Configuration][10]). Once SSO is enabled, it becomes the exclusive login method unless free registration is also implemented.

---

## Email Configuration

### Built-in SMTP Server

Default configuration uses built-in SMTP powered by exim4 ([Email Configuration][11]):

```yaml
# sentry/config.yml
mail.from: "sentry@example.com"

# .env
SENTRY_MAIL_HOST=sentry.example.com
```

### External SMTP Providers

For production environments, Sentry recommends external SMTP providers due to "various sender requirements implemented by major email providers" ([Email Configuration][11]):

```yaml
# sentry/config.yml
mail.from: "sentry@example.com"
mail.host: "smtp.sendgrid.net"
mail.port: 587
mail.username: "apikey"
mail.password: "SG.your-api-key"
mail.use-tls: true
mail.use-ssl: false
```

**Supported Providers**:
- SendGrid
- AWS SES
- Mailgun
- Postmark
- Any SMTP relay

**Important**: "Because of the way configuration is layered, if you update `mail` settings through the web interface, you will need to also comment out the `mail.host: 'smtp'` default in your `config.yml`" ([Email Configuration][11]).

### Testing Email Delivery

For testing without external SMTP ([Email Configuration][11]):

```yaml
# sentry/config.yml
mail.backend: "console"  # Logs emails instead of sending
```

### Inbound Email

Limited inbound email functionality available exclusively through Mailgun integration ([Email Configuration][11]).

---

## Production Deployment

### Load Balancer Configuration

For production environments, implement ([Self-Hosted Docs][3]):

**Requirements**:
- Dedicated load balancer with SSL/TLS termination
- Forward client IP addresses
- Health checks against `/_health/` endpoint

**Configuration**:
1. Set up load balancer
2. Update `system.url-prefix` in `config.yml`:

```yaml
system.url-prefix: "https://sentry.example.com"
```

3. Configure SSL/TLS settings in `sentry/sentry.conf.py`:

```python
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Proxy Configuration

Enterprise environments requiring HTTP proxies ([Self-Hosted Docs][3]):

**1. System-level proxy** (`/etc/environment`):
```bash
http_proxy=http://proxy.example.com:8080
https_proxy=http://proxy.example.com:8080
no_proxy=localhost,127.0.0.1
```

**2. Docker daemon** (`/etc/systemd/system/docker.service.d/http-proxy.conf`):
```ini
[Service]
Environment="HTTP_PROXY=http://proxy.example.com:8080"
Environment="HTTPS_PROXY=http://proxy.example.com:8080"
Environment="NO_PROXY=localhost,127.0.0.1"
```

**3. Docker client** (`/etc/docker/config.json` or `~/.docker/config.json`):
```json
{
  "proxies": {
    "default": {
      "httpProxy": "http://proxy.example.com:8080",
      "httpsProxy": "http://proxy.example.com:8080",
      "noProxy": "localhost,127.0.0.1"
    }
  }
}
```

### Custom CA Certificates

For services with non-publicly-trusted TLS certificates ([Custom CA Certificates][12]):

**Setup**:
1. Place custom CA certificates in `certificates/` folder at installation root
2. Restart containers

The system automatically runs `update-ca-certificates` during startup. Monitor container logs for certificate issues ([Custom CA Certificates][12]).

**Known Compatibility**: Python libraries (requests, botocore, grpc) configured to use system roots ([Custom CA Certificates][12]).

### Storage Solutions

For disk constraints ([Self-Hosted Docs][3]):

**Options**:
1. Migrate to external storage (AWS S3, Google Cloud Storage)
2. Reduce retention periods via `SENTRY_EVENT_RETENTION_DAYS`
3. Scale disk capacity

---

## Geolocation

### Overview

Sentry uses MaxMind's GeoLite2-City database to map IP addresses to geographic locations ([Geolocation][13]).

### Configuration

**1. Obtain MaxMind credentials** (free account)

**2. Create `geoip/GeoIP.conf`**:
```conf
AccountID YOUR_ACCOUNT_ID
LicenseKey YOUR_LICENSE_KEY
EditionIDs GeoLite2-City
```

**3. Configure services**:

**Relay** (`relay/config.yml`):
```yaml
processing:
  geoip_path: "/geoip/GeoLite2-City.mmdb"
```

**Sentry** (`sentry/sentry.conf.py`):
```python
GEOIP_PATH_MMDB = '/geoip/GeoLite2-City.mmdb'
```

### Important Limitation

"In order to take advantage of server-side IP address geolocation, you must send IP addresses to Sentry" ([Geolocation][13]). Modern SDKs don't transmit IP data by default - explicit configuration required at SDK level.

### Manual Updates

Refresh GeoIP database ([Geolocation][13]):
```bash
./install/geoip.sh
```

---

## Releases & Upgrades

### Release Schedule

Sentry uses **CalVer versioning** with monthly releases on the 15th ([Release Docs][14]):

**Pattern**: YY.MM.patch (e.g., 25.10.0 = October 2025)

**Important**: "CalVer is optimized for continuous deployment, not long-term stability" ([Release Docs][14]). Older versions are not patched; critical bugs may trigger out-of-cycle releases.

**Latest Release**: 25.10.0 (October 15, 2025) ([Releases][2])

### Upgrade Procedure

Standard upgrade path ([Release Docs][14]):

```bash
# 1. Stop services
docker compose down

# 2. Checkout desired version
git fetch --tags
git checkout 25.10.0

# 3. Review configuration changes
# Check sentry/ directory for new settings
# Update .env.custom with new variables

# 4. Run installation script
./install.sh

# 5. Start services
docker compose up --wait
```

**Downtime**: Upgrades cause downtime during service shutdown and data migrations. Experimental `--minimize-downtime` option available ([Release Docs][14]).

### Hard Stops for Incremental Upgrades

When upgrading infrequently, must follow specific path through designated versions with significant database changes ([Release Docs][14]):

**Required hard stops**: 9.1.2, 21.5.0, 21.6.3, 23.6.2, 23.11.0, 24.8.0, 25.5.1

**Example upgrade path** (22.8.0 → 24.2.0):
```bash
22.8.0 → 23.6.2 → 23.11.0 → 24.2.0
```

### Versions to Avoid

- **23.7.0**: Database migration and Django 3 upgrade issues ([Release Docs][14])
- **24.12.0 & 24.12.1**: Login functionality issues (especially hardware 2FA) ([Release Docs][14])

### Breaking Changes

**23.11.0**: Removes `sentry run smtp` worker process ([Release Docs][14])

**24.1.2**: Memcached backend changes from `MemcachedCache` to `PyMemcacheCache` - requires configuration file updates with different OPTIONS API ([Release Docs][14])

---

## Backup & Restore

### Data Categories

Sentry distinguishes between low-volume and high-volume data ([Backup Guide][15]):

**Included in Partial Backups**:
- Global configuration (options, admin accounts, API keys)
- User profiles, organizations, teams, projects
- Alert rules and monitoring configurations

**Excluded**:
- Events and issues (high-volume data)
- External file references

### Partial JSON Backups

Three implementation paths depending on version ([Backup Guide][15]):

**Pre-23.3.0**:
```bash
docker compose run --rm web export
```

**23.3.1+**:
```bash
./scripts/backup.sh
```

**24.1.0+** (Scoped backups):
```bash
# Backup specific scope
./scripts/backup.sh user          # User credentials/permissions
./scripts/backup.sh organization  # Organization-owned data
./scripts/backup.sh config        # Instance-wide settings
./scripts/backup.sh global        # All exportable data
```

### Advanced Scoped Backups (v23.11.1+)

```bash
./sentry-admin.sh export <scope>
```

### Encryption Support

Backups support RSA 2048-bit encryption ([Backup Guide][15]):

**Options**:
- Locally-stored keys
- Google Cloud KMS
- Produces tarball output when encrypted

### Restore Procedures

**Critical Requirement**: "Restore your backup on the **same version of Sentry** on a fresh install (empty database but migrations are run)" to prevent corruption ([Backup Guide][15]).

**Restore command** (version-dependent):
```bash
# Pre-23.3.0
docker compose run --rm web import /path/to/backup.json

# 23.3.1+
./scripts/restore.sh /path/to/backup.json

# 23.11.1+ with encryption
./sentry-admin.sh import --decrypt /path/to/backup.tar.gz
```

### Full Volume Backups

For comprehensive disaster recovery, backup Docker volumes ([Backup Guide][15]):

```bash
# Stop services
docker compose down

# Backup volumes
docker run --rm \
  -v sentry-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/sentry-data.tar.gz -C /data .

docker run --rm \
  -v sentry-postgres:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/sentry-postgres.tar.gz -C /data .

# Repeat for: sentry-redis, sentry-kafka, sentry-clickhouse, sentry-symbolicator

# Restart services
docker compose up -d
```

**Restore volumes**:
```bash
docker compose down

docker run --rm \
  -v sentry-data:/data \
  -v $(pwd):/backup \
  alpine sh -c "rm -rf /data/* && tar xzf /backup/sentry-data.tar.gz -C /data"

docker compose up -d
```

---

## Troubleshooting

### Diagnostic Commands

Self-hosted Sentry is "geared towards low traffic loads (less than ~1 million submitted Sentry events per month)" ([Troubleshooting][16]). Higher volumes require infrastructure expansion or hosted Sentry.

**View service logs** ([Troubleshooting][16]):
```bash
# Specific service
docker compose logs <service_name>

# Follow logs in real-time
docker compose logs -f <service_name>

# With timestamps
docker compose logs -ft <service_name>

# All services
docker compose logs
```

### Common Issues

#### Service Won't Start

**Check logs**:
```bash
docker compose logs <service_name>
```

**Common causes**:
- Port conflicts: Change `SENTRY_BIND` in `.env`
- Volume permissions: Ensure write access
- Insufficient resources: Check `docker stats`

#### Database Connection Errors

**PostgreSQL not ready**:
```yaml
# docker-compose.yml
services:
  web:
    depends_on:
      postgres:
        condition: service_healthy
```

**Connection string format**:
```bash
# Correct
postgresql://user:password@host:5432/database

# Incorrect
postgres://user:password@host:5432/database
```

#### Events Not Appearing

**Check Relay connectivity**:
```bash
curl http://localhost:9000/_health/
```

**Verify DSN configuration in SDK**:
```python
import sentry_sdk

sentry_sdk.init(
    dsn="http://public@localhost:9000/1",
    traces_sample_rate=1.0,
)
```

#### Performance Issues

**Check resource usage**:
```bash
docker stats
```

**Increase container limits**:
```yaml
services:
  web:
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: "2.0"
```

**Scale workers**:
```bash
docker compose up -d --scale worker=4
```

#### Email Not Sending

**Test SMTP configuration**:
```bash
docker compose exec web sentry sendmail
```

**Check logs**:
```bash
docker compose logs smtp
```

### Component-Specific Troubleshooting

Dedicated troubleshooting documentation exists for ([Troubleshooting][16]):
- Sentry core application
- Kafka message broker
- Docker containerization
- PostgreSQL database
- Redis caching layer

---

## Getting Support

### Support Policy

Sentry **does not** provide dedicated support for self-hosted deployments ([Support][17]). No paid support options exist.

### Community Support Channels

#### GitHub Issues

**For setup questions**: File issue on [self-hosted repository](https://github.com/getsentry/self-hosted/issues) ([Support][17])

**For missing docs, bugs, installation problems**: "[File an issue](https://github.com/getsentry/self-hosted/issues/new/choose) for missing docs, bugs during upgrades or installation" ([Support][17])

**For functionality issues**: Report broken authentication, non-working features to [main Sentry repository](https://github.com/getsentry/sentry/issues) ([Support][17])

#### Discord Community

Join the Sentry Community Discord server's #self-hosted channel for peer support. Sentry employees monitor and contribute when available ([Troubleshooting][16]).

### Contributing

"[Submit PRs](https://github.com/getsentry/self-hosted/compare) directly for simple fixes" ([Support][17])

### Before Seeking Help

Review the [troubleshooting section](https://develop.sentry.dev/self-hosted/troubleshooting/) ([Support][17]) and check existing GitHub issues.

---

## Limitations vs SaaS

Self-hosted deployments lack ([Self-Hosted Docs][3]):

**Business Features**:
- Billing system and pricing tiers
- Spike protection and spend allocation

**AI/ML Features**:
- Seer (AI-powered features)

**Platform Support**:
- Complete mobile symbolication support
- Gaming platform integrations (PlayStation, Nintendo Switch)

**Scale**:
- Optimized for <1M events/month
- No automatic scaling

---

## SDK Integration

### Supported Platforms

Sentry captures application data "using an SDK within your application's runtime" ([SDK Platforms][18]). SDKs connect to self-hosted instances through DSN configuration.

**Major Languages** ([SDK Platforms][18]):
- **Web/JavaScript**: Next.js, React, Node.js, Angular, Vue
- **Backend**: Python, PHP (Laravel), Go, Java, Kotlin, Ruby, Rust, .NET, Elixir
- **Mobile**: Android, iOS (Apple), React Native, Flutter (Dart)
- **Game Engines**: Unity, Unreal Engine, Godot, Xbox
- **Other**: C/C++ (Native), PowerShell, Clojure, Crystal, Lua

### Configuration Example

**Python**:
```python
import sentry_sdk

sentry_sdk.init(
    dsn="http://public@sentry.example.com:9000/1",
    environment="production",
    release="my-app@1.0.0",
    traces_sample_rate=0.1,
    profiles_sample_rate=0.1,
)
```

**JavaScript**:
```javascript
import * as Sentry from "@sentry/browser";

Sentry.init({
  dsn: "http://public@sentry.example.com:9000/1",
  environment: "production",
  release: "my-app@1.0.0",
  tracesSampleRate: 0.1,
});
```

### Important Notes

- Third-party libraries shouldn't embed Sentry SDKs (version conflicts, signal handler interference) ([SDK Platforms][18])
- Avoid using Sentry alongside competing APM tools ([SDK Platforms][18])

---

## Production Deployment Checklist

### Security

- [ ] Pin Docker image versions (not `nightly` or `latest`)
- [ ] Change default database passwords
- [ ] Configure `system.url-prefix` with production URL
- [ ] Set up SSL/TLS termination at load balancer
- [ ] Configure SSL/TLS settings in `sentry.conf.py`
- [ ] Enable authentication (SSO/SAML)
- [ ] Restrict network access to services
- [ ] Use environment secrets management
- [ ] Configure CSRF trusted origins
- [ ] Set up custom CA certificates if needed

### Data Management

- [ ] Configure event retention (`SENTRY_EVENT_RETENTION_DAYS`)
- [ ] Set up automated database backups
- [ ] Test backup restoration procedures
- [ ] Configure external storage (S3) for large deployments
- [ ] Plan disk capacity for event volume

### Email & Notifications

- [ ] Configure external SMTP provider
- [ ] Test email delivery
- [ ] Set up alert rules and notifications
- [ ] Configure integrations (Slack, PagerDuty)

### Monitoring

- [ ] Configure health checks at load balancer (`/_health/`)
- [ ] Set up log aggregation
- [ ] Monitor disk usage
- [ ] Monitor resource utilization (CPU, memory)
- [ ] Track event ingestion rates

### High Availability

- [ ] Use external PostgreSQL (RDS, Cloud SQL)
- [ ] Configure PostgreSQL replication
- [ ] Plan for horizontal scaling
- [ ] Set up load balancing
- [ ] Configure resource limits
- [ ] Implement automated backups

### Operations

- [ ] Document deployment procedures
- [ ] Set up CI/CD for updates
- [ ] Plan upgrade strategy (hard stops)
- [ ] Establish incident response procedures
- [ ] Train team on troubleshooting

---

## Environment Variables Reference

Complete list from `.env` file ([Environment Variables][9]):

### Core Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `COMPOSE_PROJECT_NAME` | Docker Compose project name | `sentry-self-hosted` |
| `COMPOSE_PROFILES` | Feature sets: `feature-complete` or `errors-only` | `feature-complete` |
| `SENTRY_EVENT_RETENTION_DAYS` | Event retention period | `90` |
| `SENTRY_BIND` | Port or IP:PORT for Sentry access | `9000` |
| `SENTRY_MAIL_HOST` | FQDN for email functionality | None (required) |

### Container Images

| Variable | Description | Default |
|----------|-------------|---------|
| `SENTRY_IMAGE` | Main application image | `ghcr.io/getsentry/sentry:nightly` |
| `SNUBA_IMAGE` | Analytics backend | `ghcr.io/getsentry/snuba:nightly` |
| `RELAY_IMAGE` | Event relay service | `ghcr.io/getsentry/relay:nightly` |
| `SYMBOLICATOR_IMAGE` | Symbol processing | `ghcr.io/getsentry/symbolicator:nightly` |
| `TASKBROKER_IMAGE` | Task management | `ghcr.io/getsentry/taskbroker:nightly` |
| `VROOM_IMAGE` | Additional service | `ghcr.io/getsentry/vroom:nightly` |
| `UPTIME_CHECKER_IMAGE` | Monitoring service | `ghcr.io/getsentry/uptime-checker:nightly` |

### Health Check Settings

Multiple variables configure service health monitoring with sensible production defaults ([Environment Variables][9]).

### Feature Flags

| Variable | Description | Default |
|----------|-------------|---------|
| `SETUP_JS_SDK_ASSETS` | Enable JavaScript SDK asset configuration | Disabled |

---

## Additional Resources

### Official Documentation

- [Sentry Documentation](https://docs.sentry.io/)
- [Self-Hosted Documentation](https://develop.sentry.dev/self-hosted/)
- [Self-Hosted GitHub Repository](https://github.com/getsentry/self-hosted)
- [Release Notes](https://github.com/getsentry/self-hosted/releases)
- [Configuration Guide](https://develop.sentry.dev/self-hosted/configuration/)
- [Backup & Restore](https://develop.sentry.dev/self-hosted/backup/)
- [Troubleshooting](https://develop.sentry.dev/self-hosted/troubleshooting/)

### Community

- [Sentry Community Discord](https://discord.gg/sentry)
- [GitHub Issues](https://github.com/getsentry/self-hosted/issues)
- [GitHub Discussions](https://github.com/getsentry/sentry/discussions)

### Related Technologies

- [Relay Documentation](https://docs.sentry.io/product/relay/)
- [Snuba Repository](https://github.com/getsentry/snuba)
- [ClickHouse Documentation](https://clickhouse.com/docs)
- [Kafka Documentation](https://kafka.apache.org/documentation/)

---

## References

[1]: https://github.com/getsentry/self-hosted "Sentry Self-Hosted GitHub Repository"
[2]: https://github.com/getsentry/self-hosted/releases "Sentry Self-Hosted Releases"
[3]: https://develop.sentry.dev/self-hosted/ "Sentry Self-Hosted Documentation"
[4]: https://github.com/getsentry/self-hosted/blob/master/install.sh "Sentry Installation Script"
[5]: https://github.com/getsentry/self-hosted/blob/master/docker-compose.yml "Sentry Docker Compose Configuration"
[6]: https://docs.sentry.io/product/relay/ "Sentry Relay Documentation"
[7]: https://github.com/getsentry/snuba "Snuba GitHub Repository"
[8]: https://develop.sentry.dev/self-hosted/configuration/ "Sentry Configuration Guide"
[9]: https://github.com/getsentry/self-hosted/blob/master/.env "Sentry Environment Variables"
[10]: https://develop.sentry.dev/self-hosted/sso/ "Sentry SSO Configuration"
[11]: https://develop.sentry.dev/self-hosted/email/ "Sentry Email Configuration"
[12]: https://develop.sentry.dev/self-hosted/custom-ca-roots/ "Sentry Custom CA Certificates"
[13]: https://develop.sentry.dev/self-hosted/geolocation/ "Sentry Geolocation Setup"
[14]: https://develop.sentry.dev/self-hosted/releases/ "Sentry Release Documentation"
[15]: https://develop.sentry.dev/self-hosted/backup/ "Sentry Backup Guide"
[16]: https://develop.sentry.dev/self-hosted/troubleshooting/ "Sentry Troubleshooting"
[17]: https://develop.sentry.dev/self-hosted/support/ "Sentry Support Information"
[18]: https://docs.sentry.io/platforms/ "Sentry SDK Platforms"