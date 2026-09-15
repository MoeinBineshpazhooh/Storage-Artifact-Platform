# 🟣 MinIO Object Storage

<p align="center"><strong>S3-Compatible Storage • Backup Target • Kubernetes Integration</strong></p>

This section documents practical MinIO usage based on project experience.

## Implemented Use Cases

### Docker Compose Deployment

A standalone MinIO instance was deployed as S3-compatible storage and used as an Elasticsearch snapshot repository target.

Flow:

```text
Elasticsearch
      |
      v
 Snapshot Repository
      |
      v
    MinIO S3
```

### Kubernetes Deployment

MinIO can also be deployed in Kubernetes using Helm for application storage testing.

## Client Operations

Install MinIO Client:

```bash
curl -O https://dl.min.io/client/mc/release/linux-amd64/mc
chmod +x mc
mv mc /usr/local/bin/mc
```

Configure access:

```bash
mc alias set myminio http://<MINIO_HOST>:9000
```

Common operations:

```bash
mc ls myminio
mc mb myminio/mybucket
mc cp file.txt myminio/mybucket/
mc cp myminio/mybucket/file.txt ./file.txt
```

## Kubernetes Validation

```bash
kubectl get pods -n <namespace>
kubectl get secret -n <namespace>
kubectl port-forward svc/minio-console 9001:9001 -n <namespace>
```

## Scope

This repository focuses on practical deployment and usage, not complete object-storage administration.
