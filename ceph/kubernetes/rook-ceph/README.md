# ☸️ Rook-Ceph Kubernetes Lab

This path is for a Kubernetes-native Ceph implementation.

## Components

- Rook Operator
- CephCluster
- MON
- MGR
- OSD
- RBD pool
- Ceph-CSI
- StorageClass
- PVC/PV
- workload test

Use a pinned Rook release and its matching CRDs/operator manifests. Create a CephCluster sized for the available lab nodes/disks, create an RBD pool and StorageClass, then run the supplied PVC/workload tests.

Do not use unpinned `latest` manifests for production.

`operator.yaml` and `cluster.yaml` in this directory contain comments only. They are planning placeholders, not installable resources. Obtain the complete operator/CRDs and cluster configuration for the chosen release before applying the consumer examples. The referenced `replicapool` must also exist.

After the PVC/workload is ready, use the [persistence test](../../../docs/runbooks/persistence-validation.md) to verify data survives Pod replacement.
