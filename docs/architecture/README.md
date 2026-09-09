# 🏗️ Architecture

## Platform view

```text
                           PLATFORM STORAGE
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
        ▼                         ▼                         ▼
 Persistent / Block          Object Storage          Artifact Storage
        │                         │                         │
   ┌────┴────┐                  MinIO               ┌──────┴──────┐
   │         │                    │                 │             │
Longhorn   Ceph              ELK Snapshots        Harbor        Nexus
   │         │                    │                 │             │
   └────┬────┘                    │                 └──────┬──────┘
        │                         │                        │
        └─────────────────────────┴────────────────────────┘
                                  │
                                  ▼
                         Kubernetes / CI/CD
```

## Design principles

- Use Kubernetes-native PV/PVC abstractions for persistent workload storage.
- Keep distributed-storage experiments explicitly separated from production claims.
- Use object storage for backup/snapshot workflows where appropriate.
- Keep container images and general build artifacts logically separated.
- Sanitize all examples before publication.

## Fictional infrastructure naming

The portfolio uses `moein.local` as its common fictional infrastructure domain.
