# 🛠 Manual Ceph Deployment

This path represents an externally managed Ceph cluster: Linux hosts run Ceph daemons and Kubernetes consumes the resulting RBD storage through Ceph-CSI.

This is also the deployment model closest to the historical implementation represented in this portfolio: Ceph was deployed outside Kubernetes and then used by Kubernetes as storage.

## Flow

```
Linux hosts
  ├── MON
  ├── MGR
  └── OSDs
       ↓
     RADOS/RBD
       ↓
    Ceph-CSI
       ↓
   Kubernetes PV/PVC
```

## Suggested sequence

1. Prepare Linux hosts and storage devices.
2. Establish hostname/DNS, time synchronization and network connectivity.
3. Bootstrap MON quorum.
4. Deploy MGR.
5. Prepare and deploy OSDs.
6. Verify OSD `up`/`in` state.
7. Validate CRUSH topology.
8. Create/configure RBD pool.
9. Create a restricted CephX identity for CSI.
10. Deploy Ceph-CSI in Kubernetes.
11. Create StorageClass and test PVC.
12. Test failure/recovery behavior.

Exact historical commands are intentionally not claimed. Use the current Ceph release documentation for the chosen deployment mechanism.
