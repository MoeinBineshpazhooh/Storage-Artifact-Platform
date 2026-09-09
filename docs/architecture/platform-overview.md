# Storage & Artifact Platform Architecture

```text
                         STORAGE & ARTIFACT PLATFORM
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          │                           │                           │
   Kubernetes Storage           Object Storage              Artifact Storage
          │                           │                           │
   ┌──────┴──────┐                  MinIO                ┌────────┴────────┐
   │             │                    │                  │                 │
Longhorn       Ceph             S3-compatible          Harbor            Nexus
   │             │                    │                  │                 │
PV / PVC      PV / PVC          ELK snapshots       Container images    Packages
   │             │                    │                  │                 │
   └─────────────┴────────────────────┴──────────────────┴─────────────────┘
                                      │
                               Platform / CI/CD
```

## Design principle

Each technology has a focused responsibility:

- **Longhorn:** Kubernetes persistent-storage operations.
- **Ceph:** distributed-storage laboratory and Kubernetes integration validation.
- **MinIO:** S3-compatible object storage used for Elasticsearch snapshots.
- **Harbor:** private container-image registry.
- **Nexus:** artifact/package repository layer, documented only where implementation evidence is available.

Examples are intentionally sanitized so they can be adapted without exposing private infrastructure details.
