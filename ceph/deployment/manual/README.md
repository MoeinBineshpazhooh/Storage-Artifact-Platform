# 🛠 Manual / External Ceph Deployment

This is the practical path for a Ceph cluster deployed independently of Kubernetes and then consumed by Kubernetes through RBD and Ceph-CSI.

## Architecture

```text
Ceph hosts
├── MON
├── MGR
└── OSDs
     ↓
   RADOS
     ↓
    RBD
     ↓
 Ceph-CSI
     ↓
StorageClass
     ↓
  PVC / PV
```

## Build sequence

1. Prepare Linux hosts, disks, DNS/hosts and time synchronization.
2. Prepare Ceph public/client and cluster networks as required.
3. Bootstrap MON quorum.
4. Deploy MGR.
5. Prepare and deploy OSDs.
6. Validate `ceph -s`, OSD state and CRUSH topology.
7. Create an RBD pool and configure replication/PG settings.
8. Create a restricted CephX identity for CSI.
9. Deploy Ceph-CSI in Kubernetes.
10. Create the RBD StorageClass.
11. Provision a PVC and test a workload.
12. Test OSD failure, recovery, capacity and volume operations.

## Why this path matters

This reflects the external-Ceph model used in the historical hands-on experience: the storage cluster is independent from the Kubernetes cluster, while Kubernetes consumes its block storage.

Historical implementation details that cannot be reliably reconstructed are not presented as facts. The runbook is designed as a current, repeatable implementation path.
