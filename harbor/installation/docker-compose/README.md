# Harbor Docker Compose Deployment

## Purpose

This implementation provides a practical Harbor deployment template using Docker Compose.

The goal is to demonstrate:

- Harbor service architecture
- Container registry deployment
- HTTPS exposure
- CI/CD registry workflow

## Deployment Flow

```text
harbor.yml.example
        |
        v
prepare configuration
        |
        v
docker compose up
        |
        v
https://harbor.moein.local
```

## Harbor Services

The generated deployment contains:

| Service | Purpose |
|---|---|
| nginx-photon | External HTTPS entry point |
| harbor-core | Harbor API and authentication |
| harbor-portal | Web interface |
| registry-photon | Docker registry backend |
| harbor-registryctl | Registry management |
| harbor-jobservice | Background tasks |
| harbor-db | PostgreSQL metadata database |
| redis-photon | Cache and task support |
| harbor-log | Service logging |

## Security Notes

- Internal services communicate only through the Docker network.
- Only nginx exposes external ports.
- Secrets and certificates are placeholders.
- Replace all values before deployment.
