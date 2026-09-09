# Implementation Manifests

This directory contains sanitized, implementation-oriented examples for the technologies covered by the repository.

## Conventions

| Technology | Manifest type | Example endpoint / identifier |
|---|---|---|
| Longhorn | Kubernetes YAML | `longhorn-fast` |
| Ceph | Kubernetes YAML | `ceph-block` |
| MinIO | Docker Compose | `moein.local:9000` / `moein.local:9001` |
| Harbor | Kubernetes YAML | `moein.local` |
| Nexus | Reference templates | `moein.local` |

## Fake infrastructure domain

The portfolio uses **`moein.local`** consistently for fictional infrastructure endpoints.

Examples:

```text
harbor.moein.local
nexus.moein.local
minio.moein.local
registry.moein.local
```

Use the specific hostname required by each example; do not treat these names as real production endpoints.

## Safety

All manifests are sanitized. Never replace placeholders with production credentials and commit the resulting file.
