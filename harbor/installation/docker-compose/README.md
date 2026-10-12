# Harbor Docker Compose Deployment

## Purpose

The supplied `docker-compose.yml.example` illustrates Harbor's service architecture. It lacks the complete generated configuration and is not an installable Harbor deployment.

For deployment, obtain a tested official Harbor installer release, configure its matching `harbor.yml.tmpl` locally, and run the installer to generate the required configuration and Compose stack. The reduced `harbor.yml.example` here is reference material, not a replacement for that release's template. Keep generated credentials and private keys outside Git. Follow the [official installation guide](https://goharbor.io/docs/main/install-config/) for the selected release.

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

The hand-written `harbor/nginx/harbor.moein.local.conf` is also an architecture sketch. It lacks the complete installer-generated routing and registry token/authentication wiring; do not use it as a production proxy.
