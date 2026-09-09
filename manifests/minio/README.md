# MinIO Manifests

Sanitized single-node Docker Compose example matching the documented implementation pattern.

## Start

```bash
cp .env.example .env
# Edit .env locally; never commit it.
docker compose -f docker-compose.yaml up -d
```

## Endpoints

- S3 API: `http://moein.local:9000`
- Console: `http://moein.local:9001`

For a local lab, add `moein.local` to `/etc/hosts` or use DNS that resolves it to the Docker host.

## Checks

```bash
docker compose ps
docker compose logs --tail=100 minio
```

This is a single-node example, not a distributed MinIO deployment.
