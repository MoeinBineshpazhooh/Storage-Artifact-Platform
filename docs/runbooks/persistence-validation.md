# Validate PVC Persistence

Use a disposable lab workload and an existing, healthy storage backend. Run commands from the repository root. The helper writes a unique marker into the mounted PVC, reads it, restarts the selected Deployment, verifies that the Pod UID changed, and compares the marker after replacement. A successful read before replacement alone does not prove persistence.

## Generic test

1. Copy `examples/kubernetes/storage-test.yaml` locally and replace `REPLACE_WITH_STORAGE_CLASS` with the installed class name.
2. Review and apply that edited file.
3. Wait for the Deployment and run:

```bash
kubectl -n storage-lab rollout status deployment/storage-test --timeout=300s
python scripts/check-persistence.py --namespace storage-lab --deployment storage-test
```

## Existing examples

| Example | Prerequisite | Helper arguments |
|---|---|---|
| Longhorn | Healthy Longhorn CSI and the reviewed consumer manifest | `--namespace default --deployment longhorn-storage-test` |
| External Ceph | Ceph-CSI configuration, pool, CephX Secret, StorageClass and PVC | `--namespace default --deployment ceph-rbd-test` |
| Rook Ceph | Matching installed Rook release, CephCluster, pool, StorageClass and PVC | `--namespace default --deployment rook-ceph-rbd-test` |

If you deploy the Ceph examples into another namespace, pass that namespace. The helper requires one replica, a `Recreate` update strategy, a simple label selector, and exactly one container mounting a PVC at `/data`. Use it only on the selected lab Deployment: it deliberately restarts the Pod and causes brief downtime. The container must provide `sh`, `cat`, `sync`, and `rm`.

The test Deployments use `Recreate` to avoid a rolling update creating overlapping consumers of one volume. `ReadWriteOnce` restricts write mounting to one node; it does not guarantee that only one Pod can access the volume on that node. This is a lab update strategy, not a production availability design.

On failure, inspect Pod events, PVC/PV state and CSI/backend health. The marker may remain for investigation. This test does not prove cross-node recovery, backend fault tolerance, backup integrity or restore capability.

## Data lifecycle

Keep the PVC while testing pod replacement. The example StorageClasses use `reclaimPolicy: Delete`; deleting the PVC can also delete its dynamically provisioned backing volume. Inspect the bound PV's policy before cleanup. Do not delete the namespace, PVC or backing volume to test persistence. Production data needs its own backup/restore and retention procedure.

References: [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) and [Deployment strategies](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/).
