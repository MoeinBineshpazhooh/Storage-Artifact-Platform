# MinIO — S3-Compatible Object Storage

## Implementation

A single MinIO instance was implemented with Docker Compose and persistent Docker storage.

## ELK snapshot workflow

```text
Elasticsearch
     │
     │ daily snapshot
     ▼
S3-compatible API
     │
     ▼
   MinIO
     │
     ▼
Persistent object data
```

The practical use case is storing daily Elasticsearch snapshots in an S3-compatible object-storage backend.

## Start

```bash
docker compose -f manifests/minio/docker-compose.yaml up -d
```

Set `MINIO_ROOT_USER` and `MINIO_ROOT_PASSWORD` through an external environment or secret-management mechanism. Never commit real credentials.

## Operational checks

```bash
docker compose ps
docker compose logs --tail=100 minio
```

## Scope boundary

This repository does not present the implementation as a distributed or highly available MinIO cluster.
