# 🔵 Ceph — Six-Node Kubernetes Storage Lab

<p align="center"><strong>Distributed Storage • RBD • CSI • 3+3 Lab • Kubernetes PV/PVC Validation</strong></p>

---

## 🎯 01 • What This Component Solves

Ceph provides distributed storage primitives that can be consumed by Kubernetes for persistent workloads.

This repository documents a **personally deployed six-node Ceph test environment** used for storage evaluation and template/productivity testing.

> ⚠️ **Lab only:** this is not presented as production Ceph infrastructure.

---

## 🧑‍💻 02 • My Hands-On Experience

```text
Ceph Test Environment
├── 3 nodes
└── 3 nodes
    └── 3+3 layout
```

Hands-on scope:

- Deployed the six-node Ceph test environment
- Integrated Ceph with Kubernetes
- Worked with the Kubernetes storage consumption path
- Created PV/PVC test resources
- Validated persistent storage from Kubernetes workloads
- Used the environment for distributed-storage evaluation and template/productivity testing

---

# 🧩 03 • RBD vs CSI — The Important Distinction

A key concept in this repository is that **RBD and CSI are different layers**.

### RBD — RADOS Block Device

**RBD** is the Ceph block-storage interface. It provides block devices backed by Ceph's distributed RADOS storage system.

Conceptually:

```text
Application data
      │
      ▼
   RBD image
      │
      ▼
  Ceph RADOS
      │
      ▼
Distributed Ceph storage
```

RBD is therefore the **storage backend/data path** used to provide block volumes.

### CSI — Container Storage Interface

**CSI** is the Kubernetes storage integration interface. A Ceph CSI driver allows Kubernetes to request and mount Ceph-backed volumes without applications needing to understand Ceph internals.

Conceptually:

```text
Kubernetes
    │
    │ CSI API
    ▼
Ceph CSI Driver
    │
    │ provision / attach / mount
    ▼
Ceph RBD
    │
    ▼
Ceph RADOS
```

CSI is therefore the **integration/control layer between Kubernetes and the storage backend**.

### The relationship

```text
┌─────────────────────────────────────────────┐
│              Kubernetes Workload            │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
                     PVC
                       │
                       ▼
                 StorageClass
                       │
                       ▼
                Ceph CSI Driver
                       │
                       ▼
                  Ceph RBD
                       │
                       ▼
                  Ceph RADOS
                       │
                       ▼
             Distributed Ceph Storage
```

**Short version:**

> **RBD provides the block storage. CSI makes that storage consumable by Kubernetes.**

This distinction is important when troubleshooting. A Kubernetes PVC problem may be caused by the StorageClass/CSI integration even when the underlying Ceph cluster itself is healthy.

---

## 🏗️ 04 • Architecture

```text
                         Kubernetes
                              │
                         PVC request
                              │
                              ▼
                        StorageClass
                              │
                              ▼
                     ┌─────────────────┐
                     │   Ceph CSI      │
                     │    Driver       │
                     └────────┬────────┘
                              │
                         RBD operations
                              │
                              ▼
                     ┌─────────────────┐
                     │   Ceph RBD      │
                     │  Block Device   │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │   Ceph RADOS     │
                     │ Distributed Data │
                     └────────┬────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                 3 nodes             3 nodes
                    │                   │
                    └─────────┬─────────┘
                              ▼
                     Six-Node Ceph Lab
```

---

## ⚙️ 05 • Kubernetes Integration

The repository focuses on the Kubernetes integration and validation side rather than pretending to provide a universal Ceph deployment installer.

The test manifests assume that the target Kubernetes environment already has:

1. A working Ceph cluster/backend
2. A configured **Ceph RBD pool**
3. A working **Ceph CSI RBD driver**
4. A Kubernetes `StorageClass` that uses the CSI driver
5. The required Ceph authentication configuration

A simplified StorageClass relationship looks like:

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ceph-block
provisioner: <ceph-rbd-csi-provisioner>
parameters:
  clusterID: <ceph-cluster-id>
  pool: <rbd-pool>
  imageFormat: "2"
  imageFeatures: layering
reclaimPolicy: Delete
allowVolumeExpansion: true
volumeBindingMode: Immediate
```

> This is a sanitized reference pattern. Values such as cluster IDs, pool names, and authentication configuration must be supplied by the actual Ceph/CSI deployment.

---

## 📦 06 • PV / PVC Provisioning Flow

With dynamic provisioning, Kubernetes does not normally create an RBD image manually for every PVC.

The flow is:

```text
kubectl apply PVC
       │
       ▼
StorageClass
       │
       ▼
Ceph CSI Controller
       │
       ├── Create/provision RBD-backed volume
       │
       ▼
Ceph RBD / RADOS
       │
       ▼
PV created/bound
       │
       ▼
Ceph CSI Node Plugin
       │
       ├── Node-side volume operations
       └── Mount volume into Pod
       │
       ▼
Application Pod
```

This is the most useful mental model for understanding where each component belongs.

---

## 🧪 07 • Validation

The expected path is:

```text
Ceph Backend
     │
     ▼
RBD Pool
     │
     ▼
Ceph CSI
     │
     ▼
StorageClass
     │
     ▼
PVC
     │
     ▼
PV Bound
     │
     ▼
Pod Mount
     │
     ▼
Read / Write Test
```

Useful checks:

```bash
kubectl get storageclass
kubectl get pv
kubectl get pvc -A
kubectl describe pvc <pvc-name> -n <namespace>
kubectl describe pv <pv-name>
```

Check CSI components when troubleshooting provisioning or mounting:

```bash
kubectl get pods -A | grep -i csi
kubectl get csidrivers
kubectl get events -A --sort-by=.lastTimestamp
```

The repository's test manifest is available here:

📁 [`pvc-test.yaml`](../../../manifests/ceph/pvc-test.yaml)

📁 [`validation-pod.yaml`](../../../manifests/ceph/validation-pod.yaml)

---

## 🔧 08 • Operate

For a Kubernetes consumer, day-2 verification focuses on the complete chain rather than checking Ceph alone:

- StorageClass exists and references the expected CSI driver
- CSI controller components are healthy
- CSI node plugins are present on required nodes
- PVC provisioning succeeds
- PV reaches `Bound`
- Volume attachment/mount succeeds
- Pod can read/write the mounted filesystem
- Ceph RBD/RADOS backend remains healthy

### Layered troubleshooting model

```text
PVC Pending
   │
   ├──► StorageClass
   │
   ├──► CSI Controller
   │
   ├──► Ceph RBD pool
   │
   └──► Ceph backend

PVC Bound but Pod cannot mount
   │
   ├──► CSI Node Plugin
   ├──► Volume attachment
   ├──► Node-side mount
   └──► RBD access
```

---

## 🚨 09 • Troubleshoot

| Symptom | Likely layer | First checks |
|---|---|---|
| PVC stays `Pending` | StorageClass / CSI controller / Ceph provisioning | `kubectl describe pvc`, events, CSI controller pods |
| PV is not created | CSI provisioning path | StorageClass, CSI controller logs/events |
| PVC is `Bound`, Pod cannot mount | CSI node path / volume mount | CSI node pods, Pod events |
| RBD volume cannot be provisioned | Ceph RBD / pool / CSI configuration | RBD pool and CSI configuration |
| Mount fails on a node | CSI node plugin / node-side dependencies | Pod events and CSI node components |
| Kubernetes looks healthy but storage fails | Ceph backend | Ceph cluster/backend health |

The important troubleshooting principle is:

> **Do not treat “Ceph is healthy” and “Kubernetes storage is healthy” as the same statement.**

The CSI layer sits between them.

---

## 🧠 10 • Lessons Learned

The lab reinforced three separate abstractions:

| Layer | Responsibility |
|---|---|
| **Ceph RADOS** | Distributed storage backend |
| **Ceph RBD** | Block-volume interface on top of RADOS |
| **Ceph CSI** | Kubernetes integration for provisioning and mounting |

From an application perspective, the backend can remain hidden behind the Kubernetes storage abstraction:

**Application → PVC → StorageClass → CSI → RBD → Ceph RADOS**

This separation makes storage testing reusable and helps isolate failures during troubleshooting.

---

## 🔐 11 • Evidence Boundary

This repository deliberately labels the environment as **test/lab**. It does not claim production deployment, production availability targets, or production operational ownership.

The documented experience is specifically:

- six-node Ceph lab
- 3+3 node layout
- Kubernetes integration
- Ceph-backed persistent-volume testing
- RBD/CSI architecture and troubleshooting understanding

---

<div align="center">

**Distributed Storage → RBD → CSI → Kubernetes**

</div>
