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
