# 📦 Storage & Artifact Platform

<p align="center">
  <img src="https://github.com/MoeinBineshpazhooh.png?size=160" width="120" alt="Moein Bineshpazhooh" />
</p>

<p align="center">
  <strong>Persistent Storage • Distributed Storage • Object Storage • Artifact Repositories</strong>
</p>

<p align="center"><em>Hands-on DevOps infrastructure portfolio built around real implementation evidence, reusable manifests, validation workflows, and operational lessons.</em></p>

<p align="center">
<img src="https://img.shields.io/badge/Kubernetes-Storage-326CE5?logo=kubernetes&logoColor=white" />
<img src="https://img.shields.io/badge/Longhorn-Operations-00A3FF" />
<img src="https://img.shields.io/badge/Ceph-Lab-EF4A2E" />
<img src="https://img.shields.io/badge/MinIO-S3-C72E49?logo=minio&logoColor=white" />
<img src="https://img.shields.io/badge/Harbor-Registry-60B932?logo=harbor&logoColor=white" />
<img src="https://img.shields.io/badge/JFrog-Artifactory-41B883?logo=jfrog&logoColor=white" />
</p>

---

## 🎯 What I Actually Implemented

| Technology | Experience | What is documented |
|---|---|---|
| 🟢 **Longhorn** | Operational | Kubernetes StorageClass, PV/PVC, application integration, troubleshooting, capacity management |
| 🔵 **Ceph** | Hands-on lab | Personally deployed 6-node 3+3 test environment and integrated it with Kubernetes for PV/PVC validation |
| 🟣 **MinIO** | Hands-on integration | Single-node Docker Compose deployment with persistent storage; S3 backend for daily Elasticsearch snapshots |
| 🟢 **Harbor** | Operational | Private container registry used by Kubernetes, CI/CD and offline/air-gapped workflows |
| 🟢 **JFrog Artifactory** | Operational usage | Used as an artifact/package proxy layer with remote, private and local repositories; GitLab CI/CD consumed repositories for dependency restore |
| ⚪ **Nexus** | Reference | Kept as a repository-manager reference area; no unsupported personal implementation claims |

> **Evidence boundary:** production/operational work, lab work, and reference material are explicitly separated. The repository does not claim platform ownership where the underlying platform was implemented by another engineer.

---

## 🏗️ Architecture

```text
                           STORAGE & ARTIFACT PLATFORM
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
        ▼                             ▼                             ▼
 Persistent / Block             Object Storage               Artifact Storage
        │                             │                             │
   ┌────┴────┐                      MinIO              ┌────────────┼────────────┐
   │         │                        │                │            │            │
Longhorn   Ceph                 ELK Snapshots       Harbor       JFrog        Nexus
   │         │                                         │        Artifactory   │
   ▼         ▼                                         ▼            │            ▼
 PV/PVC    PV/PVC                                   Images     Packages /      Reference
   │         │                                                  Dependencies
   └─────────┴──────────────────────┬──────────────────────────────┘
                                    ▼
                              Kubernetes / CI/CD
```

### Traffic & Artifact Flow

```text
Developer
   │
   ▼
GitLab CI/CD
   │
   ├──────────────► Harbor ─────────► Kubernetes image pull
   │
   └──────────────► JFrog Artifactory
                         │
                         ├── Remote repositories
                         ├── Private repositories
                         └── Local repositories
                                  │
                                  ▼
                           Dependency restore

Elasticsearch ──► S3 API ──► MinIO ──► Snapshot storage

Kubernetes workload ──► PVC ──► StorageClass ──► Longhorn / Ceph
```

---

## 🧭 Why These Technologies Belong Together

A platform needs several different storage models rather than one universal storage system:

- **Block / persistent storage** → application volumes and Kubernetes PV/PVC.
- **Distributed storage** → resilient storage experimentation and Kubernetes integration.
- **Object storage** → backups and snapshots through S3-compatible APIs.
- **Container registry** → OCI/container images required by Kubernetes and CI/CD.
- **Artifact repository** → packages and dependencies consumed by build pipelines.

The repository therefore focuses on the complete path from **workload → data → image → dependency → delivery**.

---

## ☸️ Longhorn — Kubernetes Storage Operations

### Environment

- Kubernetes cluster
- 3 control-plane nodes
- 18 worker nodes
- Longhorn platform implemented by another engineer

### My hands-on scope

- StorageClass configuration
- PersistentVolume lifecycle
- PersistentVolumeClaim lifecycle
- Application Deployment integration
- Storage troubleshooting
- Capacity management

### Quick validation

```bash
kubectl apply -f manifests/longhorn/storageclass-pvc.yaml
kubectl get storageclass
kubectl get pv
kubectl get pvc
kubectl get pods
```

📁 [`docs/kubernetes-storage/longhorn/`](docs/kubernetes-storage/longhorn/)

📁 [`manifests/longhorn/`](manifests/longhorn/)

---

## 🔵 Ceph — Six-Node Storage Lab

A dedicated **six-node test environment** was personally deployed using a 3+3 layout.

```text
             Ceph Lab
                │
        ┌───────┴───────┐
        │               │
     3 nodes          3 nodes
        │               │
        └───────┬───────┘
                ▼
          Ceph Storage
                │
                ▼
       Kubernetes Integration
                │
             PV / PVC
                │
                ▼
          Validation Workload
```

Purpose:

- Distributed-storage evaluation
- Kubernetes integration testing
- PV/PVC validation
- Template/productivity testing

> **Lab only:** this is not presented as production Ceph infrastructure.

📁 [`docs/kubernetes-storage/ceph/`](docs/kubernetes-storage/ceph/)

📁 [`manifests/ceph/`](manifests/ceph/)

---

## 🟣 MinIO — S3 Object Storage for ELK Snapshots

MinIO was personally implemented as a **single-node Docker Compose service** with persistent storage.

```text
Elasticsearch
      │
      │ Daily snapshot
      ▼
 S3-compatible API
      │
      ▼
    MinIO
      │
      ▼
Persistent object data
```

The practical use case is storing daily Elasticsearch snapshots in an S3-compatible backend.

### Sanitized endpoints

```text
minio.moein.local
harbor.moein.local
registry.moein.local
```

📁 [`docs/object-storage/minio/`](docs/object-storage/minio/)

📁 [`manifests/minio/`](manifests/minio/)

---

## 🐳 Harbor — Container Image Storage

Harbor is the container-image layer used in the documented Kubernetes and CI/CD workflows.

```text
GitLab CI/CD
     │
     ▼
 Build Image
     │
     ▼
harbor.moein.local
     │
 ┌───┴──────────────┐
 ▼                  ▼
Kubernetes       Offline / Air-Gapped
Pull             Image Workflow
```

The repository contains sanitized Kubernetes pull examples and deliberately excludes real registry credentials and internal endpoints.

📁 [`docs/artifact-storage/harbor/`](docs/artifact-storage/harbor/)

📁 [`manifests/harbor/`](manifests/harbor/)

---

## 🟢 JFrog Artifactory — Dependency & Artifact Proxy Layer

JFrog belongs here and is a **real operational part of the artifact-storage story**.

The documented usage is not "I deployed Artifactory." The accurate claim is:

> **Used JFrog Artifactory as a repository/proxy layer, working with remote, private and local repositories and connecting GitLab CI/CD dependency restoration to the appropriate repositories.**

### Architecture

```text
                         GitLab CI/CD
                              │
                              ▼
                     Package / Dependency
                           Restore
                              │
                              ▼
                    JFrog Artifactory
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
        Remote Repo       Private Repo      Local Repo
             │                │                │
             └────────────────┼────────────────┘
                              ▼
                       Build Dependency
```

### Why it matters

This demonstrates an important distinction:

**Harbor stores container images; Artifactory serves package/artifact dependencies.**

The CI/CD pipeline can therefore consume packages through a controlled internal repository layer rather than allowing every build job to depend directly on external package sources.

### Fictional endpoint

```text
artifactory.moein.local
```

Credentials, tokens and private repository URLs are intentionally excluded.

📁 [`docs/artifact-storage/jfrog-artifactory/`](docs/artifact-storage/jfrog-artifactory/)

📁 [`manifests/jfrog-artifactory/`](manifests/jfrog-artifactory/)

---

## ⚪ Nexus — Repository Manager Reference

Nexus remains in the repository as a **reference/implementation-template area**, not as a stronger personal claim than the evidence supports.

📁 [`docs/artifact-storage/nexus/`](docs/artifact-storage/nexus/)

📁 [`manifests/nexus/`](manifests/nexus/)

---

## 🧪 Implementation Standard

Every component follows the portfolio's implementation pattern:

```text
┌──────────────────┐
│ 01 • WHAT        │  Purpose / responsibility
└────────┬─────────┘
         ▼
┌──────────────────┐
│ 02 • ARCHITECTURE│  Where it fits
└────────┬─────────┘
         ▼
┌──────────────────┐
│ 03 • IMPLEMENT   │  Ready-to-adapt manifests
└────────┬─────────┘
         ▼
┌──────────────────┐
│ 04 • VALIDATE    │  Commands / expected state
└────────┬─────────┘
         ▼
┌──────────────────┐
│ 05 • OPERATE     │  Day-2 workflow
└────────┬─────────┘
         ▼
┌──────────────────┐
│ 06 • TROUBLESHOOT│  Symptom → Evidence → Fix
└──────────────────┘
```

---

## 🔍 Validation Philosophy

A manifest is not considered useful merely because it is valid YAML.

Validation should prove the complete path:

```text
Configuration
     │
     ▼
Resource Created
     │
     ▼
Backend Ready
     │
     ▼
Workload Uses Resource
     │
     ▼
Read / Write or Pull / Restore
     │
     ▼
Expected Result
```

---

## 🔧 Troubleshooting Model

```text
SYMPTOM
   │
   ▼
OBSERVE
   │
   ▼
COLLECT NON-SECRET EVIDENCE
   │
   ▼
TRACE THE DEPENDENCY CHAIN
   │
   ▼
ROOT CAUSE
   │
   ▼
RECOVERY
   │
   ▼
VALIDATE
   │
   ▼
LESSON LEARNED
```

Examples include PVC provisioning, volume attachment/mount problems, capacity issues, image pulls, package restore failures, and repository connectivity.

---

## 🌐 Portfolio-Wide Fictional Domain

All fictional infrastructure addresses in the GitHub portfolio use:

```text
moein.local
```

Examples:

```text
harbor.moein.local
registry.moein.local
artifactory.moein.local
nexus.moein.local
minio.moein.local
gitlab.moein.local
k8s.moein.local
```

This keeps examples consistent across repositories while clearly separating them from real infrastructure.

---

## 🔐 Engineering & Safety Principles

- Production and lab claims are separated.
- Sensitive infrastructure endpoints are sanitized.
- Credentials, passwords, tokens and private keys never belong in Git.
- Real production logs are not committed.
- Manifests use placeholders and fictional domains.
- Examples are implementation-oriented but must still be reviewed for the target environment.
- Product capabilities are not presented as personal implementation unless supported by evidence.

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
│   │   ├── jfrog-artifactory/
│   │   └── nexus/
│   └── runbooks/
├── manifests/
│   ├── longhorn/
│   ├── ceph/
│   ├── minio/
│   ├── harbor/
│   ├── jfrog-artifactory/
│   └── nexus/
├── examples/
├── diagrams/
└── .gitignore
```

---

## 🚀 Portfolio Checklist

- [x] Evidence-first storage scope
- [x] Longhorn operational boundary
- [x] Ceph six-node lab boundary
- [x] MinIO + ELK snapshot workflow
- [x] Harbor registry workflow
- [x] JFrog Artifactory dependency/proxy workflow
- [x] Portfolio-wide `moein.local` domain
- [x] Sanitized implementation manifests
- [ ] Complete technology-specific deployment runbooks
- [ ] Add reusable validation scripts
- [ ] Add committed Mermaid/SVG architecture assets
- [ ] Add CI validation for Kubernetes YAML

---

## ⭐ Portfolio Positioning

This repository demonstrates practical infrastructure thinking across multiple storage models:

**Kubernetes workloads → persistent volumes → distributed storage → object snapshots → container images → package dependencies → GitLab CI/CD.**

The goal is a repository that an engineer can **understand quickly, implement safely, validate confidently, and operate afterward**.
