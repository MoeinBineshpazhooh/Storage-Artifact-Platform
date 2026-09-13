# RADOS and the Ceph Data Path

RADOS is the distributed object storage layer at the center of Ceph.

For an RBD workload:

```
Application
  ↓
Filesystem
  ↓
RBD image
  ↓
RADOS objects
  ↓
Pool
  ↓
PG
  ↓
CRUSH
  ↓
OSD set
  ↓
OSD / BlueStore
```

RBD is not the physical storage engine. RBD presents a block abstraction; RADOS distributes the underlying objects.

Useful checks:

```bash
ceph -s
ceph health detail
ceph df
rbd pool ls
rbd ls <pool>
```
