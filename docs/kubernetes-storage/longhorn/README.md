# 🟢 Longhorn — Kubernetes Storage Operations

<p align="center"><strong>Persistent Volumes • StorageClass • Application Integration • Day-2 Operations</strong></p>

---

## 🎯 What This Component Solves

Longhorn provides persistent block storage for Kubernetes workloads.

This section focuses on practical Kubernetes storage consumption: PV/PVC lifecycle, workload integration, validation, and troubleshooting.

---

## 🧑‍💻 Experience Boundary

### Environment

```text
Kubernetes Cluster
├── 3 Control-Plane Nodes
└── 18 Worker Nodes
```

The Longhorn platform itself was implemented by another engineer.

My practical scope:

| Area | Hands-on scope |
|---|---|
| StorageClass | Configuration and usage |
| PV | Lifecycle and troubleshooting |
| PVC | Creation and validation |
| Applications | Persistent volume integration |
| Operations | Capacity and storage issue investigation |

This repository separates platform ownership from operational experience.

---

## 🏗️ Architecture

```text
Application Pod
      |
      v
PersistentVolumeClaim
      |
      v
PersistentVolume
      |
      v
StorageClass
      |
      v
Longhorn Storage Backend
```

The important Kubernetes storage chain:

```text
Workload → PVC → StorageClass → Provisioner → PV → Storage Backend
```

---

## ⚙️ Implementation Example

Example validation workflow:

```bash
kubectl get storageclass
kubectl get pv
kubectl get pvc -A
kubectl describe pvc <name> -n <namespace>
```

A successful storage test should prove:

```text
StorageClass
      |
      v
PVC Bound
      |
      v
PV Created
      |
      v
Pod Scheduled
      |
      v
Volume Mounted
      |
      v
Application Read/Write
```

---

## 🔧 Day-2 Operations

Common operational activities:

- Investigate Pending PVCs
- Validate volume attachment
- Check application mounts
- Review capacity usage
- Troubleshoot storage-related deployment failures

---

## 🚨 Troubleshooting Flow

```text
PVC Pending
   |
   ├── Check StorageClass
   ├── Check Kubernetes Events
   ├── Check PV creation
   ├── Check provisioner status
   └── Check Longhorn backend health
```

Useful commands:

```bash
kubectl get events -A --sort-by=.lastTimestamp
kubectl get pvc -A
kubectl get pv
kubectl describe pod <pod-name> -n <namespace>
```

---

## 📌 Repository Position

This is a practical Kubernetes storage operations guide, not a Longhorn deployment guide.

The focus is on how a DevOps engineer consumes, validates and operates persistent storage inside Kubernetes environments.
