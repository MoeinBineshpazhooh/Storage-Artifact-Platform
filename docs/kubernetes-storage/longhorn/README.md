# Longhorn — Kubernetes Storage Operations

## Experience boundary

Longhorn was already implemented as the underlying storage platform. The hands-on scope documented here is Kubernetes-side consumption and operations.

### Environment

- Kubernetes: 3 control-plane nodes + 18 workers
- Workloads: primarily stateless applications using persistent volumes where required

### Hands-on scope

- StorageClass configuration
- PersistentVolume (PV) lifecycle
- PersistentVolumeClaim (PVC) lifecycle
- Application Deployment integration
- Storage troubleshooting
- Capacity management

## Common workflow

```text
StorageClass
    │
    ▼
PVC ───────────────► Application Deployment
    │                         │
    ▼                         ▼
PV / Longhorn ◄────────── Mounted Volume
```

## Validation commands

```bash
kubectl get storageclass
kubectl get pv
kubectl get pvc -A
kubectl describe pvc <pvc-name> -n <namespace>
kubectl describe pv <pv-name>
```

> Replace placeholders with environment-specific values. Do not copy production credentials or private endpoints into this repository.

## Implementation-ready example

See [`manifests/longhorn/storageclass-pvc.yaml`](../../../manifests/longhorn/storageclass-pvc.yaml).
