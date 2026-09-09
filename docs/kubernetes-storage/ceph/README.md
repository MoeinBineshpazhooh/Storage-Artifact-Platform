# Ceph — Six-Node Storage Lab

## Scope

This is a laboratory implementation used for distributed-storage evaluation and template/productivity testing. It is **not** presented as production infrastructure.

## Environment

- 6 Ceph nodes
- 3+3 layout
- Kubernetes integration
- PV/PVC validation workloads

## Validation flow

```text
Ceph Lab
   │
   ▼
Kubernetes storage integration
   │
   ▼
StorageClass
   │
   ▼
PVC → PV
   │
   ▼
Test workload
```

## Checks

```bash
kubectl get storageclass
kubectl get pv
kubectl get pvc -A
kubectl describe pvc <pvc-name> -n <namespace>
```

For the reusable validation manifest, see [`manifests/ceph/pvc-test.yaml`](../../../manifests/ceph/pvc-test.yaml).
