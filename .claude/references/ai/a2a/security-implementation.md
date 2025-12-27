---
title: "A2A Security and Implementation Guide"
description: "Security best practices and implementation patterns for the A2A Protocol"
type: "integration-guide"
tags: ["security", "authentication", "authorization", "oauth", "implementation", "deployment", "best-practices", "enterprise"]
category: "ai"
subcategory: "protocols"
version: "0.3.0"
last_updated: "2025-07-01"
status: "stable"
sources:
  - name: "A2A Protocol Specification"
    url: "https://a2a-protocol.org/latest/specification/"
  - name: "A2A Enterprise Features"
    url: "https://a2a-protocol.org/latest/topics/enterprise-ready/"
  - name: "A2A GitHub Repository"
    url: "https://github.com/a2aproject/A2A"
  - name: "A2A Python SDK"
    url: "https://github.com/a2aproject/a2a-python"
  - name: "A2A Sample Implementations"
    url: "https://github.com/a2aproject/a2a-samples"
related: ["specification.md", "overview.md"]
author: "unknown"
contributors: []
---

# A2A Security and Implementation Guide

Comprehensive guide covering security best practices, authentication patterns, implementation workflows, and enterprise deployment considerations for the A2A Protocol.

## Security Architecture

A2A implements security at multiple layers to ensure enterprise-grade protection: ([A2A Enterprise Features][2])

### Defense in Depth

**Transport Layer:**
- HTTPS mandatory (TLS 1.3+ recommended)
- Certificate validation
- Strong cipher suites

**Authentication Layer:**
- Mandatory request authentication
- Industry-standard schemes (OAuth2, OIDC, mTLS)
- Token-based access control

**Authorization Layer:**
- Granular per-skill permissions
- OAuth scope-based access
- Identity-based policy enforcement

**Application Layer:**
- Input validation and sanitization
- Rate limiting and throttling
- Audit logging and tracing

## Authentication Mechanisms

Every A2A request MUST be authenticated per the agent's declared security schemes. ([A2A Specification][1])

### OAuth 2.0

**Best For:** User-delegated access, third-party integrations, fine-grained permissions

**Agent Card Declaration:**
```yaml
securitySchemes:
  oauth2:
    type: oauth2
    flows:
      authorizationCode:
        authorizationUrl: https://auth.example.com/oauth/authorize
        tokenUrl: https://auth.example.com/oauth/token
        scopes:
          agent:read: "View agent capabilities"
          agent:execute: "Execute agent tasks"
          agent:admin: "Manage agent configuration"

security:
  - oauth2: ["agent:read", "agent:execute"]
```

**Client Implementation:**

```python
from a2a_sdk import A2AClient
from requests_oauthlib import OAuth2Session

# OAuth 2.0 flow
oauth = OAuth2Session(
    client_id='your-client-id',
    redirect_uri='https://your-app.com/callback',
    scope=['agent:read', 'agent:execute']
)

# Get authorization URL
authorization_url, state = oauth.authorization_url(
    'https://auth.example.com/oauth/authorize'
)

# User visits authorization_url and grants consent
# After redirect, exchange code for token
token = oauth.fetch_token(
    'https://auth.example.com/oauth/token',
    client_secret='your-client-secret',
    code='authorization-code'
)

# Use token with A2A client
client = A2AClient(
    agent_url='https://agent.example.com',
    auth_token=token['access_token']
)
```

**Per-Skill Authorization:**

Use OAuth scopes to control access to specific agent skills:

```yaml
skills:
  - name: "public-search"
    description: "Public web search"
    requiredScopes: ["agent:read"]

  - name: "private-data-access"
    description: "Access confidential data"
    requiredScopes: ["agent:read", "agent:admin"]
```

**Token Refresh:**

```python
# Automatic token refresh
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient

client = BackendApplicationClient(client_id='your-client-id')
oauth = OAuth2Session(
    client=client,
    auto_refresh_url='https://auth.example.com/oauth/token',
    auto_refresh_kwargs={
        'client_id': 'your-client-id',
        'client_secret': 'your-client-secret'
    },
    token_updater=lambda token: save_token(token)
)
```

### OpenID Connect

**Best For:** SSO integrations, identity federation, enterprise authentication

**Agent Card Declaration:**
```yaml
securitySchemes:
  openIdConnect:
    type: openIdConnect
    openIdConnectUrl: https://auth.example.com/.well-known/openid-configuration

security:
  - openIdConnect: []
```

**Client Implementation:**

```python
from authlib.integrations.requests_client import OAuth2Session

# OIDC discovery
client = OAuth2Session(
    client_id='your-client-id',
    client_secret='your-client-secret',
    scope='openid profile email',
    redirect_uri='https://your-app.com/callback'
)

# Discover OIDC endpoints
authorize_url = 'https://auth.example.com/oauth/authorize'
token_url = 'https://auth.example.com/oauth/token'

# Get authorization and exchange for token
authorization_url, state = client.create_authorization_url(authorize_url)
# User authorizes...
token = client.fetch_token(token_url, authorization_response='...')

# Extract ID token and user info
id_token = token['id_token']
userinfo = client.userinfo()
```

**ID Token Validation:**

```python
from jose import jwt

def validate_id_token(id_token, issuer, audience, jwks_url):
    # Fetch JWKS
    jwks_client = jwt.PyJWKClient(jwks_url)
    signing_key = jwks_client.get_signing_key_from_jwt(id_token)

    # Validate token
    claims = jwt.decode(
        id_token,
        signing_key.key,
        algorithms=['RS256'],
        issuer=issuer,
        audience=audience
    )

    return claims
```

### API Key Authentication

**Best For:** Service-to-service communication, simple integrations, development/testing

**Agent Card Declaration:**
```yaml
securitySchemes:
  apiKey:
    type: apiKey
    in: header
    name: X-API-Key

security:
  - apiKey: []
```

**Client Implementation:**

```python
from a2a_sdk import A2AClient

client = A2AClient(
    agent_url='https://agent.example.com',
    headers={'X-API-Key': 'your-api-key'}
)
```

**Best Practices:**
- Generate cryptographically random keys (32+ bytes)
- Store keys in secure credential management systems (not code)
- Rotate keys periodically
- Use different keys per environment (dev, staging, prod)
- Revoke compromised keys immediately

**Key Storage:**

```python
import os
from cryptography.fernet import Fernet

# Environment variable (development)
api_key = os.environ.get('A2A_API_KEY')

# Encrypted config file (production)
def decrypt_api_key(encrypted_key_file):
    with open('encryption.key', 'rb') as f:
        key = f.read()
    fernet = Fernet(key)

    with open(encrypted_key_file, 'rb') as f:
        encrypted = f.read()

    return fernet.decrypt(encrypted).decode()
```

### HTTP Bearer Authentication

**Best For:** JWT-based authentication, stateless API access, microservices

**Agent Card Declaration:**
```yaml
securitySchemes:
  bearerAuth:
    type: http
    scheme: bearer
    bearerFormat: JWT

security:
  - bearerAuth: []
```

**Client Implementation:**

```python
import jwt
from datetime import datetime, timedelta

# Generate JWT
def create_jwt(secret_key, payload_data):
    payload = {
        'sub': 'client-id',
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=1),
        **payload_data
    }

    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

# Use with A2A client
token = create_jwt('your-secret', {'user_id': '123'})
client = A2AClient(
    agent_url='https://agent.example.com',
    auth_token=token
)
```

**Server Validation:**

```python
import jwt
from functools import wraps
from flask import request, jsonify

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid token'}), 401

        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        return f(*args, **kwargs)
    return decorated
```

### Mutual TLS (mTLS)

**Best For:** Zero-trust architectures, high-security environments, service mesh

**Agent Card Declaration:**
```yaml
securitySchemes:
  mutualTLS:
    type: mutualTLS

security:
  - mutualTLS: []
```

**Client Configuration:**

```python
import requests
from a2a_sdk import A2AClient

# Configure client certificate
client = A2AClient(
    agent_url='https://agent.example.com',
    cert=('/path/to/client-cert.pem', '/path/to/client-key.pem'),
    verify='/path/to/ca-cert.pem'
)
```

**Server Configuration (Nginx):**

```nginx
server {
    listen 443 ssl;
    server_name agent.example.com;

    ssl_certificate /path/to/server-cert.pem;
    ssl_certificate_key /path/to/server-key.pem;

    # Require client certificate
    ssl_client_certificate /path/to/ca-cert.pem;
    ssl_verify_client on;
    ssl_verify_depth 2;

    location / {
        # Pass client cert info to backend
        proxy_set_header X-SSL-Client-Cert $ssl_client_cert;
        proxy_set_header X-SSL-Client-S-DN $ssl_client_s_dn;
        proxy_pass http://backend;
    }
}
```

**Certificate Management:**

```bash
# Generate CA key and certificate
openssl genrsa -out ca-key.pem 4096
openssl req -new -x509 -days 3650 -key ca-key.pem -out ca-cert.pem

# Generate client key and CSR
openssl genrsa -out client-key.pem 4096
openssl req -new -key client-key.pem -out client.csr

# Sign client certificate with CA
openssl x509 -req -days 365 -in client.csr -CA ca-cert.pem \
  -CAkey ca-key.pem -CAcreateserial -out client-cert.pem
```

## Authorization Patterns

### Principle of Least Privilege

Grant minimum permissions necessary for task execution: ([A2A Enterprise Features][2])

**OAuth Scope Design:**
```yaml
scopes:
  agent:discover: "View agent capabilities (Agent Card)"
  agent:read: "Read task status and artifacts"
  agent:execute: "Create and manage tasks"
  agent:cancel: "Cancel running tasks"
  agent:admin: "Configure agent settings"

  skill:search:execute: "Execute web search skill"
  skill:analysis:execute: "Execute document analysis skill"
  skill:sensitive:execute: "Execute sensitive data access skill"
```

**Granular Skill Authorization:**
```python
def check_skill_authorization(user_scopes, skill_name, skill_scopes):
    required = set(skill_scopes)
    granted = set(user_scopes)

    if not required.issubset(granted):
        missing = required - granted
        raise AuthorizationError(
            f"Missing required scopes for skill '{skill_name}': {missing}"
        )
```

### Role-Based Access Control (RBAC)

Map OAuth scopes to organizational roles:

```python
ROLE_SCOPES = {
    'viewer': ['agent:discover', 'agent:read'],
    'operator': ['agent:discover', 'agent:read', 'agent:execute'],
    'admin': ['agent:discover', 'agent:read', 'agent:execute',
              'agent:cancel', 'agent:admin']
}

def get_scopes_for_role(role):
    return ROLE_SCOPES.get(role, [])
```

### Attribute-Based Access Control (ABAC)

Policy-based authorization using user and resource attributes:

```python
def evaluate_policy(user_attrs, resource_attrs, action):
    # Example: Allow task execution if user's department matches agent's department
    if action == 'execute' and user_attrs['department'] == resource_attrs['department']:
        return True

    # Example: Allow sensitive data access only during business hours
    if 'sensitive' in resource_attrs and not is_business_hours():
        return False

    # Evaluate additional policy rules...
    return False
```

## Secondary Authentication

A2A supports secondary in-task authentication for external systems via the `auth-required` state. ([A2A Specification][1])

### Use Case

Agent needs to access external system requiring user credentials:

**Flow:**
1. Client sends message to agent
2. Agent determines external system access needed
3. Agent transitions task to `auth-required` state
4. Client prompts user for credentials
5. Client sends credentials in follow-up message
6. Agent authenticates with external system
7. Agent resumes processing

**Example:**

```python
# Client code
response = client.message_send(messages=[
    {"role": "user", "parts": [{"type": "text", "text": "Fetch my email"}]}
])

task = response['task']

# Poll for status
while task['state'] not in ['completed', 'failed', 'auth-required']:
    time.sleep(1)
    task = client.tasks_get(task['taskId'])['task']

if task['state'] == 'auth-required':
    # Prompt user for email credentials
    email = input("Email: ")
    password = getpass.getpass("Password: ")

    # Send credentials to agent
    client.message_send(
        messages=[{
            "role": "user",
            "parts": [{
                "type": "data",
                "data": {
                    "email": email,
                    "password": password
                }
            }]
        }],
        task_id=task['taskId']
    )
```

**Security Considerations:**
- Never log or store secondary credentials
- Use secure channels for credential transmission
- Prefer OAuth/OIDC over password exchange when possible
- Implement credential timeouts
- Clear credentials from memory after use

## Enterprise Security Features

### Distributed Tracing

A2A supports W3C Trace Context for distributed tracing: ([A2A Enterprise Features][2])

**Headers:**
```
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
tracestate: vendor1=value1,vendor2=value2
```

**Client Implementation:**

```python
from opentelemetry import trace
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

tracer = trace.get_tracer(__name__)
propagator = TraceContextTextMapPropagator()

# Create span
with tracer.start_as_current_span("a2a_request") as span:
    # Inject trace context into headers
    headers = {}
    propagator.inject(headers)

    # Make A2A request with trace headers
    client = A2AClient(
        agent_url='https://agent.example.com',
        headers=headers
    )
    response = client.message_send(...)
```

**Server Extraction:**

```python
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

def handle_request(request):
    propagator = TraceContextTextMapPropagator()

    # Extract trace context from request headers
    ctx = propagator.extract(request.headers)

    # Start span with extracted context
    with tracer.start_as_current_span("process_message", context=ctx):
        # Process request...
        pass
```

### Audit Logging

Comprehensive logging for compliance and security monitoring: ([A2A Enterprise Features][2])

**Required Log Fields:**
```python
import logging
import json

def log_request(request, response, user_id, duration_ms):
    log_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'user_id': user_id,
        'task_id': response.get('task', {}).get('taskId'),
        'session_id': request.get('sessionId'),
        'method': request['method'],
        'agent_url': request['agent_url'],
        'status': 'success' if 'result' in response else 'error',
        'duration_ms': duration_ms,
        'trace_id': extract_trace_id(request.headers),
        'ip_address': request.remote_addr,
        'user_agent': request.headers.get('User-Agent')
    }

    logging.info(json.dumps(log_entry))
```

**Compliance Requirements:**
- Log all authentication attempts (success and failure)
- Log task creation, state transitions, and completion
- Log access to sensitive skills or data
- Include correlation IDs (taskId, sessionId, traceId)
- Retain logs per regulatory requirements (GDPR, HIPAA, SOC2)

### Rate Limiting

Protect against abuse and ensure fair resource allocation: ([A2A Enterprise Features][2])

**Token Bucket Implementation:**

```python
from collections import defaultdict
from time import time

class RateLimiter:
    def __init__(self, rate_per_second, burst_size):
        self.rate = rate_per_second
        self.burst = burst_size
        self.buckets = defaultdict(lambda: {
            'tokens': burst_size,
            'last_update': time()
        })

    def allow_request(self, client_id):
        bucket = self.buckets[client_id]
        now = time()

        # Refill tokens
        elapsed = now - bucket['last_update']
        bucket['tokens'] = min(
            self.burst,
            bucket['tokens'] + elapsed * self.rate
        )
        bucket['last_update'] = now

        # Check and consume token
        if bucket['tokens'] >= 1:
            bucket['tokens'] -= 1
            return True
        return False

# Usage
limiter = RateLimiter(rate_per_second=10, burst_size=100)

def handle_request(request):
    client_id = get_client_id(request)

    if not limiter.allow_request(client_id):
        return {
            'jsonrpc': '2.0',
            'id': request['id'],
            'error': {
                'code': 2003,
                'message': 'Rate limit exceeded'
            }
        }, 429

    # Process request...
```

**Per-User and Per-Skill Limits:**

```python
RATE_LIMITS = {
    'default': {'rate': 10, 'burst': 100},
    'premium': {'rate': 100, 'burst': 1000},
    'skill:search': {'rate': 20, 'burst': 50},
    'skill:sensitive': {'rate': 5, 'burst': 10}
}

def get_rate_limit(user_tier, skill_name):
    skill_limit = RATE_LIMITS.get(f'skill:{skill_name}')
    user_limit = RATE_LIMITS.get(user_tier, RATE_LIMITS['default'])

    # Return most restrictive limit
    return {
        'rate': min(skill_limit['rate'], user_limit['rate']),
        'burst': min(skill_limit['burst'], user_limit['burst'])
    }
```

### API Gateway Integration

Use API gateways for centralized security policy enforcement:

**Kong Configuration:**
```yaml
services:
  - name: a2a-agent
    url: http://agent-backend:8000
    routes:
      - name: a2a-route
        paths:
          - /
    plugins:
      - name: oauth2
        config:
          scopes:
            - agent:read
            - agent:execute
      - name: rate-limiting
        config:
          minute: 60
          hour: 1000
      - name: request-transformer
        config:
          add:
            headers:
              - X-Trace-ID:$(uuid)
      - name: correlation-id
      - name: file-log
        config:
          path: /var/log/kong/a2a-access.log
```

**AWS API Gateway:**
```yaml
Resources:
  A2AApi:
    Type: AWS::ApiGateway::RestApi
    Properties:
      Name: A2A Agent API

  A2AAuthorizer:
    Type: AWS::ApiGateway::Authorizer
    Properties:
      Type: COGNITO_USER_POOLS
      IdentitySource: method.request.header.Authorization
      ProviderARNs:
        - !GetAtt CognitoUserPool.Arn

  A2AThrottle:
    Type: AWS::ApiGateway::UsagePlan
    Properties:
      Throttle:
        RateLimit: 100
        BurstLimit: 200
```

## Data Privacy and Compliance

### Data Minimization

Only collect and transmit necessary data: ([A2A Enterprise Features][2])

**Message Filtering:**
```python
def sanitize_message(message, allowed_fields):
    sanitized_parts = []

    for part in message['parts']:
        if part['type'] == 'data':
            # Remove sensitive fields
            filtered_data = {
                k: v for k, v in part['data'].items()
                if k in allowed_fields
            }
            sanitized_parts.append({
                'type': 'data',
                'data': filtered_data
            })
        else:
            sanitized_parts.append(part)

    return {
        'role': message['role'],
        'parts': sanitized_parts
    }
```

### PII Detection and Redaction

Automatically detect and redact personally identifiable information:

```python
import re

PII_PATTERNS = {
    'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
    'credit_card': r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
    'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
}

def redact_pii(text):
    redacted = text
    for pii_type, pattern in PII_PATTERNS.items():
        redacted = re.sub(pattern, f'[REDACTED-{pii_type.upper()}]', redacted)
    return redacted

def process_message_with_pii_protection(message):
    for part in message['parts']:
        if part['type'] == 'text':
            part['text'] = redact_pii(part['text'])
    return message
```

### GDPR Compliance

Implement right to erasure and data portability:

```python
def delete_user_data(user_id):
    # Delete all tasks for user
    tasks = get_tasks_by_user(user_id)
    for task in tasks:
        delete_task(task['taskId'])

    # Delete audit logs
    delete_audit_logs(user_id)

    # Anonymize remaining references
    anonymize_user_references(user_id)

    log_gdpr_deletion(user_id)

def export_user_data(user_id):
    # Export all user data in machine-readable format
    data = {
        'user_id': user_id,
        'tasks': get_tasks_by_user(user_id),
        'audit_logs': get_audit_logs(user_id),
        'consents': get_user_consents(user_id)
    }

    return json.dumps(data, indent=2)
```

## Common Implementation Patterns

### Basic Synchronous Execution

Simple request/response pattern:

```python
from a2a_sdk import A2AClient

# Initialize client
client = A2AClient(
    agent_url='https://agent.example.com',
    auth_token='your-token'
)

# Send message
response = client.message_send(messages=[
    {
        "role": "user",
        "parts": [
            {"type": "text", "text": "Analyze this document"},
            {"type": "file", "file": {"bytes": base64_data}, "mimeType": "application/pdf"}
        ]
    }
])

task_id = response['task']['taskId']

# Poll for completion
while True:
    task = client.tasks_get(task_id)['task']

    if task['state'] in ['completed', 'failed', 'rejected']:
        break

    time.sleep(1)

# Retrieve results
if task['state'] == 'completed':
    for artifact in task.get('artifacts', []):
        for part in artifact['parts']:
            if part['type'] == 'text':
                print(part['text'])
```

### Streaming Execution

Real-time updates via Server-Sent Events:

```python
from a2a_sdk import A2AClient

client = A2AClient(
    agent_url='https://agent.example.com',
    auth_token='your-token'
)

# Start streaming
for event in client.message_stream(messages=[
    {"role": "user", "parts": [{"type": "text", "text": "Generate report"}]}
]):
    if event['type'] == 'taskStatusUpdate':
        print(f"Status: {event['task']['state']}")

    elif event['type'] == 'taskArtifactUpdate':
        artifact = event['artifact']
        for part in artifact['parts']:
            if part['type'] == 'text':
                print(f"Partial result: {part['text']}")

    elif event['type'] == 'taskError':
        print(f"Error: {event['error']['message']}")
        break
```

### Multi-Turn Interaction

Handling `input-required` state:

```python
def handle_multi_turn_conversation(client, initial_message):
    response = client.message_send(messages=[initial_message])
    task_id = response['task']['taskId']

    while True:
        task = client.tasks_get(task_id)['task']

        if task['state'] == 'input-required':
            # Agent needs additional input
            user_input = input("Agent asks: Provide additional information: ")

            # Send follow-up message
            client.message_send(
                messages=[{
                    "role": "user",
                    "parts": [{"type": "text", "text": user_input}]
                }],
                task_id=task_id
            )

        elif task['state'] in ['completed', 'failed']:
            break

        else:
            time.sleep(1)

    return task
```

### Asynchronous with Webhooks

Fire-and-forget with notifications:

```python
# Configure webhook
client.push_notification_config_set(
    url='https://your-app.com/webhooks/a2a',
    events=['taskStatusUpdate', 'taskArtifactUpdate'],
    headers={'X-Webhook-Secret': 'your-webhook-secret'}
)

# Submit task
response = client.message_send(messages=[...])
task_id = response['task']['taskId']

# Disconnect - agent will POST updates to webhook

# Webhook handler (Flask example)
from flask import Flask, request, jsonify
import hmac

app = Flask(__name__)

@app.route('/webhooks/a2a', methods=['POST'])
def handle_webhook():
    # Verify webhook signature
    signature = request.headers.get('X-Webhook-Signature')
    if not verify_signature(request.data, signature):
        return jsonify({'error': 'Invalid signature'}), 401

    event = request.json

    if event['type'] == 'taskStatusUpdate':
        task = event['task']
        if task['state'] == 'completed':
            process_completed_task(task)

    return jsonify({'status': 'ok'})
```

### Connection Retry with Exponential Backoff

Resilient client implementation:

```python
import time
import random

def retry_with_backoff(func, max_retries=5, base_delay=1, max_delay=60):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise

            delay = min(base_delay * (2 ** attempt), max_delay)
            jitter = random.uniform(0, delay * 0.1)
            sleep_time = delay + jitter

            print(f"Attempt {attempt + 1} failed: {e}. Retrying in {sleep_time:.2f}s...")
            time.sleep(sleep_time)

# Usage
response = retry_with_backoff(
    lambda: client.message_send(messages=[...])
)
```

### File Exchange Patterns

**Upload:**
```python
import base64

def upload_file(client, file_path, task_message):
    with open(file_path, 'rb') as f:
        file_bytes = base64.b64encode(f.read()).decode('utf-8')

    response = client.message_send(messages=[
        {
            "role": "user",
            "parts": [
                {"type": "text", "text": task_message},
                {
                    "type": "file",
                    "file": {"bytes": file_bytes},
                    "mimeType": "application/pdf",
                    "filename": os.path.basename(file_path)
                }
            ]
        }
    ])

    return response
```

**Download:**
```python
import requests

def download_artifact_files(task):
    for artifact in task.get('artifacts', []):
        for part in artifact['parts']:
            if part['type'] == 'file' and 'uri' in part['file']:
                uri = part['file']['uri']
                headers = part['file'].get('headers', {})

                response = requests.get(uri, headers=headers)
                filename = part.get('filename', f"artifact_{artifact['artifactId']}")

                with open(filename, 'wb') as f:
                    f.write(response.content)

                print(f"Downloaded: {filename}")
```

## Security Best Practices

### Never Publish Credentials in Agent Cards

Agent Cards are publicly accessible - NEVER include credentials: ([A2A Enterprise Features][2])

**❌ Bad:**
```yaml
securitySchemes:
  apiKey:
    type: apiKey
    in: header
    name: X-API-Key
    value: "secret-key-123"  # NEVER DO THIS
```

**✅ Good:**
```yaml
securitySchemes:
  apiKey:
    type: apiKey
    in: header
    name: X-API-Key
# Client obtains key through out-of-band mechanism
```

### Sanitize External Agent Data

Treat data from external agents as untrusted: ([A2A Enterprise Features][2])

```python
def sanitize_agent_response(response):
    # Prevent prompt injection
    if 'task' in response:
        for artifact in response['task'].get('artifacts', []):
            for part in artifact['parts']:
                if part['type'] == 'text':
                    # Remove potential injection patterns
                    part['text'] = remove_injection_patterns(part['text'])

    return response

def remove_injection_patterns(text):
    # Remove common injection attempts
    dangerous_patterns = [
        r'```.*?```',  # Code blocks
        r'<script.*?</script>',  # Scripts
        r'system:',  # System prompts
        r'assistant:',  # Role manipulation
    ]

    cleaned = text
    for pattern in dangerous_patterns:
        cleaned = re.sub(pattern, '[REMOVED]', cleaned, flags=re.IGNORECASE | re.DOTALL)

    return cleaned
```

### Use Secure Credential Storage

Store credentials in secure systems, never in code or config files:

```python
# AWS Secrets Manager
import boto3

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

# HashiCorp Vault
import hvac

def get_vault_secret(path):
    client = hvac.Client(url='https://vault.example.com', token=os.environ['VAULT_TOKEN'])
    secret = client.secrets.kv.v2.read_secret_version(path=path)
    return secret['data']['data']

# Azure Key Vault
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def get_azure_secret(vault_url, secret_name):
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    secret = client.get_secret(secret_name)
    return secret.value
```

### Implement Request Timeouts

Prevent resource exhaustion from hanging requests:

```python
from a2a_sdk import A2AClient

client = A2AClient(
    agent_url='https://agent.example.com',
    auth_token='your-token',
    timeout=30  # 30 second timeout
)

# Per-request timeout
try:
    response = client.message_send(
        messages=[...],
        timeout=60  # 60 seconds for this specific request
    )
except TimeoutError:
    print("Request timed out")
```

### Validate Agent Cards

Verify Agent Card integrity before trusting:

```python
def validate_agent_card(card):
    # Check required fields
    required_fields = ['protocolVersion', 'name', 'url', 'preferredTransport']
    for field in required_fields:
        if field not in card:
            raise ValueError(f"Missing required field: {field}")

    # Verify protocol version compatibility
    if not is_compatible_version(card['protocolVersion'], '0.3.0'):
        raise ValueError(f"Incompatible protocol version: {card['protocolVersion']}")

    # Verify HTTPS URL
    if not card['url'].startswith('https://'):
        raise ValueError("Agent URL must use HTTPS")

    # Verify signatures if present
    if 'signatures' in card:
        verify_agent_card_signature(card)

    return True
```

## Production Deployment Checklist

- [ ] **HTTPS enforced** with TLS 1.3+ and strong cipher suites
- [ ] **Authentication configured** using appropriate scheme (OAuth2, OIDC, mTLS)
- [ ] **Authorization implemented** with granular per-skill permissions
- [ ] **Rate limiting enabled** to prevent abuse
- [ ] **Audit logging configured** for all requests and authentication attempts
- [ ] **Distributed tracing enabled** with W3C Trace Context headers
- [ ] **Error handling implemented** with proper error codes and messages
- [ ] **Secrets stored securely** in credential management system
- [ ] **Input validation** for all message content
- [ ] **Output sanitization** to prevent injection attacks
- [ ] **Connection timeouts** configured appropriately
- [ ] **Retry logic** implemented with exponential backoff
- [ ] **Monitoring and alerting** for failures and anomalies
- [ ] **Data retention policies** configured per compliance requirements
- [ ] **Backup and disaster recovery** plans in place
- [ ] **Security review completed** by security team
- [ ] **Penetration testing** performed
- [ ] **Documentation updated** for security procedures

## References

[1]: https://a2a-protocol.org/latest/specification/ "A2A Protocol Specification"
[2]: https://a2a-protocol.org/latest/topics/enterprise-ready/ "A2A Enterprise Features"
[3]: https://github.com/a2aproject/A2A "A2A GitHub Repository"
[4]: https://github.com/a2aproject/a2a-python "A2A Python SDK"
[5]: https://github.com/a2aproject/a2a-samples "A2A Sample Implementations"
