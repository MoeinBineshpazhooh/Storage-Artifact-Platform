# 🔗 External Ceph → Kubernetes

Use this path when Ceph is managed outside Kubernetes and Kubernetes consumes its RBD volumes.

## Components

- Ceph MON endpoints
- RBD pool
- restricted CephX identity
- Ceph-CSI
- CSI sidecars
- StorageClass
- PVC/PV
- workload test

## Data path

```
PVC
 ↓
Ceph-CSI Controller
 ↓
Ceph MON / RBD
 ↓
RADOS / CRUSH / PG
 ↓
OSDs

Pod
 ↓
Ceph-CSI Node Plugin
 ↓
RBD device
 ↓
filesystem
```

Files in this directory are sanitized examples. Replace placeholders with environment-specific values.
