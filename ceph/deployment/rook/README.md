# ☸️ Rook-Ceph Deployment

Rook manages Ceph through Kubernetes and represents the cluster through Kubernetes resources.

## Practical flow

```
Kubernetes
 ↓
Rook Operator
 ↓
CephCluster
 ├── MON
 ├── MGR
 └── OSDs
 ↓
RADOS/RBD
 ↓
Rook/Ceph CSI
 ↓
PVC/PV
```

A practical lab should use the official Rook release manifests appropriate to the selected version, then apply a CephCluster and RBD StorageClass.

Version-specific manifests should be pinned rather than using `latest`.
