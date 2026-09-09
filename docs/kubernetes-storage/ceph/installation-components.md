# 🔵 Ceph Installation & Component Reference

<p align="center"><strong>Six-Node Lab • Ceph Core • RADOS • RBD • Ceph-CSI • Kubernetes</strong></p>

---

## 🎯 Purpose

This document reconstructs the **component model and installation sequence** for a Ceph RBD environment integrated with Kubernetes.

The goal is not to claim the exact historical commands used in the original lab. The original environment was implemented approximately a year ago, so this document intentionally separates:

- what is required by the architecture,
- what is optional,
- what belongs to Ceph itself,
- what belongs to Kubernetes/CSI,
- and what should be treated as a reference implementation.

> ⚠️ **Evidence boundary:** the documented personal experience is a six-node, 3+3 Ceph lab integrated with Kubernetes and validated through PV/PVC workloads. The exact original installer/orchestrator is not asserted without evidence.

---

# 🧭 01 • Full Component Map

```text
┌──────────────────────────── Kubernetes ────────────────────────────┐
│                                                                    │
│  Application → PVC → StorageClass → Ceph-CSI → PV → Pod           │
│                              │                                     │
│                     ┌────────┴────────┐                            │
│                     │                 │                            │
│               CSI Controller     CSI Node Plugin                   │
│                     │                 │                            │
└─────────────────────┼─────────────────┼────────────────────────────┘
                      │                 │
                      └────────┬────────┘
                               │
                         Ceph RBD API
                               │
                         ┌─────▼─────┐
                         │    RBD    │
                         │ RADOS Block│
                         │   Device  │
                         └─────┬─────┘
                               │
                         ┌─────▼─────┐
                         │   RADOS   │
                         └─────┬─────┘
                               │
                 ┌─────────────┼─────────────┐
                 │             │             │
              ceph-mon      ceph-mgr      ceph-osd
                 │             │             │
                 │             │       Physical storage
                 │             │             │
                 └─────────────┴─────────────┘
                               │
                         CRUSH placement
```

---

# 🧩 02 • Ceph Core Components

## `ceph-mon` — Monitor

The Monitor maintains the authoritative cluster maps and participates in monitor quorum.

Important responsibilities include:

- cluster membership and quorum
- monitor map
- OSD map
- CRUSH map
- authentication information
- cluster state coordination

For a multi-node lab, multiple MON instances provide quorum rather than relying on a single monitor.

**Think:** `MON = cluster coordination and maps`.

---

## `ceph-mgr` — Manager

The Manager provides management and monitoring functionality around the Ceph cluster.

Typical responsibilities include:

- cluster management modules
- metrics and monitoring integration
- exposing operational information
- dashboard/management functionality when enabled

**Think:** `MGR = management, metrics and modules`.

A Manager is not a replacement for MON and does not store the primary application data.

---

## `ceph-osd` — Object Storage Daemon

OSDs are the component that actually stores Ceph data.

An OSD is associated with storage media and participates in:

- data storage
- replication or erasure-coded placement
- recovery
- rebalancing
- scrubbing
- communication with other OSDs

For an RBD deployment, the RBD data ultimately resides through the OSD layer.

**Think:** `OSD = where the distributed data lives`.

---

# 🧠 03 • RADOS, CRUSH and Pools

## RADOS

**RADOS (Reliable Autonomic Distributed Object Store)** is the core distributed storage layer underneath Ceph services.

RBD, CephFS and RGW use RADOS as their underlying storage system.

```text
RBD
 │
 ▼
RADOS
 │
 ▼
OSDs
```

---

## CRUSH

CRUSH determines where objects should be placed across the Ceph cluster.

It allows Ceph to distribute data without requiring a centralized lookup table for every object.

For troubleshooting, CRUSH matters because replica placement, failure domains and rebalancing are part of the storage behavior.

```text
RADOS object
     │
     ▼
   CRUSH
     │
 ┌───┼───┐
 ▼   ▼   ▼
OSD OSD OSD
```

---

## RBD Pool

An RBD pool is a Ceph pool used for RADOS Block Device images.

For Kubernetes dynamic provisioning, the CSI driver creates RBD-backed volumes in the configured pool.

The important distinction is:

```text
Pool ≠ RBD image ≠ PVC
```

They belong to different abstraction layers:

- **Pool** — Ceph storage namespace
- **RBD image** — block volume inside the pool
- **PVC** — Kubernetes request for storage

---

# 🔐 04 • CephX Authentication

Ceph uses **CephX** for authentication and authorization.

Kubernetes/CSI normally needs a dedicated Ceph identity with permissions appropriate for the RBD pool.

Conceptually:

```text
Kubernetes Secret
      │
      │ CephX credentials
      ▼
Ceph-CSI
      │
      ▼
Ceph cluster
      │
      ▼
RBD pool
```

A production-quality configuration should use a **least-privilege CSI identity** rather than a cluster administrator credential.

> Never store real CephX keys in this repository.

---

# ☸️ 05 • Ceph-CSI Components

Ceph-CSI is the Kubernetes integration layer. It implements the Kubernetes **Container Storage Interface (CSI)** and translates Kubernetes storage operations into Ceph operations.

For the RBD driver, the important components are:

### CSI Controller / Provisioner

The controller side handles control-plane storage operations such as:

- CreateVolume
- DeleteVolume
- ControllerExpandVolume
- snapshot-related operations when configured
- interaction with Kubernetes through CSI sidecars

Conceptually:

```text
PVC
 │
 ▼
External Provisioner
 │
 ▼
Ceph-CSI Controller
 │
 ▼
RBD image
```

### CSI Node Plugin

The node plugin runs on Kubernetes nodes and performs node-side volume operations such as:

- NodeStageVolume
- NodePublishVolume
- mounting the volume into the Pod
- unmounting/unpublishing
- node-side expansion operations where applicable

Conceptually:

```text
RBD volume
    │
    ▼
CSI Node Plugin
    │
    ▼
Kubernetes node
    │
    ▼
Pod filesystem
```

### CSI Sidecars

Ceph-CSI deployments normally use Kubernetes CSI sidecars for controller integration. Depending on the driver/version and enabled features, examples include:

- external-provisioner
- external-attacher
- external-resizer
- external-snapshotter
- liveness-probe

Not every sidecar is required for every feature. For example, snapshot support requires the relevant snapshot components and Kubernetes snapshot API support.

---

# 📋 06 • Kubernetes Resources

A functioning RBD-backed Kubernetes StorageClass normally depends on several Kubernetes resources.

| Resource | Purpose |
|---|---|
| `CSIDriver` | Registers the CSI driver with Kubernetes |
| `StorageClass` | Defines dynamic provisioning behavior |
| Secret | Stores Ceph authentication material |
| ConfigMap/configuration | Provides cluster connection information where required |
| RBAC | Allows CSI components to interact with Kubernetes |
| Controller Deployment | Runs CSI controller/provisioning components |
| Node DaemonSet | Runs CSI node functionality on nodes |
| PVC | Requests storage |
| PV | Represents provisioned storage |

For an RBD StorageClass, the driver is normally represented by:

```yaml
provisioner: rbd.csi.ceph.com
```

> Use a version-compatible Ceph-CSI release for the target Kubernetes and Ceph versions. The exact manifest should be pinned rather than relying on an unversioned remote installation URL.

---

# 🏗️ 07 • Reference Installation Sequence

This is the architecture-level installation sequence, not a claim about the exact commands used in the historical lab.

## Phase A — Prepare Nodes

Prepare the six-node lab with:

- supported Linux operating system
- synchronized time
- hostname resolution
- network connectivity between Ceph nodes
- dedicated/available storage devices for OSDs
- required Ceph packages or installer tooling

Avoid using the operating-system disk as an OSD unless the design explicitly supports that layout.

---

## Phase B — Bootstrap the Ceph Cluster

Install/bootstrap the Ceph cluster using the selected Ceph deployment method.

The resulting architecture needs:

```text
MON quorum
   +
MGR
   +
OSDs
   ↓
Healthy Ceph cluster
```

The exact deployment mechanism could vary by Ceph generation and environment. Examples include cephadm-based deployment or other supported methods.

**Do not mix commands from different deployment generations.**

---

## Phase C — Verify Ceph Health

Before connecting Kubernetes, verify the Ceph layer independently.

Typical operational checks include:

```bash
ceph -s
ceph health detail
ceph osd status
ceph osd tree
ceph df
```

The objective is to establish:

```text
Ceph healthy
   ↓
RBD works
   ↓
Only then integrate Kubernetes
```

---

## Phase D — Prepare RBD

Create/configure an RBD pool and initialize it for RBD usage.

Reference flow:

```text
Ceph cluster
    ↓
RADOS pool
    ↓
RBD initialization
    ↓
RBD-ready pool
```

The actual pool name and replication/failure-domain policy should be environment-specific.

---

## Phase E — Create CSI Identity

Create a dedicated CephX identity for the Kubernetes CSI integration.

The identity should have access only to the required pools/resources.

Conceptually:

```text
CSI identity
   │
   ├── read cluster information
   ├── manage RBD images
   └── access configured RBD pool
```

Do not publish the resulting key.

---

## Phase F — Install Ceph-CSI RBD

Deploy the RBD CSI components into Kubernetes.

Expected architecture:

```text
Ceph-CSI
├── Controller
│   ├── provisioner
│   ├── resizer (if enabled)
│   └── other required sidecars
│
└── Node
    └── RBD CSI node plugin
```

Validate:

```bash
kubectl get csidrivers
kubectl get pods -A | grep -i csi
```

---

## Phase G — Configure Kubernetes StorageClass

The StorageClass connects Kubernetes to the Ceph CSI RBD driver.

Sanitized reference:

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ceph-block
provisioner: rbd.csi.ceph.com
parameters:
  clusterID: <ceph-cluster-id>
  pool: <rbd-pool>
  imageFormat: "2"
  imageFeatures: layering
  csi.storage.k8s.io/provisioner-secret-name: <csi-provisioner-secret>
  csi.storage.k8s.io/provisioner-secret-namespace: <namespace>
  csi.storage.k8s.io/node-stage-secret-name: <csi-node-secret>
  csi.storage.k8s.io/node-stage-secret-namespace: <namespace>
reclaimPolicy: Delete
allowVolumeExpansion: true
volumeBindingMode: Immediate
```

This is intentionally a **reference pattern**. Secret names, namespaces, cluster ID, pool and other parameters must match the actual CSI deployment.

---

# 🔄 08 • End-to-End Provisioning

Once everything is installed:

```text
Developer
   │
   │ PVC
   ▼
Kubernetes API
   │
   ▼
StorageClass
   │
   ▼
Ceph-CSI Controller
   │
   │ CreateVolume
   ▼
Ceph RBD
   │
   ▼
RADOS Pool
   │
   ▼
OSDs
```

Then when the Pod starts:

```text
Pod
 │
 ▼
Kubelet
 │
 ▼
Ceph-CSI Node Plugin
 │
 ▼
RBD volume
 │
 ▼
Mounted filesystem
```

This explains why **PVC provisioning and Pod mounting are separate troubleshooting stages**.

---

# 🧪 09 • Validation Layers

Validate from bottom to top.

### Layer 1 — Ceph

```bash
ceph -s
ceph health detail
ceph osd tree
```

### Layer 2 — RBD

Verify the RBD pool and image operations using the appropriate Ceph administration commands.

### Layer 3 — CSI

```bash
kubectl get csidrivers
kubectl get pods -A | grep -i csi
```

### Layer 4 — Kubernetes Storage

```bash
kubectl get storageclass
kubectl get pv
kubectl get pvc -A
```

### Layer 5 — Workload

```bash
kubectl describe pvc <pvc-name> -n <namespace>
kubectl get pod -n <namespace>
kubectl describe pod <pod-name> -n <namespace>
```

Finally test actual read/write behavior from the mounted filesystem.

---

# 🚨 10 • Troubleshooting Matrix

| Failure | First layer to inspect |
|---|---|
| Ceph cluster unhealthy | MON/MGR/OSD/RADOS |
| OSD down/full | OSD and storage devices |
| RBD operation fails | RBD pool / CephX / Ceph health |
| PVC remains Pending | StorageClass / CSI controller / Ceph provisioning |
| PV created but mount fails | CSI node plugin / node-side RBD path |
| Authentication failure | CephX Secret and permissions |
| CSI pods unhealthy | CSI deployment, RBAC, image/configuration |
| Volume expansion fails | CSI resizer + StorageClass + backend support |
| Snapshot feature fails | CSI snapshotter + Kubernetes snapshot API + backend support |

---

# 🚫 11 • Optional Components — Do Not Confuse Them With RBD

These components are valid Ceph technologies but are **not prerequisites for the RBD Kubernetes path** documented here.

### CephFS / MDS

Used for Ceph's POSIX-like distributed filesystem.

```text
CephFS → MDS → RADOS
```

Not required for an RBD-only Kubernetes integration.

### RGW

RADOS Gateway provides object-storage protocols such as S3-compatible access.

```text
S3 → RGW → RADOS
```

Not required for RBD.

### Ceph Dashboard

Useful for management and visualization, but not fundamental to RBD provisioning.

### Rook

Rook is a Kubernetes operator that can orchestrate Ceph. It is a deployment/orchestration choice, not a fundamental Ceph storage component.

If the historical six-node lab was deployed directly on Linux, Rook should not be retroactively inserted into the architecture.

---

# 🧠 12 • The Mental Model to Remember

If you forget the installation details later, remember the layers:

```text
                     USER / APPLICATION
                            │
                           PVC
                            │
                      StorageClass
                            │
                     Ceph-CSI RBD
                      /           \
               Controller       Node
                    │              │
                    └──────┬───────┘
                           RBD
                            │
                          RADOS
                            │
                         CRUSH
                            │
                         OSDs
                            │
                    Physical Storage

MON = cluster maps + quorum
MGR = management + metrics
OSD = data storage
RADOS = distributed storage engine
CRUSH = data placement
RBD = block-device abstraction
CSI = Kubernetes integration
```

That model is the key to reconstructing the environment without memorizing every command.

---

## 🔐 Evidence Boundary

This document intentionally does **not** state that a particular historical installer, Ceph version, operating system, network topology, or exact command sequence was used unless that detail is currently supported by repository evidence.

The personal implementation evidence remains:

- six-node Ceph test environment
- 3+3 layout
- Ceph deployment performed personally
- Kubernetes integration
- RBD-backed persistent-storage testing
- PV/PVC validation

Everything else in the installation sequence is presented as a reusable technical reconstruction/reference.
