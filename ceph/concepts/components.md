# Ceph Components — What Each One Does

## MON — Monitor

Maintains cluster maps and quorum. MON is control-plane state, not application-data storage.

Key concepts:
- monitor quorum
- cluster maps
- authentication coordination

```bash
ceph status
ceph quorum_status --format json-pretty
ceph mon stat
```

## MGR — Manager

Provides management services, metrics and modules. Multiple MGRs can provide active/standby availability.

```bash
ceph mgr stat
ceph mgr module ls
```

## OSD — Object Storage Daemon

Stores RADOS objects and performs reads/writes, replication, recovery, backfill, scrubbing and rebalancing.

```bash
ceph osd tree
ceph osd status
ceph osd df
```

## RADOS

The distributed object-store foundation underneath Ceph services. RBD, CephFS and RGW ultimately use RADOS.

## CRUSH

Calculates placement through pools, PGs and the CRUSH hierarchy. It can enforce failure domains such as host or rack.

```bash
ceph osd crush tree
ceph osd crush rule ls
```

## Pool

Logical namespace for RADOS objects. Pool settings determine replication or erasure coding, CRUSH rule and PG configuration.

## PG — Placement Group

A placement/recovery unit between objects and OSD sets.

```
Object → Pool → PG → CRUSH → OSD set
```

PGs are central to peering, recovery and backfill.

## BlueStore

The modern OSD storage backend. It stores Ceph objects directly on block devices and uses metadata structures such as RocksDB.

## RBD

Block-device abstraction on top of RADOS. An RBD image becomes the storage volume used by RBD clients and Ceph-CSI.

## CephX

Authentication and authorization mechanism for Ceph identities.

## Ceph-CSI

CSI implementation that connects Kubernetes storage APIs to Ceph. Controller components provision/manage volumes; node components stage/publish/mount them.

## CephFS / MDS

CephFS provides a distributed filesystem. MDS manages filesystem metadata. MDS is not required for RBD.

## RGW

Object gateway providing S3-compatible/object-storage access. RGW is not required for RBD.

## Rook

Kubernetes operator that manages Ceph lifecycle from Kubernetes. Rook is an orchestration layer, not a fundamental Ceph daemon.

## Dashboard

Optional management/visibility interface. Not required for basic RBD storage.

### Troubleshooting rule

When Kubernetes reports a storage problem, trace:

```
PVC → StorageClass → CSI → CephX → MON → Pool/RBD → PG/CRUSH → OSD
```

The visible error may be several layers away from the root cause.
