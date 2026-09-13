# 🔵 Ceph Technical Concepts & Implementation Guide

<p align="center"><strong>Components • Data Path • Cluster Formation • Failure Domains • RBD • CSI • Troubleshooting</strong></p>

---

## 🎯 Why This Document Exists

The previous Ceph documentation explained the Kubernetes storage path, but not enough of the Ceph cluster itself. This guide is the technical reference I would want when reconstructing the environment months later.

The personal implementation evidence is a six-node, 3+3 Ceph lab integrated with Kubernetes. The exact historical installer, Ceph release, network layout, disk layout and commands are not claimed unless preserved as evidence.

---

# 01 • The Complete Mental Model

```text
                         Ceph Cluster
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
       MON quorum          MGR services        OSDs
          │                   │                   │
          │                   │              Actual data
          └───────────────────┼───────────────────┘
                              │
                            RADOS
                              │
                 ┌────────────┼────────────┐
                 │            │            │
                RBD         CephFS         RGW
              Block          File         Object
                 │
                 ▼
            Ceph-CSI RBD
                 │
                 ▼
          Kubernetes PVC/PV
```

For this repository, the important path is:

**MON/MGR/OSD → RADOS → CRUSH → Pool/PG → RBD → Ceph-CSI → StorageClass → PVC/PV → Pod**

---

# 02 • MON — Cluster State and Quorum

`ceph-mon` maintains the authoritative cluster maps and participates in monitor quorum.

Important maps include:

- Monitor map
- Manager map
- OSD map
- CRUSH map
- MDS map when CephFS is used

MON does not store application data.

**Think: MON = cluster maps + quorum + authentication coordination.**

### Why multiple MONs?

A single MON creates a control-plane single point of failure. A typical HA design uses 3 or 5 MONs.

```text
MON1 ─┐
MON2 ─┼── quorum
MON3 ─┘
```

With three MONs, losing one still leaves quorum; losing two does not.

Useful checks:

```bash
ceph status
ceph quorum_status --format json-pretty
ceph mon stat
```

---

# 03 • MGR — Management, Metrics and Modules

`ceph-mgr` provides management functionality and runtime information.

Typical responsibilities:

- cluster metrics
- monitoring modules
- management interfaces
- dashboard functionality when enabled
- orchestration interfaces in modern deployments

**Think: MGR = management and operational visibility.**

MGR is not the primary application-data storage daemon.

Useful checks:

```bash
ceph mgr stat
ceph mgr module ls
```

Multiple MGRs can provide active/standby management availability.

---

# 04 • OSD — Where Data Lives

`ceph-osd` stores and serves Ceph data.

OSDs participate in:

- reads and writes
- replication
- recovery
- rebalancing
- scrubbing
- peer communication
- health reporting

**Think: OSD = distributed storage worker.**

An OSD is not simply a mounted Linux disk:

```text
Storage device
    ↓
OSD provisioning
    ↓
OSD identity
    ↓
CRUSH placement
    ↓
ceph-osd daemon
    ↓
BlueStore
    ↓
RADOS objects
```

---

# 05 • BlueStore and OSD Device Preparation

Modern Ceph OSDs normally use BlueStore. It stores Ceph objects directly on block devices and uses metadata structures such as RocksDB.

An available OSD device normally needs to be free of:

- partitions
- filesystem signatures
- old LVM metadata
- previous Ceph OSD metadata
- active mounts

Useful investigation commands:

```bash
lsblk
blkid
pvs
vgs
lvs
```

Modern cephadm deployments also provide:

```bash
ceph orch device ls
```

A disk being visible to Linux does not mean Ceph can safely consume it.

---

# 06 • CRUSH — How Ceph Decides Where Data Goes

CRUSH means **Controlled Replication Under Scalable Hashing**.

Instead of maintaining a centralized object-location lookup, Ceph clients and OSDs calculate placement.

```text
RADOS object
     │
     ▼
    PG
     │
     ▼
   CRUSH
     │
     ├── OSD.1
     ├── OSD.4
     └── OSD.7
```

CRUSH is fundamental to scalability, replication and failure handling.

---

# 07 • CRUSH Hierarchy and Failure Domains

CRUSH can model the physical topology:

```text
root=default
│
├── host=ceph01
│   ├── osd.0
│   └── osd.1
│
├── host=ceph02
│   ├── osd.2
│   └── osd.3
│
└── host=ceph03
    ├── osd.4
    └── osd.5
```

Possible failure domains include host, rack, row, room or site.

Therefore **three replicas does not automatically mean three hosts**. The CRUSH rule and hierarchy determine placement.

Useful commands:

```bash
ceph osd tree
ceph osd crush tree
ceph osd crush rule ls
ceph osd crush rule dump
```

---

# 08 • Pools

A Ceph pool is a logical namespace for RADOS objects.

```text
RBD pool
  ├── image-1
  ├── image-2
  └── image-3
```

Pool configuration influences:

- replication
- CRUSH rule
- placement groups
- failure domain
- recovery behavior

Do not confuse:

- **Pool** — Ceph storage namespace
- **RBD image** — block volume inside the pool
- **PVC** — Kubernetes storage request

---

# 09 • Placement Groups — PGs

Placement Groups provide an important layer of indirection:

```text
RBD object
    ↓
Pool
    ↓
PG
    ↓
CRUSH
    ↓
OSD set
```

CRUSH maps objects to PGs, and PGs to OSD sets. This allows data to move when cluster topology changes.

Useful checks:

```bash
ceph pg stat
ceph pg dump
ceph health detail
```

PGs are therefore important when investigating peering, recovery, backfill and degraded data.

---

# 10 • Replication, Size and min_size

Replicated pools store multiple copies.

```text
size = 3

Object X
  ├── OSD.1
  ├── OSD.4
  └── OSD.7
```

- `size` = desired replica count
- `min_size` = minimum replica availability required for I/O under the pool policy

Example:

```text
size = 3
min_size = 2

One replica unavailable → I/O may continue
Too many unavailable → writes may stop
```

This explains why a cluster can remain partially available while reporting degraded health.

---

# 11 • Health, PG States and Recovery

Common high-level states:

- `HEALTH_OK` — healthy
- `HEALTH_WARN` — attention required
- `HEALTH_ERR` — serious condition

A healthy replicated pool commonly reaches:

```text
active+clean
```

After an OSD failure:

```text
OSD failure
    ↓
PG degraded
    ↓
Recovery / backfill
    ↓
Replica restored
    ↓
active+clean
```

Useful commands:

```bash
ceph -s
ceph health detail
ceph pg stat
```

Recovery and backfill consume network, disk and CPU resources. Capacity planning must include recovery headroom.

---

# 12 • Public and Cluster/Data Networks

Ceph environments can separate traffic classes:

```text
              Ceph Nodes
             /          \
      Public Network   Cluster Network
           │                │
     client traffic     OSD replication
     MON access         recovery/backfill
```

A lab may use one network. Larger deployments can separate client-facing traffic from internal replication/recovery traffic.

The exact historical network design of the six-node lab is intentionally not invented here.

---

# 13 • CephX Authentication

CephX authenticates Ceph clients and daemons.

Kubernetes CSI therefore needs credentials:

```text
Kubernetes Secret
      ↓
CephX identity
      ↓
Ceph-CSI
      ↓
Ceph cluster
      ↓
RBD pool
```

A strong design separates administrative and workload identities:

```text
client.admin
   └── cluster administration

client.csi-rbd
   └── restricted RBD access
```

Never publish real keys.

---

# 14 • RBD — Block Storage Layer

RBD is the block-device interface built on RADOS.

```text
RBD image
    ↓
block device
    ↓
filesystem
    ↓
application
```

RBD supports features such as:

- layering
- striping
- exclusive locking
- object-map
- fast-diff
- journaling

Not every feature is required for a basic Kubernetes workload. Client, kernel and CSI compatibility must be considered before enabling features.

---

# 15 • Ceph-CSI — Kubernetes Integration

Kubernetes does not natively know how to create and mount a Ceph RBD image. CSI provides the standard integration interface.

```text
Kubernetes
    │
    │ CSI API
    ▼
Ceph-CSI
    │
    ▼
Ceph RBD
```

### Controller side

Typical responsibilities include:

- CreateVolume
- DeleteVolume
- controller-side expansion
- snapshot-related operations when configured

### Node side

Typical responsibilities include:

- NodeStageVolume
- NodePublishVolume
- mount
- unmount
- node-side volume operations

Therefore **PVC Pending** and **Pod mount failure** are different troubleshooting stages.

---

# 16 • CSI Sidecars and Kubernetes Resources

Depending on the enabled features, Ceph-CSI deployments can use:

- external-provisioner
- external-attacher
- external-resizer
- external-snapshotter
- liveness-probe

Kubernetes resources involved can include:

- `CSIDriver`
- ServiceAccounts
- ClusterRoles/RoleBindings
- Secrets
- ConfigMaps
- controller Deployments
- node DaemonSets
- StorageClasses
- PVs
- PVCs

Typical RBD driver identifier:

```yaml
provisioner: rbd.csi.ceph.com
```

---

# 17 • Full Kubernetes Provisioning Path

```text
PVC
 ↓
StorageClass
 ↓
External Provisioner
 ↓
Ceph-CSI Controller
 ↓
CephX authentication
 ↓
Ceph MON
 ↓
RBD pool
 ↓
RADOS
 ↓
CRUSH
 ↓
PG
 ↓
OSD set
 ↓
RBD image
 ↓
PV Bound
 ↓
Pod scheduled
 ↓
Ceph-CSI Node Plugin
 ↓
RBD mapped/staged
 ↓
filesystem mounted
 ↓
Pod reads/writes
```

This is the most important troubleshooting map in the repository.

---

# 18 • Why Implementation Can Fail at Every Layer

| Symptom | Possible layer |
|---|---|
| MON quorum lost | MON/network/time |
| MGR unavailable | MGR placement/service |
| OSD down | disk/device/daemon/network |
| OSD up but cluster degraded | PG/replication/recovery |
| Cluster near full | capacity/OSD imbalance/pool usage |
| RBD image creation fails | pool/CRUSH/CephX/RBD |
| PVC Pending | StorageClass/CSI controller/auth/Ceph |
| PV Bound but mount fails | CSI node/RBD mapping/node dependencies |
| Pod sees filesystem error | node mount/filesystem/RBD path |

Do not troubleshoot only from Kubernetes. Trace the entire stack.

---

# 19 • Capacity Management

Raw disk capacity is not equal to safe usable capacity.

Capacity depends on:

- replica size
- CRUSH failure domain
- pool configuration
- OSD balance
- operational headroom
- recovery requirements
- full/near-full thresholds

Useful commands:

```bash
ceph df
ceph osd df
ceph osd pool ls detail
```

An apparently large raw cluster can still have an individual OSD or pool approaching a dangerous threshold.

---

# 20 • OSD Lifecycle

### Add

```text
New disk
  ↓
device validation
  ↓
OSD provisioning
  ↓
OSD joins cluster
  ↓
CRUSH topology updated
  ↓
PG mapping changes
  ↓
data rebalances
```

### Remove

```text
OSD out
  ↓
data migration
  ↓
recovery complete
  ↓
stop/remove OSD
  ↓
clean CRUSH/auth state
  ↓
verify cluster
```

Removing an OSD is therefore not equivalent to deleting a disk.

---

# 21 • Deployment Method Matters

Modern Ceph documentation recommends **cephadm** for new deployments.

Conceptually:

```text
cephadm bootstrap
      ↓
MON + MGR
      ↓
add hosts
      ↓
deploy services
      ↓
deploy OSDs
      ↓
manage lifecycle
```

Rook is a different orchestration model for running Ceph with Kubernetes.

The historical six-node lab should not be retroactively labeled cephadm, Rook or manual deployment without evidence.

---

# 22 • Modern cephadm Reference

Current reference flow:

```text
Prepare Linux hosts
      ↓
Install cephadm
      ↓
bootstrap
      ↓
MON + MGR
      ↓
add remaining hosts
      ↓
discover storage devices
      ↓
create OSDs
      ↓
configure CRUSH/pools
      ↓
create RBD pool
      ↓
create CSI CephX identity
      ↓
install Ceph-CSI
      ↓
create StorageClass
      ↓
test PVC
```

Reference commands:

```bash
cephadm bootstrap --mon-ip <mon-ip>
ceph orch host ls
ceph orch device ls
ceph orch daemon add osd <host>:<device>
ceph status
```

These are current reference commands, not claims about the historical lab.

---

# 23 • Components You Do NOT Need for RBD

### CephFS / MDS

Required for CephFS, not RBD.

```text
CephFS → MDS → RADOS
```

### RGW

Provides object-storage interfaces such as S3-compatible access.

```text
S3 → RGW → RADOS
```

Not required for RBD.

### Rook

Kubernetes operator/orchestration layer for Ceph, not a fundamental Ceph daemon.

### Dashboard

Useful for visibility and management, but not required for basic RBD storage.

---

# 24 • Practical Validation Checklist

### Host

- [ ] Hostnames resolve
- [ ] Time synchronization works
- [ ] Required network paths work
- [ ] Management/SSH access works
- [ ] OSD devices are identified
- [ ] OS disks are not accidentally selected

### Ceph

- [ ] MON quorum healthy
- [ ] MGR active/standby healthy
- [ ] OSDs are `up`
- [ ] OSDs are `in`
- [ ] CRUSH hierarchy is correct
- [ ] Pools exist
- [ ] PGs are healthy
- [ ] Replication/failure domain is understood
- [ ] Capacity has sufficient headroom

### RBD

- [ ] RBD pool exists
- [ ] Pool is initialized for RBD
- [ ] RBD operations work
- [ ] CSI CephX identity exists
- [ ] Permissions are appropriate

### Kubernetes

- [ ] Ceph-CSI controller healthy
- [ ] CSI node plugin healthy
- [ ] `CSIDriver` registered
- [ ] Secrets configured
- [ ] StorageClass configured
- [ ] PVC provisions
- [ ] PV becomes Bound
- [ ] Pod mounts the volume
- [ ] Read/write test succeeds

---

# 25 • Troubleshooting Decision Tree

```text
                    Storage problem
                          │
                          ▼
                   Is Ceph healthy?
                    /            \
                  NO              YES
                  │                │
             MON/MGR/OSD      Is RBD healthy?
                                  /       \
                                NO         YES
                                │           │
                         Pool/RBD/Auth   Is CSI healthy?
                                            /      \
                                          NO        YES
                                          │          │
                                    Controller/   Is PVC
                                    Node/RBAC     healthy?
                                                   /   \
                                                 NO     YES
                                                 │       │
                                           StorageClass  Pod
                                           /CSI/PVC     mount
                                                       │
                                                       ▼
                                                  Node plugin
                                                  RBD mapping
                                                  filesystem
```

---

# 26 • What I Should Remember a Year Later

```text
MON   = cluster maps + quorum
MGR   = management + metrics
OSD   = data storage
RADOS = distributed object store
CRUSH = placement algorithm
Pool  = logical storage namespace
PG    = placement/recovery unit
RBD   = block-device abstraction
CephX = authentication/authorization
CSI   = Kubernetes storage integration
SC    = provisioning policy
PVC   = storage request
PV    = provisioned volume
Pod   = consumer
```

**The key implementation lesson:** when storage fails, identify the layer first. Do not assume a Kubernetes storage error is a Kubernetes problem.

---

## 📚 Official References

- Ceph Architecture: https://docs.ceph.com/en/latest/architecture/
- Ceph Storage Cluster: https://docs.ceph.com/en/latest/architecture/storage-cluster/
- Scalability and HA: https://docs.ceph.com/en/latest/architecture/scalability-high-availability/
- Dynamic Cluster Management: https://docs.ceph.com/en/latest/architecture/dynamic-cluster-management/
- Cephadm Deployment: https://docs.ceph.com/en/latest/cephadm/install/
- Manual Deployment: https://docs.ceph.com/en/latest/install/manual-deployment/
- Ceph RBD: https://docs.ceph.com/en/latest/rbd/
- Ceph-CSI: https://github.com/ceph/ceph-csi

---

## 🔐 Evidence Boundary

Confirmed personal experience:

- six-node Ceph test environment
- 3+3 layout
- Ceph deployed personally
- Kubernetes integration
- RBD/CSI storage consumption
- PV/PVC testing

Not asserted without evidence:

- exact historical Ceph version
- exact installer/orchestrator
- exact network topology
- exact disk/OSD layout
- exact historical commands

The technical concepts are documented so the repository remains useful without turning uncertain memories into false portfolio claims.