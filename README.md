# 📦 Storage & Artifact Platform

<p align="center">
  <strong>Persistent Storage • Distributed Storage • Object Storage • Artifact Storage</strong>
</p>

<p align="center">
  <em>Implementation-ready infrastructure portfolio for Kubernetes storage, object storage, registries, and artifact repositories.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Kubernetes-Storage-326CE5?logo=kubernetes&logoColor=white" alt="Kubernetes Storage" />
  <img src="https://img.shields.io/badge/Longhorn-Operations-00A3FF" alt="Longhorn" />
  <img src="https://img.shields.io/badge/Ceph-Lab-EF4A2E" alt="Ceph" />
  <img src="https://img.shields.io/badge/MinIO-S3-C72E49?logo=minio&logoColor=white" alt="MinIO" />
  <img src="https://img.shields.io/badge/Harbor-Registry-60B932?logo=harbor&logoColor=white" alt="Harbor" />
  <img src="https://img.shields.io/badge/Nexus-Artifacts-1B1C30" alt="Nexus" />
</p>

---

## 🎯 What this repository demonstrates

This repository connects the storage layers behind a modern Kubernetes platform:

```text
                         ┌──────────────────────────┐
                         │   Kubernetes Workloads   │
                         └────────────┬─────────────┘
                                      │
                   ┌──────────────────┼──────────────────┐
                   │                  │                  │
                   ▼                  ▼                  ▼
              PV / PVC            Images             Packages
                   │                  │                  │
          ┌────────┴───────┐          │          ┌───────┴───────┐
          │                │          │          │               │
      Longhorn           Ceph      Harbor      Nexus          CI/CD
          │                │          │          │
          └────────┬───────┘          │          │
                   │                  │          │
                   ▼                  └────┬─────┘
             Kubernetes                  │
               Storage                   ▼
                                      Artifacts

                         ┌──────────────────────────┐
                         │         MinIO             │
                         │   S3-compatible Object   │
                         │   Storage for ELK Backup  │
                         └──────────────────────────┘
```

The goal is not to collect tutorials. Each section follows the same practical pattern:

**Understand → Implement → Validate → Operate → Troubleshoot**

---

## 🧭 Experience Matrix

| Technology | Evidence level | Practical scope |
|---|---|---|
| 🟢 **Longhorn** | Operational | Kubernetes StorageClass, PV/PVC, application integration, troubleshooting, capacity management |
| 🔵 **Ceph** | Hands-on lab | Personally deployed six-node 3+3 test environment, Kubernetes integration, PV/PVC validation |
| 🟣 **MinIO** | Hands-on integration | Single-node Docker Compose deployment, persistent storage, S3-compatible Elasticsearch snapshots |
| 🟢 **Harbor** | Operational | Private image registry, Kubernetes image pulls, CI/CD and offline/air-gapped image workflows |
| ⚪ **Nexus** | Evidence-controlled | Artifact repository documentation and sanitized templates only where implementation details are validated |

> **Evidence boundary:** production/operational work and laboratory work are deliberately separated. The repository does not claim ownership of platforms implemented by another engineer.

---

## 🗺️ Repository Navigation

| Area | Purpose | Start here |
|---|---|---|
| 🏗️ Architecture | Platform-level design and relationships | [`docs/architecture/`](docs/architecture/) |
| ☸️ Kubernetes Storage | Longhorn + Ceph | [`docs/kubernetes-storage/`](docs/kubernetes-storage/) |
| 🪣 Object Storage | MinIO + ELK snapshots | [`docs/object-storage/`](docs/object-storage/) |
| 📦 Artifact Storage | Harbor + Nexus | [`docs/artifact-storage/`](docs/artifact-storage/) |
| 🧩 Manifests | Implementation-ready sanitized examples | [`manifests/`](manifests/) |
| 🧪 Examples | Generic validation workloads | [`examples/`](examples/) |
| 🔧 Runbooks | Repeatable troubleshooting procedures | [`docs/runbooks/`](docs/runbooks/) |

---

## 🧩 Kubernetes Storage Model

```text
Application
    │
    ▼
   Pod
    │
    ▼
   PVC ───────────────┐
    │                 │
    ▼                 ▼
StorageClass      Application
    │              Integration
    ▼
Provisioner
    │
    ▼
PV / Storage Backend
```

The repository keeps the Kubernetes storage abstraction visible so the technology-specific sections explain **why** a resource exists, not only how to write YAML.

---

## 🟢 Longhorn — Kubernetes Storage Operations

The documented environment was a Kubernetes cluster with **3 control-plane nodes and 18 workers**. The underlying Longhorn platform was implemented by another engineer.

My hands-on scope was the Kubernetes consumption and operational layer:

- StorageClass configuration
- PersistentVolume lifecycle
- PersistentVolumeClaim lifecycle
- Application Deployment integration
- Storage troubleshooting
- Capacity management

### Implementation

```bash
kubectl apply -f manifests/longhorn/storageclass-pvc.yaml
kubectl get storageclass
kubectl get pv
kubectl get pvc
kubectl get pods
```

📁 [Longhorn documentation](docs/kubernetes-storage/longhorn/)

📁 [Longhorn manifests](manifests/longhorn/)

---

## 🔵 Ceph — Six-Node Storage Lab

A six-node Ceph environment was personally deployed as a **test/lab platform**, using a 3+3 layout. It was integrated with Kubernetes and validated through PV/PVC workloads.

```text
                 Ceph Laboratory
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
              Kubernetes Integration
                       │
                    PV / PVC
                       │
                       ▼
                 Test Workload
```

📁 [Ceph documentation](docs/kubernetes-storage/ceph/)

📁 [Ceph validation manifests](manifests/ceph/)

> This section is intentionally labelled **lab** and does not imply production deployment.

---

## 🟣 MinIO — S3-Compatible Storage for ELK Snapshots

MinIO was implemented as a **single-node Docker Compose** service with persistent Docker storage. The practical integration was daily Elasticsearch snapshots to an S3-compatible object-storage backend.

```text
Elasticsearch
     │
     │ Daily Snapshot
     ▼
 S3-compatible API
     │
     ▼
   MinIO
     │
     ▼
 Persistent Storage
```

### Local implementation domain

The portfolio standard is **`moein.local`** for fictional infrastructure endpoints.

Examples:

```text
minio.moein.local
harbor.moein.local
nexus.moein.local
registry.moein.local
```

📁 [MinIO documentation](docs/object-storage/minio/)

📁 [MinIO manifests](manifests/minio/)

---

## 📦 Harbor — Container Image Storage

Harbor represents the container-image storage and distribution layer used by Kubernetes and CI/CD workflows.

```text
Developer / CI
      │
      ▼
 Build Image
      │
      ▼
Harbor Registry
      │
 ┌────┴─────────┐
 ▼              ▼
Kubernetes   Offline Image
Pull         Workflow
```

The examples use `moein.local` and placeholders rather than private registry endpoints or credentials.

📁 [Harbor documentation](docs/artifact-storage/harbor/)

📁 [Harbor manifests](manifests/harbor/)

---

## 📦 Nexus — Artifact Repository

Nexus is kept **evidence-controlled** in this portfolio. Generic repository-manager structure and sanitized templates are provided, while technology-specific implementation claims are added only when supported by validated experience.

📁 [Nexus documentation](docs/artifact-storage/nexus/)

📁 [Nexus manifest area](manifests/nexus/)

---

## 🧪 Implementation Standard

Every technology directory is designed to answer five questions:

```text
┌───────────────┐
│ 1. What is it?│
└───────┬───────┘
        ▼
┌────────────────┐
│ 2. Why use it? │
└───────┬────────┘
        ▼
┌─────────────────┐
│ 3. How deploy?  │
└───────┬─────────┘
        ▼
┌─────────────────┐
│ 4. How validate?│
└───────┬─────────┘
        ▼
┌──────────────────┐
│ 5. How troubleshoot? │
└──────────────────┘
```

This makes the repository useful both as a **portfolio** and as a practical starting point for another engineer.

---

## 🔐 Sanitization Rules

- Fictional infrastructure domain: **`moein.local`**
- No production credentials
- No tokens or passwords
- No private keys
- No internal production endpoints
- Examples use explicit placeholders
- Production and lab environments are clearly labelled
- Manifests are designed to be adapted rather than copied blindly into production

---

## 📁 Repository Structure

```text
Storage-Artifact-Platform/
├── README.md
├── docs/
│   ├── architecture/
│   ├── kubernetes-storage/
│   │   ├── longhorn/
│   │   └── ceph/
│   ├── object-storage/
│   │   └── minio/
│   ├── artifact-storage/
│   │   ├── harbor/
│   │   └── nexus/
│   └── runbooks/
├── manifests/
│   ├── longhorn/
│   ├── ceph/
│   ├── minio/
│   ├── harbor/
│   └── nexus/
├── examples/
│   └── kubernetes/
├── diagrams/
└── .gitignore
```

---

## 🚀 Portfolio Roadmap

- [x] Establish storage/artifact platform scope
- [x] Separate operational and lab evidence
- [x] Standardize `moein.local` fictional domain
- [x] Add implementation-oriented manifest structure
- [x] Add Longhorn consumer manifest + validation workload
- [x] Add Ceph PVC + validation workload
- [x] Add MinIO Compose + environment template
- [x] Add Harbor Kubernetes pull example
- [ ] Expand technology-specific deployment guides
- [ ] Add reusable validation scripts
- [ ] Add troubleshooting runbooks
- [ ] Add architecture diagrams as committed SVG/Mermaid assets
- [ ] Add CI lint/validation for manifests

---

## ⭐ Portfolio Positioning

This repository is designed to show more than familiarity with product names.

It demonstrates the ability to connect:

**Kubernetes workloads → persistent storage → distributed storage → object storage → container images → software artifacts → CI/CD operations.**

The implementation examples are intentionally sanitized so the repository remains safe to share while still being useful to engineers who want to reproduce the concepts quickly.
