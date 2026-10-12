<div align="center">

# MinIO Deployment Examples

**Object Storage • S3-Compatible API • Docker Compose • Kubernetes**

</div>

---

## 🎯 Purpose

This directory contains sanitized, implementation-oriented MinIO examples for two deployment patterns:

- 🐳 **Docker Compose** — single-node MinIO with persistent Docker storage
- ☸️ **Kubernetes** — standalone MinIO installation with Helm
- 🛠️ **MinIO Client (`mc`)** — CLI installation, authentication, bucket management, upload/download, and verification

> **Scope:** The Kubernetes example uses standalone mode with one replica and disabled persistence for lab/testing scenarios. It is not a distributed or production HA MinIO deployment.

---

## 🏗️ Deployment Modes

```text
                         MinIO
                           │
              ┌────────────┴────────────┐
              │                         │
        Docker Compose             Kubernetes + Helm
              │                         │
        Single Instance            Standalone
              │                         │
        Docker Volume              1 Replica
              │                         │
              └────────────┬────────────┘
                           │
                      S3-Compatible API
                           │
                    MinIO Client (mc)
```

---

# 🐳 1. Docker Compose

Use the Compose example for a lightweight single-node deployment.

### Start

```bash
cp .env.example .env
# Set an approved MINIO_IMAGE version/digest and fresh root credentials locally.
# Never commit .env.
docker compose --env-file .env -f docker-compose.yaml up -d
```

### Endpoints

Use the sanitized portfolio hostname:

```text
S3 API:   http://127.0.0.1:9000
Console:  http://127.0.0.1:9001
```

Ports bind to loopback by default. For remote Elasticsearch clients, set `MINIO_BIND_ADDRESS` to the reviewed interface and configure TLS and firewall rules. Resolve the fictional hostname only in the target lab. Keep the same Compose project identity to reuse its named volume; `down -v` deletes that volume.

### Validate

```bash
docker compose --env-file .env -f docker-compose.yaml ps
docker compose --env-file .env -f docker-compose.yaml logs --tail=100 minio
```

---

# ☸️ 2. Kubernetes Installation

The following pattern installs MinIO through the Helm chart in standalone mode.

Supply the referenced Secret before installation through your secure workflow. The command does not pass passwords in Helm values. Inspect the selected release's values and both server/client images before using it.

```bash
helm repo add minio https://charts.min.io/
helm repo update

kubectl create namespace thanos-test
# Create minio-credentials through your secure workflow in this namespace.
# It must contain rootUser and rootPassword keys.
# Set a reviewed chart version; inspect its values before installing.
: "${MINIO_CHART_VERSION:?Set an approved chart version}"
helm show values minio/minio --version "$MINIO_CHART_VERSION"

helm install minio minio/minio \
  --namespace thanos-test \
  --version "$MINIO_CHART_VERSION" \
  --set existingSecret=minio-credentials \
  --set-json 'users=[]' \
  --set resources.requests.memory=512Mi \
  --set persistence.enabled=false \
  --set replicas=1 \
  --set mode=standalone
```

### Validate the Pod

```bash
kubectl get pods -n thanos-test
```

Expected pattern:

```text
NAME                     READY   STATUS    RESTARTS   AGE
minio-<generated-name>   1/1     Running   0          <age>
```

### Access the Console

For a lab/test environment, expose the console locally through port-forwarding:

```bash
kubectl port-forward svc/minio-console 9001:9001 \
  -n thanos-test
```

Access the console locally at `http://127.0.0.1:9001`; the default port-forward listens on localhost.

---

# 🔐 3. Kubernetes Credential Source

The install command refers to the pre-existing `minio-credentials` Secret with `rootUser` and `rootPassword` keys. Supply credentials through your approved secret workflow rather than command-line Helm values. Confirm only metadata:

```bash
kubectl get secret minio-credentials -n thanos-test
```

This is a disposable lab chart pattern. The upstream values reviewed for chart 5.4.0 use `existingSecret` and include a sample additional console user; `users=[]` prevents creating that user. Review these fields, both server/client image versions and resource sizing for your selected chart release. The 512Mi request is a lab starting point, not a production sizing recommendation. With persistence disabled, Pod replacement can lose data: do not store Elasticsearch backups in this Kubernetes example.

Reference: [upstream chart values](https://github.com/minio/minio/blob/master/helm/minio/values.yaml).

---

# 🛠️ 4. MinIO Client (`mc`)

The MinIO Client provides a command-line interface for interacting with S3-compatible storage.

## Install `mc`

```bash
curl -O https://dl.min.io/client/mc/release/linux-amd64/mc
chmod +x mc
mv mc /usr/local/bin/mc
```

Verify the installation:

```bash
mc --version
```

## Configure an Alias

Point the client at the MinIO S3 API endpoint:

```bash
mc alias set myminio http://<minio-host>:9000
```

When prompted, enter the credentials obtained from your secure deployment mechanism:

```text
Enter Access Key: <your-access-key>
Enter Secret Key: <your-secret-key>
Added `myminio` successfully.
```

For a sanitized portfolio environment, the endpoint can be represented as:

```bash
mc alias set myminio http://minio.moein.local:9000
```

> Do not put real access keys or secret keys in this repository.

---

# 🪣 5. Bucket Operations

List buckets:

```bash
mc ls myminio
```

Create a bucket:

```bash
mc mb myminio/mybucket
```

Verify it:

```bash
mc ls myminio
```

---

# 📤 6. Upload and Download Objects

Upload a local file:

```bash
mc cp /path/to/local/file myminio/mybucket/
```

Download an object:

```bash
mc cp myminio/mybucket/file /path/to/local/destination
```

Verify the object:

```bash
mc ls myminio/mybucket
```

---

# 🔄 7. Operational Flow

```text
Application / Elasticsearch
          │
          │ S3 API
          ▼
       MinIO
          │
          ├── Bucket
          │     └── Object
          │
          ▼
     MinIO Client (mc)
          │
          ├── ls
          ├── mb
          ├── cp upload
          └── cp download
```

In the broader platform, MinIO can provide S3-compatible object storage for workloads such as Elasticsearch snapshot repositories.

---

# ✅ Validation Checklist

```bash
# Kubernetes
kubectl get pods -n thanos-test
kubectl get svc -n thanos-test
kubectl get secret minio-credentials -n thanos-test

# MinIO Client
mc alias list
mc ls myminio
mc ls myminio/mybucket
```

A successful validation confirms:

- MinIO is running
- the S3 endpoint is reachable
- authentication works
- the alias is configured
- bucket operations work
- object upload/download works

---

# 🧰 Troubleshooting

| Symptom | Check |
|---|---|
| Pod not running | `kubectl describe pod -n thanos-test <pod>` |
| Console unreachable | Check `kubectl get svc -n thanos-test` and port-forward status |
| `mc` cannot connect | Verify the S3 endpoint and network reachability |
| Authentication failure | Verify credentials through the Kubernetes Secret or deployment configuration |
| Bucket creation fails | Check credentials, endpoint, and MinIO server health |
| Upload/download fails | Check object path, bucket name, connectivity, and permissions |

---

# ⚠️ Evidence & Scope

This repository intentionally separates reusable examples from claims about production ownership:

- **Docker Compose:** single-node MinIO implementation pattern
- **Kubernetes:** standalone Helm installation pattern for lab/test usage
- **MinIO Client:** operational CLI workflow for object-storage administration
- **Production distributed MinIO:** not claimed here

The examples are sanitized and use `moein.local`-based hostnames so no private infrastructure endpoints or credentials are exposed.

---

## 📚 Related Files

```text
manifests/minio/
├── README.md
├── docker-compose.yaml
└── .env.example
```

---

<div align="center">

**MinIO Documentation:** https://min.io/docs

</div>
