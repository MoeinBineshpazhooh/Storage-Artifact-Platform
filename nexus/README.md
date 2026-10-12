# ⚪ Nexus Repository Manager

<p align="center"><strong>Artifact Repository • Docker Registry Proxy • Internal Package Storage</strong></p>

This section documents a practical Nexus deployment pattern used as an internal repository service.

## Implementation Scope

The example demonstrates:

- Docker Compose deployment
- Persistent Nexus data storage
- Nginx reverse proxy exposure
- HTTPS endpoint pattern
- Docker registry access through Nexus

This is a reusable lab/template implementation. Credentials and certificates are placeholders only.

## Architecture

```text
Developer / CI/CD
       |
       v
registry.moein.local
       |
       v
     Nginx
       |
       v
 Nexus Docker Registry
       |
       v
 Persistent Nexus Data
```

## Components

| Component | Purpose |
|---|---|
| Nexus | Artifact repository service |
| Docker Registry Port | Store/pull container images |
| Nginx | TLS termination and external access |
| Volume | Persistent repository data |

## Deployment

```bash
cp .env.example .env
# Set reviewed NEXUS_IMAGE and NGINX_IMAGE versions/digests locally.
# Provide certificate.crt and private.key in the ignored certs/ directory.
docker compose --env-file .env -f docker-compose.yml config --quiet
docker compose --env-file .env -f docker-compose.yml up -d
```

Validation:

```bash
docker ps
curl https://registry.moein.local
```

## Repository Role

Nexus is kept as a practical repository-manager example in this storage platform. The stronger artifact workflow examples are documented in Harbor and JFrog sections.

This reference defaults to loopback host bindings. Port 5000 is reachable only inside the Compose network through NGINX; it is not published as an unauthenticated HTTP alternative. Configure a Nexus Docker repository connector on that port and enable the appropriate Docker authentication realm/permissions before registry tests. Access the UI locally at port 8081, replace the initial administrator credentials, and restrict anonymous access according to the repository policy. Set NEXUS_BIND_ADDRESS to a reviewed interface only with TLS/firewall controls. The sample TLS proxy needs the two named certificate files; it is not a complete Nexus repository/bootstrap configuration. Preserve the named data volume and never run down -v on required data.
