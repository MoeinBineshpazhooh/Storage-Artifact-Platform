# Ceph Components — Practical Mental Model

Ceph becomes much easier to implement when each component has one clear responsibility.

## MON — Monitor

Maintains authoritative cluster maps and quorum. MONs do not normally store application data. A production cluster normally uses an odd number of MONs so quorum can survive failures.

```bash
ceph status
ceph quorum_status --format json-pretty
ceph mon stat
```

## MGR — Manager

Provides management modules, metrics and operational interfaces. MGR daemons can run active/standby.

```bash
ceph mgr stat
ceph mgr module ls
```

## OSD — Object Storage Daemon

OSDs store RADOS objects and handle client I/O, replication, recovery, backfill, scrubbing and rebalancing.

```bash
ceph osd tree
ceph osd status
ceph osd df
```

## RADOS

The distributed object-storage foundation used by Ceph services. RBD, CephFS and RGW are interfaces built on top of RADOS.

## CRUSH

Calculates object placement without a central placement table. CRUSH rules can separate replicas by host, rack or another failure domain.

```bash
ceph osd crush tree
ceph osd crush rule ls
```

## Pool

A logical namespace for RADOS objects. Pool configuration selects replication or erasure coding, a CRUSH rule and PG settings.

## PG — Placement Group

An intermediate placement/recovery unit. Objects map to PGs, and CRUSH maps PGs to OSD sets.

```text
Object → Pool → PG → CRUSH → OSD set
```

PGs are central to peering, recovery and backfill.

## BlueStore

The modern OSD storage backend. It stores Ceph objects directly on block devices and uses RocksDB for metadata.

## RBD

RADOS Block Device provides a block-storage abstraction backed by RADOS. Kubernetes RBD volumes are ultimately RADOS data placed on OSDs.

## CephX

Ceph authentication and authorization. Kubernetes integrations should use a restricted CephX identity rather than an administrator credential.

## Ceph-CSI

The CSI implementation connecting Kubernetes storage APIs to Ceph. Controller components provision/manage volumes; node components stage, publish and mount them.

## CephFS + MDS

CephFS provides a distributed filesystem. MDS manages filesystem metadata. Neither is required for an RBD-only Kubernetes design.

## RGW

RADOS Gateway provides object-storage APIs such as S3. It is separate from RBD block storage.

## Rook

A Kubernetes operator that manages Ceph resources and lifecycle through Kubernetes APIs. It is an orchestration layer, not a replacement for MON/MGR/OSD/RADOS.

## cephadm

A Ceph-native deployment and lifecycle tool that uses the Ceph orchestrator to manage hosts and daemons.

## Dashboard

An optional management/observability interface. Useful operationally, but not required for basic RBD storage.

## Layered troubleshooting

```text
Host / network
      ↓
MON quorum
      ↓
MGR / cluster management
      ↓
OSD
      ↓
PG / CRUSH / pool
      ↓
RBD
      ↓
CephX
      ↓
Ceph-CSI
      ↓
StorageClass
      ↓
PVC / PV
      ↓
Pod mount
```

A Kubernetes error may therefore be caused by a Ceph layer several levels below the PVC.
