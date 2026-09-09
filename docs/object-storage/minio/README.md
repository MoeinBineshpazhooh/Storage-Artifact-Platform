# 🟣 MinIO — S3-Compatible Object Storage

<p align="center"><strong>Object Storage • Docker Compose • Persistent Data • Elasticsearch Snapshots</strong></p>

---

## 🎯 01 • What This Component Solves

MinIO provides an S3-compatible object-storage interface suitable for applications that need object-based data rather than Kubernetes block volumes.

In this portfolio, its practical role is **ELK snapshot storage**.

---

## 🧑‍💻 02 • My Hands-On Experience

MinIO was personally implemented as a **single-node Docker Compose service** with persistent Docker storage.

```text
MinIO
├── Single instance
├── Docker Compose
└── Persistent Docker volume
```

The implementation was used as an S3-compatible backend for daily Elasticsearch snapshots.

> ⚠️ This is not presented as distributed or highly available MinIO.

---

## 🏗️ 03 • Architecture

```text
              Elasticsearch
                    │
                    │ Daily Snapshot
                    ▼
             S3-Compatible API
                    │
                    ▼
             ┌──────────────┐
             │    MinIO     │
             └──────┬───────┘
                    │
                    ▼
             Persistent Data
```

The value of this design is the separation between the application's snapshot mechanism and the underlying object-storage implementation.

---

## ⚙️ 04 • Implement

The sanitized Compose definition is available here:

📁 [`docker-compose.yaml`](../../../manifests/minio/docker-compose.yaml)

Create the local environment file from the template:

```bash
cp manifests/minio/.env.example manifests/minio/.env
```

Then start MinIO:

```bash
docker compose -f manifests/minio/docker-compose.yaml up -d
```

The portfolio uses the fictional endpoint:

```text
minio.moein.local
```

Credentials are supplied externally and are never committed.

---

## 🧪 05 • Validate

```bash
docker compose -f manifests/minio/docker-compose.yaml ps
docker compose -f manifests/minio/docker-compose.yaml logs --tail=100 minio
```

Validation should prove:

```text
Container Running
      │
      ▼
S3 Endpoint Reachable
      │
      ▼
Bucket Available
      │
      ▼
Elasticsearch Snapshot Repository
      │
      ▼
Snapshot Successfully Written
```

---

## 🔧 06 • Operate

Typical operational checks:

- Container state
- Persistent volume availability
- Object-storage endpoint reachability
- Bucket availability
- Elasticsearch snapshot success
- Available storage capacity

---

## 🚨 07 • Troubleshoot

```text
Snapshot Failure
      │
      ├──► Check MinIO container
      ├──► Check endpoint connectivity
      ├──► Check bucket/repository configuration
      ├──► Check object-storage capacity
      └──► Check Elasticsearch repository errors
```

Useful non-secret checks:

```bash
docker compose -f manifests/minio/docker-compose.yaml ps
docker compose -f manifests/minio/docker-compose.yaml logs --tail=100 minio
docker volume ls
```

---

## 🧠 08 • Lessons Learned

Object storage is a different abstraction from PV/PVC-based block storage. For snapshot workflows, the important contract is the **S3 API**, allowing Elasticsearch to write snapshots without depending directly on a filesystem path.

---

## 🔐 Evidence Boundary

The documented implementation is specifically **single-node MinIO with Docker Compose**. No distributed, erasure-coded or HA MinIO deployment is claimed.

No credentials or private infrastructure endpoints belong in this repository.
