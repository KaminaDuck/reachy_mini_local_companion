---
author: unknown
category: deployment
contributors: []
description: Production-ready Phoenix deployment with Docker Compose and PostgreSQL
last_updated: '2025-11-01'
related:
- span-kinds-reference.md
- tracing-links.md
- ../../python/pydantic-ai/phoenix-integration.md
- opentelemetry-best-practices.md
- semantic-conventions.md
sources:
- name: Phoenix Documentation
  url: https://arize.com/docs/phoenix
- name: Phoenix Docker Hub
  url: https://hub.docker.com/r/arizephoenix/phoenix
status: stable
subcategory: docker
tags:
- docker
- postgres
- observability
- phoenix
- deployment
- docker-compose
- arize
title: Phoenix Docker Compose Deployment
type: deployment-guide
version: '1.0'
---

# Arize Phoenix Docker Compose Deployment Reference

This guide provides complete configuration options, deployment patterns, and best practices for running Arize Phoenix using Docker Compose.

## Quick Start

### Prerequisites

- Docker Engine and Docker Compose installed
- Verify installation: `docker info`
- For production: External PostgreSQL or persistent volumes

### Minimal Deployment

```bash
# Pull the latest Phoenix image
docker pull arizephoenix/phoenix:latest

# Run Phoenix standalone
docker run -p 6006:6006 -p 4317:4317 arizephoenix/phoenix:latest
```

Access UI: http://localhost:6006

---

## Docker Image Information

**Docker Hub:** https://hub.docker.com/r/arizephoenix/phoenix

### Image Tags

- `latest` - Latest stable release (recommended for testing)
- `nightly` - Nightly builds with latest features
- `12.9.0`, `12.8.0`, `12.7.1`, etc. - Specific version pins (recommended for production)
- `12.9.0-nonroot`, `12.9.0-debug` - Variant tags for specific use cases

### Architecture Support

- `amd64` (x86_64) - Default
- `arm64` - For Apple Silicon, Raspberry Pi (use base image: `gcr.io/distroless/python3-debian12:nonroot-arm64`)

**Production Recommendation:** Always pin to a specific version tag
```yaml
image: arizephoenix/phoenix:12.9.0  # Not 'latest'
```

---

## Port Configuration

Phoenix exposes three ports by default:

| Port | Protocol | Endpoint | Function | Environment Variable |
|------|----------|----------|----------|---------------------|
| 6006 | HTTP | `/` | Web UI | `PHOENIX_PORT` |
| 6006 | HTTP | `/v1/traces` | OTLP HTTP collector (Protobuf) | `PHOENIX_PORT` |
| 4317 | gRPC | n/a | OTLP gRPC collector (Protobuf) | `PHOENIX_GRPC_PORT` |
| 9090 | HTTP | `/metrics` | Prometheus metrics (optional) | `PHOENIX_ENABLE_PROMETHEUS=true` |

**Port Mapping Example:**
```yaml
ports:
  - "6006:6006"  # UI and HTTP collector
  - "4317:4317"  # gRPC collector
  - "9090:9090"  # Prometheus metrics (if enabled)
```

---

## Deployment Patterns

### 1. PostgreSQL Backend (Recommended for Production)

**File:** `docker-compose.yml`

```yaml
services:
  phoenix:
    image: arizephoenix/phoenix:12.9.0  # Pin version for production
    depends_on:
      - db
    ports:
      - "6006:6006"  # HTTP UI and collector
      - "4317:4317"  # gRPC collector
      - "9090:9090"  # Prometheus (optional)
    environment:
      - PHOENIX_SQL_DATABASE_URL=postgresql://postgres:secure_password@db:5432/phoenix
      # Optional: Enable Prometheus metrics
      - PHOENIX_ENABLE_PROMETHEUS=true
      # Optional: Configure retention policy
      - PHOENIX_DEFAULT_RETENTION_POLICY_DAYS=30
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=secure_password  # Change this!
      - POSTGRES_DB=phoenix
      - POSTGRES_INITDB_ARGS=--data-checksums
    ports:
      - "5432:5432"  # Expose for external access (optional)
    volumes:
      - phoenix_db:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d phoenix"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s

volumes:
  phoenix_db:
    driver: local
```

**Start:**
```bash
docker compose up -d
```

**Access:** http://localhost:6006

---

### 2. SQLite with Persistent Volume

Suitable for development or single-instance deployments.

```yaml
services:
  phoenix:
    image: arizephoenix/phoenix:12.9.0
    ports:
      - "6006:6006"
      - "4317:4317"
    environment:
      - PHOENIX_WORKING_DIR=/mnt/data
    volumes:
      - phoenix_data:/mnt/data
    restart: unless-stopped

volumes:
  phoenix_data:
    driver: local
```

**Notes:**
- SQLite stored in `/mnt/data/phoenix.db`
- Not recommended for high-concurrency workloads
- Simpler setup, no separate database service

---

### 3. Phoenix as Sidecar with Application

Full-stack example with Phoenix collecting traces from a backend service.

```yaml
services:
  phoenix:
    image: arizephoenix/phoenix:12.9.0
    ports:
      - "6006:6006"  # UI
      - "4317:4317"  # gRPC collector
    environment:
      - PHOENIX_SQL_DATABASE_URL=postgresql://postgres:password@db:5432/phoenix
    depends_on:
      - db

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - COLLECTOR_ENDPOINT=http://phoenix:6006/v1/traces
      - PHOENIX_COLLECTOR_ENDPOINT=http://phoenix:6006
    depends_on:
      - phoenix
    healthcheck:
      test: ["CMD", "wget", "--spider", "http://0.0.0.0:8000/health"]
      interval: 5s
      timeout: 1s
      retries: 5

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      backend:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=phoenix
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

**Application Code (Python):**
```python
import os
from phoenix.otel import register

# Phoenix automatically reads PHOENIX_COLLECTOR_ENDPOINT
tracer_provider = register(
    project_name="my-app",
    endpoint=os.getenv("COLLECTOR_ENDPOINT", "http://localhost:6006/v1/traces")
)
```

---

### 4. Development Setup with OIDC and SMTP

Advanced setup with authentication, email, and monitoring.

```yaml
services:
  phoenix:
    image: arizephoenix/phoenix:12.9.0
    depends_on:
      - db
      - oidc-provider
      - smtp-server
    ports:
      - "6006:6006"
      - "4317:4317"
      - "9090:9090"
    environment:
      # Database
      - PHOENIX_SQL_DATABASE_URL=postgresql://postgres:postgres@db:5432/phoenix

      # Server
      - PHOENIX_LOG_LEVEL=INFO
      - PHOENIX_ENABLE_PROMETHEUS=true

      # Authentication
      - PHOENIX_ENABLE_AUTH=true
      - PHOENIX_SECRET=your-secret-key-min-32-chars-long
      - PHOENIX_ADMIN_SECRET=your-admin-secret
      - PHOENIX_USE_SECURE_COOKIES=true
      - PHOENIX_CSRF_TRUSTED_ORIGINS=http://localhost:6006

      # OIDC (OAuth2)
      - PHOENIX_OAUTH2_DEV_CLIENT_ID=phoenix-client-id
      - PHOENIX_OAUTH2_DEV_CLIENT_SECRET=phoenix-client-secret
      - PHOENIX_OAUTH2_DEV_OIDC_CONFIG_URL=http://oidc-provider:9000/.well-known/openid-configuration
      - PHOENIX_OAUTH2_DEV_DISPLAY_NAME=SSO Login
      - PHOENIX_OAUTH2_DEV_ALLOW_SIGN_UP=true

      # SMTP
      - PHOENIX_SMTP_HOSTNAME=smtp-server
      - PHOENIX_SMTP_PORT=1025
      - PHOENIX_SMTP_USERNAME=dev
      - PHOENIX_SMTP_PASSWORD=dev
      - PHOENIX_SMTP_MAIL_FROM=noreply@phoenix.local
      - PHOENIX_SMTP_VALIDATE_CERTS=false

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=phoenix
    volumes:
      - db_data:/var/lib/postgresql/data

  oidc-provider:
    image: # Your OIDC provider image
    ports:
      - "9000:9000"

  smtp-server:
    image: mailhog/mailhog
    ports:
      - "1025:1025"  # SMTP
      - "8025:8025"  # Web UI

volumes:
  db_data:
```

---

## Environment Variables Reference

### Server Configuration

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `PHOENIX_PORT` | HTTP server port (UI + OTLP HTTP) | `6006` | `8080` |
| `PHOENIX_GRPC_PORT` | gRPC OTLP collector port | `4317` | `4318` |
| `PHOENIX_HOST` | Server bind address | `0.0.0.0` | `127.0.0.1` |
| `PHOENIX_HOST_ROOT_PATH` | Reverse proxy subpath prefix | None | `/phoenix` |
| `PHOENIX_ROOT_URL` | Full public URL for Phoenix | None | `https://phoenix.example.com` |
| `PHOENIX_WORKING_DIR` | Data directory for SQLite and temp files | `~/.phoenix/` | `/mnt/data` |
| `PHOENIX_ALLOW_EXTERNAL_RESOURCES` | Load external resources (fonts, etc.) | `true` | `false` |
| `PHOENIX_LOG_LEVEL` | Logging verbosity | `INFO` | `DEBUG`, `WARNING`, `ERROR` |

### Database Configuration

| Variable | Description | Example |
|----------|-------------|---------|
| `PHOENIX_SQL_DATABASE_URL` | Complete database connection URL | `postgresql://user:pass@host:5432/db` |
| `PHOENIX_POSTGRES_HOST` | PostgreSQL hostname (alternative to URL) | `postgres-server` |
| `PHOENIX_POSTGRES_PORT` | PostgreSQL port | `5432` |
| `PHOENIX_POSTGRES_USER` | PostgreSQL username | `phoenix_user` |
| `PHOENIX_POSTGRES_PASSWORD` | PostgreSQL password | `secure_password` |
| `PHOENIX_POSTGRES_DB` | PostgreSQL database name | `phoenix` |
| `PHOENIX_SQL_DATABASE_SCHEMA` | PostgreSQL schema (optional) | `phoenix_schema` |

**PostgreSQL URL Formats:**
```bash
# With user/password in URL
postgresql://username:password@hostname:5432/database

# With parameters
postgresql://@hostname/database?user=username&password=password

# SQLite (for reference)
sqlite:///path/to/database.db
```

**PostgreSQL Version Support:** ≥ 14

### Data Retention

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `PHOENIX_DEFAULT_RETENTION_POLICY_DAYS` | Auto-delete traces older than N days | `0` (infinite) | `30`, `90` |

**Note:** Can be overridden per-project in Phoenix UI.

### Authentication

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `PHOENIX_ENABLE_AUTH` | Enable authentication system | No | `true`, `false` |
| `PHOENIX_SECRET` | JWT signing secret (min 32 chars) | Yes (if auth enabled) | `3413f9a7735bb780c6b8e4db7d946a49...` |
| `PHOENIX_ADMIN_SECRET` | Admin API secret | No | Long random string |
| `PHOENIX_USE_SECURE_COOKIES` | Use secure cookies (HTTPS only) | No | `true` |
| `PHOENIX_DISABLE_BASIC_AUTH` | Disable username/password login | No | `true` |
| `PHOENIX_CSRF_TRUSTED_ORIGINS` | Comma-separated CSRF trusted origins | No | `https://app.example.com,https://api.example.com` |
| `PHOENIX_DEFAULT_ADMIN_INITIAL_PASSWORD` | Default admin password on first start | No | `admin` (default) |
| `PHOENIX_ADMINS` | Predefined admin users | No | `Admin=admin@example.com` |

**Default Admin:**
- Email: `admin@localhost`
- Password: `admin` (or `PHOENIX_DEFAULT_ADMIN_INITIAL_PASSWORD`)

### OAuth2/OIDC Integration

Phoenix supports third-party identity providers (Google, Auth0, Okta, custom OIDC).

| Variable | Description | Example |
|----------|-------------|---------|
| `PHOENIX_OAUTH2_<NAME>_CLIENT_ID` | OAuth2 client ID | `phoenix-client-id` |
| `PHOENIX_OAUTH2_<NAME>_CLIENT_SECRET` | OAuth2 client secret | `secret-abc-123` |
| `PHOENIX_OAUTH2_<NAME>_OIDC_CONFIG_URL` | OIDC discovery URL | `https://accounts.google.com/.well-known/openid-configuration` |
| `PHOENIX_OAUTH2_<NAME>_DISPLAY_NAME` | Login button text | `Login with Google` |
| `PHOENIX_OAUTH2_<NAME>_ALLOW_SIGN_UP` | Allow new user registration | `true`, `false` |
| `PHOENIX_OAUTH2_<NAME>_AUTO_LOGIN` | Auto-redirect to OAuth | `true`, `false` |

**Note:** Replace `<NAME>` with provider identifier (e.g., `GOOGLE`, `AUTH0`, `DEV`).

**Example (Google OAuth):**
```yaml
environment:
  - PHOENIX_OAUTH2_GOOGLE_CLIENT_ID=123456789.apps.googleusercontent.com
  - PHOENIX_OAUTH2_GOOGLE_CLIENT_SECRET=GOCSPX-abc123...
  - PHOENIX_OAUTH2_GOOGLE_OIDC_CONFIG_URL=https://accounts.google.com/.well-known/openid-configuration
  - PHOENIX_OAUTH2_GOOGLE_DISPLAY_NAME=Sign in with Google
  - PHOENIX_OAUTH2_GOOGLE_ALLOW_SIGN_UP=true
```

### SMTP Configuration

Required for password resets and user invitations when authentication is enabled.

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `PHOENIX_SMTP_HOSTNAME` | SMTP server hostname | None | `smtp.sendgrid.net` |
| `PHOENIX_SMTP_PORT` | SMTP server port | `587` | `465`, `25` |
| `PHOENIX_SMTP_USERNAME` | SMTP authentication username | None | `apikey` |
| `PHOENIX_SMTP_PASSWORD` | SMTP authentication password | None | Your API key |
| `PHOENIX_SMTP_MAIL_FROM` | From email address | `noreply@arize.com` | `noreply@yourdomain.com` |
| `PHOENIX_SMTP_VALIDATE_CERTS` | Validate SSL certificates | `true` | `false` |

**Example (SendGrid):**
```yaml
environment:
  - PHOENIX_SMTP_HOSTNAME=smtp.sendgrid.net
  - PHOENIX_SMTP_PORT=587
  - PHOENIX_SMTP_USERNAME=apikey
  - PHOENIX_SMTP_PASSWORD=SG.your_api_key_here
  - PHOENIX_SMTP_MAIL_FROM=noreply@yourdomain.com
```

**Recommended Providers:**
- SendGrid
- Mailgun
- Postmark
- Resend
- AWS SES

### Monitoring & Observability

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `PHOENIX_ENABLE_PROMETHEUS` | Enable Prometheus metrics endpoint | `false` | `true` |
| `PHOENIX_SERVER_INSTRUMENTATION_OTLP_TRACE_COLLECTOR_HTTP_ENDPOINT` | Send Phoenix's own traces (HTTP) | None | `http://otel-collector:4318/v1/traces` |
| `PHOENIX_SERVER_INSTRUMENTATION_OTLP_TRACE_COLLECTOR_GRPC_ENDPOINT` | Send Phoenix's own traces (gRPC) | None | `otel-collector:4317` |

**Prometheus Metrics:**
When enabled, metrics available at `http://phoenix:9090/metrics`

---

## API Keys and Authentication

### Creating API Keys

After enabling authentication:

1. Login as admin: `admin@localhost` / `admin`
2. Navigate to Settings → API Keys
3. Create System API Key (for programmatic access)

### Using API Keys

**Environment Variable:**
```bash
export PHOENIX_API_KEY=your-system-or-user-key
```

**Python Client:**
```python
from phoenix.otel import register

# PHOENIX_API_KEY is read automatically
tracer_provider = register(
    project_name="my-app",
    endpoint="http://phoenix:6006/v1/traces"
)
```

**Manual Authorization Header:**
```python
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

exporter = OTLPSpanExporter(
    endpoint="http://phoenix:6006/v1/traces",
    headers={"authorization": "Bearer your-api-key"}  # lowercase!
)
```

**Important:** Use lowercase `authorization` for gRPC compatibility.

### API Key Types

- **System Keys:** Act on behalf of the system, created by admins, persist across user deletions
- **User Keys:** Associated with specific users, deleted when user is deleted

---

## Resource Limits and Performance Tuning

### Docker Compose Resource Limits

```yaml
services:
  phoenix:
    image: arizephoenix/phoenix:12.9.0
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: "2.0"
        reservations:
          memory: 1G
          cpus: "1.0"

  db:
    image: postgres:16-alpine
    command: |
      postgres
      -c shared_preload_libraries=pg_stat_statements
      -c max_connections=200
      -c shared_buffers=256MB
      -c effective_cache_size=1GB
      -c maintenance_work_mem=64MB
      -c checkpoint_completion_target=0.9
      -c wal_buffers=16MB
      -c default_statistics_target=100
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: "1.0"
```

### PostgreSQL Tuning Recommendations

**For 4GB RAM server:**
```yaml
command: |
  postgres
  -c shared_buffers=1GB
  -c effective_cache_size=3GB
  -c maintenance_work_mem=256MB
  -c max_connections=100
```

**For 16GB RAM server:**
```yaml
command: |
  postgres
  -c shared_buffers=4GB
  -c effective_cache_size=12GB
  -c maintenance_work_mem=1GB
  -c max_connections=200
```

---

## Reverse Proxy Configuration

Running Phoenix behind Traefik, Nginx, or another reverse proxy.

### Traefik Example

```yaml
services:
  traefik:
    image: traefik:v3.1
    command:
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
    ports:
      - "80:80"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro

  phoenix:
    image: arizephoenix/phoenix:12.9.0
    environment:
      - PHOENIX_HOST_ROOT_PATH=/phoenix
      - PHOENIX_ROOT_URL=http://localhost/phoenix
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.phoenix.rule=PathPrefix(`/phoenix`)"
      - "traefik.http.services.phoenix.loadbalancer.server.port=6006"
      - "traefik.http.middlewares.phoenix-strip.stripprefix.prefixes=/phoenix"
      - "traefik.http.routers.phoenix.middlewares=phoenix-strip"
```

**Access:** http://localhost/phoenix

### Nginx Configuration

**nginx.conf:**
```nginx
location /phoenix/ {
    proxy_pass http://phoenix:6006/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

**Phoenix Environment:**
```yaml
environment:
  - PHOENIX_HOST_ROOT_PATH=/phoenix
  - PHOENIX_ROOT_URL=https://yourdomain.com/phoenix
```

---

## Production Deployment Checklist

### Security

- [ ] Pin Docker image to specific version (not `latest`)
- [ ] Change default PostgreSQL password
- [ ] Enable authentication (`PHOENIX_ENABLE_AUTH=true`)
- [ ] Set strong `PHOENIX_SECRET` (min 32 chars, random)
- [ ] Use secure cookies (`PHOENIX_USE_SECURE_COOKIES=true`) with HTTPS
- [ ] Configure CSRF trusted origins
- [ ] Use environment secrets management (not hardcoded)
- [ ] Restrict network access to PostgreSQL
- [ ] Enable SSL/TLS for PostgreSQL connections

### Data Persistence

- [ ] Use external PostgreSQL (not SQLite)
- [ ] Configure automated database backups
- [ ] Use persistent volumes for PostgreSQL data
- [ ] Set retention policy (`PHOENIX_DEFAULT_RETENTION_POLICY_DAYS`)
- [ ] Monitor disk usage

### Monitoring

- [ ] Enable Prometheus metrics
- [ ] Set up alerting (disk space, memory, CPU)
- [ ] Configure log aggregation
- [ ] Monitor trace ingestion rates
- [ ] Set up database performance monitoring

### High Availability

- [ ] Use PostgreSQL cluster or managed service (RDS, Cloud SQL)
- [ ] Run multiple Phoenix replicas behind load balancer
- [ ] Configure health checks
- [ ] Set resource limits and auto-scaling
- [ ] Use external SMTP service for reliability

### Operations

- [ ] Document deployment procedures
- [ ] Set up CI/CD for updates
- [ ] Plan for zero-downtime deployments
- [ ] Configure automated backups and test restoration
- [ ] Establish incident response procedures

---

## Common Use Cases

### Minimal Development Setup

```yaml
# docker-compose.dev.yml
services:
  phoenix:
    image: arizephoenix/phoenix:latest
    ports:
      - "6006:6006"
      - "4317:4317"
    environment:
      - PHOENIX_WORKING_DIR=/data
    volumes:
      - ./phoenix-data:/data
```

**Start:** `docker compose -f docker-compose.dev.yml up`

### Production with External Postgres

```yaml
# docker-compose.prod.yml
services:
  phoenix:
    image: arizephoenix/phoenix:12.9.0
    ports:
      - "6006:6006"
      - "4317:4317"
      - "9090:9090"
    environment:
      - PHOENIX_SQL_DATABASE_URL=postgresql://phoenix_user:${DB_PASSWORD}@postgres.example.com:5432/phoenix_prod
      - PHOENIX_ENABLE_AUTH=true
      - PHOENIX_SECRET=${PHOENIX_SECRET}
      - PHOENIX_ENABLE_PROMETHEUS=true
      - PHOENIX_DEFAULT_RETENTION_POLICY_DAYS=90
      - PHOENIX_SMTP_HOSTNAME=${SMTP_HOST}
      - PHOENIX_SMTP_USERNAME=${SMTP_USER}
      - PHOENIX_SMTP_PASSWORD=${SMTP_PASS}
    restart: always
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: "2.0"
```

**.env file:**
```bash
DB_PASSWORD=secure_random_password
PHOENIX_SECRET=long_random_string_min_32_chars
SMTP_HOST=smtp.sendgrid.net
SMTP_USER=apikey
SMTP_PASS=SG.your_key_here
```

**Start:** `docker compose -f docker-compose.prod.yml up -d`

---

## Troubleshooting

### Phoenix won't start

**Check logs:**
```bash
docker compose logs phoenix
```

**Common issues:**
- Database connection failed: Verify `PHOENIX_SQL_DATABASE_URL`
- Port already in use: Change port mapping
- Volume permissions: Ensure write access to mounted volumes

### Traces not appearing

**Verify collector endpoint:**
```bash
curl http://localhost:6006/v1/traces
```

**Check authentication:**
- If auth enabled, ensure API key is set
- Verify authorization header format: `Bearer <token>`

**Application configuration:**
```python
import os
print(os.getenv("PHOENIX_COLLECTOR_ENDPOINT"))
print(os.getenv("PHOENIX_API_KEY"))
```

### Database connection errors

**PostgreSQL not ready:**
```yaml
phoenix:
  depends_on:
    db:
      condition: service_healthy
```

**Connection string format:**
```bash
# Correct
postgresql://user:password@host:5432/database

# Incorrect
postgres://user:password@host:5432/database  # Use 'postgresql://'
```

### Performance issues

**Check resource usage:**
```bash
docker stats
```

**Increase limits:**
```yaml
deploy:
  resources:
    limits:
      memory: 4G
      cpus: "4.0"
```

**Optimize PostgreSQL:**
- Increase `shared_buffers`
- Adjust `max_connections`
- Enable connection pooling

---

## Additional Resources

### Documentation

- [Phoenix Documentation](https://arize.com/docs/phoenix)
- [Docker Deployment Guide](file://.local/references/phoenix/docs/section-self-hosting/deployment-options/docker.md)
- [Configuration Reference](file://.local/references/phoenix/docs/section-self-hosting/configuration.md)
- [Authentication Setup](file://.local/references/phoenix/docs/section-self-hosting/authentication.md)
- [Email Configuration](file://.local/references/phoenix/docs/section-self-hosting/email.md)

### Example Files

- [Basic docker-compose.yml](file://.local/references/phoenix/docker-compose.yml)
- [Development Setup](file://.local/references/phoenix/scripts/docker/devops/docker-compose.yml)
- [Manually Instrumented Chatbot](file://.local/references/phoenix/examples/manually-instrumented-chatbot/compose.yml)

### Docker Resources

- [Phoenix Docker Hub](https://hub.docker.com/r/arizephoenix/phoenix)
- [Dockerfile Reference](file://.local/references/phoenix/Dockerfile)
- [Phoenix GitHub Repository](https://github.com/Arize-ai/phoenix)

### Support

- [GitHub Issues](https://github.com/Arize-ai/phoenix/issues)
- [Arize Community Slack](https://arize-ai.slack.com)
- [Phoenix FAQs](file://.local/references/phoenix/docs/section-self-hosting/misc/frequently-asked-questions.md)

---

## Version History

- **v4.0+** - PostgreSQL support, authentication, multi-user
- **v3.0+** - OTLP gRPC collector, project namespacing
- **v2.0+** - Docker support, persistent storage
- **v1.0+** - Initial release

**Note:** Always refer to [CHANGELOG](file://.local/references/phoenix/CHANGELOG.md) for version-specific changes.