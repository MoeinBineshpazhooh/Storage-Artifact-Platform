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

These files do not install Ceph-CSI or its cluster configuration. Install a compatible driver and configure the FSID/MON mapping, pool and restricted CephX identity before applying the StorageClass and consumer resources. Create credentials through your secret-management workflow; `secret-example.yaml` is a template only.

Use the [persistence test](../../../docs/runbooks/persistence-validation.md) after the Deployment is ready.

New StorageClasses use Retain. Existing StorageClass fields cannot be assumed to update in place: use a new class name for a revised configuration and review existing PV policies separately. Keep PVCs intact when testing. Retain requires manual cleanup and is not a backup.
