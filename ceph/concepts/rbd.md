# RBD — Ceph Block Storage

RBD (RADOS Block Device) presents a block-device abstraction backed by RADOS.

```
RBD image
 ↓
RADOS objects
 ↓
Pool / PG / CRUSH
 ↓
OSDs
```

For Kubernetes:

```
PVC → StorageClass → Ceph-CSI → RBD image → RADOS → OSDs
```

RBD image features can include layering, exclusive locking, object-map, fast-diff and journaling. Enable features only when client/CSI compatibility is understood.

Useful commands:

```bash
rbd pool ls
rbd ls <pool>
rbd info <pool>/<image>
rbd status <pool>/<image>
```
