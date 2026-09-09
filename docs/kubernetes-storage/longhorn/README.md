# 🟢 Longhorn — Kubernetes Storage Operations

<p align="center"><strong>Persistent Volumes • StorageClass • Application Integration • Day-2 Operations</strong></p>

---

## 🎯 01 • What This Component Solves

Longhorn provides the storage backend behind Kubernetes persistent workloads.

The important engineering layer documented here is the **Kubernetes storage consumption and operational workflow** rather than ownership of the underlying Longhorn platform.

---

## 🧑‍💻 02 • My Hands-On Experience

### Environment

```text
Kubernetes Cluster
├── 3 Control-Plane Nodes
└── 18 Worker Nodes
```

The underlying Longhorn platform was implemented by another engineer.

### My scope

| Area | Hands-on scope |
|---|---|
| StorageClass | Configuration and consumption |
| PV | Lifecycle and troubleshooting |
| PVC | Provisioning and lifecycle |
| Workloads | Persistent-volume integration |
| Operations | Troubleshooting and capacity management |

> **Evidence boundary:** this repository does not claim that I designed or deployed the Longhorn platform itself.

---

## 🏗️ 03 • Architecture

```text
Application
     │
     ▼
    Pod
     │
     ▼
    PVC
     │
     ▼
StorageClass
     │
     ▼
Longhorn Provisioner
     │
     ▼
Persistent Volume
     │
     ▼
Longhorn Storage
```

The Kubernetes abstraction is the key operational interface: applications request storage through PVCs while the StorageClass connects that request to the backend.

---

## ⚙️ 04 • Implementation

The repository contains a sanitized consumer-side example:

```bash
kubectl apply -f manifests/longhorn/storageclass-pvc.yaml
```

Inspect the resulting resources:

```bash
kubectl get storageclass
kubectl get pv
kubectl get pvc
kubectl get pods
```

> If the target cluster already has an approved Longhorn StorageClass, reuse it rather than creating a duplicate StorageClass.

📁 [`storageclass-pvc.yaml`](../../../manifests/longhorn/storageclass-pvc.yaml)

---

## 🧪 05 • Validate

A storage test should prove more than PVC creation:

```text
StorageClass
     │
     ▼
PVC Bound
     │
     ▼
PV Created
     │
     ▼
Pod Scheduled
     │
     ▼
Volume Mounted
     │
     ▼
Application Read / Write
```

Useful checks:

```bash
kubectl get pvc -A
kubectl describe pvc <pvc-name> -n <namespace>
kubectl get pv
kubectl describe pv <pv-name>
kubectl describe pod <pod-name> -n <namespace>
```

---

## 🔧 06 • Operate

Typical day-2 activities include:

- Checking PVC/PV state
- Investigating provisioning failures
- Checking capacity-related symptoms
- Reviewing workload volume consumption
- Confirming successful mount/attach behavior
- Validating storage after application changes

---

## 🚨 07 • Troubleshoot

```text
PVC Pending
   │
   ├──► Check StorageClass
   ├──► Check events
   ├──► Check provisioner
   ├──► Check PV creation
   └──► Check Longhorn/backend health
```

Start with non-secret evidence:

```bash
kubectl get pvc -A
kubectl get pv
kubectl get storageclass
kubectl get events -A --sort-by=.lastTimestamp
```

Never place credentials, private endpoints or production logs in this repository.

---

## 🧠 08 • Lessons Learned

The most important operational lesson is that Kubernetes storage problems should be traced through the complete dependency chain rather than treating a PVC as an isolated object:

**Workload → PVC → StorageClass → Provisioner → PV → Storage Backend**

That model makes capacity, provisioning, mount and application-storage failures much easier to isolate.

---

## 📁 Repository Files

- [`manifests/longhorn/`](../../../manifests/longhorn/)
- [`Storage troubleshooting runbook`](../../runbooks/storage-troubleshooting.md)
- [`Architecture`](../../architecture/)
