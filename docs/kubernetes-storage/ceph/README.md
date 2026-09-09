# 🔵 Ceph — Six-Node Kubernetes Storage Lab

<p align="center"><strong>Distributed Storage • 3+3 Lab • Kubernetes Integration • PV/PVC Validation</strong></p>

---

## 🎯 01 • What This Component Solves

Ceph provides distributed storage primitives that can be integrated with Kubernetes for persistent workloads.

This repository documents a **personally deployed six-node test environment** used for storage evaluation and template/productivity testing.

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
- Created PV/PVC test resources
- Validated Kubernetes storage consumption
- Used the environment for distributed-storage evaluation and template/productivity testing

---

## 🏗️ 03 • Architecture

```text
             ┌─────────────────────┐
             │   Ceph Lab Cluster  │
             └──────────┬──────────┘
                        │
              ┌─────────┴─────────┐
              │                   │
           3 nodes             3 nodes
              │                   │
              └─────────┬─────────┘
                        ▼
                 Ceph Storage
                        │
                        ▼
              Kubernetes CSI Layer
                        │
                        ▼
                  StorageClass
                        │
                        ▼
                    PVC → PV
                        │
                        ▼
                Validation Workload
```

---

## ⚙️ 04 • Implementation

The repository focuses on the Kubernetes integration and validation side rather than pretending to provide a universal Ceph deployment installer.

The test manifest assumes that the target Kubernetes environment already has a working Ceph CSI/storage integration and an appropriate StorageClass.

📁 [`pvc-test.yaml`](../../../manifests/ceph/pvc-test.yaml)

📁 [`validation-pod.yaml`](../../../manifests/ceph/validation-pod.yaml)

---

## 🧪 05 • Validate

The expected path is:

```text
Ceph Backend
     │
     ▼
CSI / Storage Integration
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

---

## 🔧 06 • Operate

For a Kubernetes consumer, day-2 verification focuses on:

- StorageClass availability
- PVC provisioning
- PV binding
- CSI-related events
- Pod scheduling and volume mounting
- Read/write behavior from the workload

---

## 🚨 07 • Troubleshoot

```text
PVC Pending
   │
   ├──► StorageClass
   ├──► CSI integration
   ├──► Provisioning events
   ├──► PV state
   └──► Ceph backend health
```

Start with non-secret evidence:

```bash
kubectl get pvc -A
kubectl get pv
kubectl get storageclass
kubectl get events -A --sort-by=.lastTimestamp
```

---

## 🧠 08 • Lessons Learned

The lab reinforced the difference between a **distributed storage backend** and the **Kubernetes storage abstraction** consuming it.

For application teams, the important path remains:

**Application → PVC → StorageClass → CSI → PV → Ceph**

This separation makes storage testing reusable and keeps application manifests independent from most backend implementation details.

---

## 🔐 Evidence Boundary

This repository deliberately labels the environment as **test/lab**. It does not claim production deployment, production availability targets, or production operational ownership.
