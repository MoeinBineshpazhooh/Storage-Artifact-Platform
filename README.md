# Storage & Artifact Platform

<p align="center">
  <strong>Persistent Storage • Distributed Storage • Object Storage • Artifact Storage</strong>
</p>

<p align="center">
  A hands-on infrastructure portfolio covering Kubernetes storage, distributed storage, S3-compatible object storage, and artifact repositories.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Kubernetes-Storage-326CE5?logo=kubernetes&logoColor=white" alt="Kubernetes Storage" />
  <img src="https://img.shields.io/badge/Longhorn-Storage-00A3FF" alt="Longhorn" />
  <img src="https://img.shields.io/badge/Ceph-Distributed%20Storage-EF4A2E" alt="Ceph" />
  <img src="https://img.shields.io/badge/MinIO-S3%20Storage-C72E49?logo=minio&logoColor=white" alt="MinIO" />
  <img src="https://img.shields.io/badge/Harbor-Container%20Registry-60B932?logo=harbor&logoColor=white" alt="Harbor" />
  <img src="https://img.shields.io/badge/Nexus-Artifact%20Repository-1B1C30" alt="Nexus" />
</p>

---

## 🎯 Repository Purpose

This repository documents practical experience with the storage and artifact infrastructure that supports Kubernetes platforms, applications, observability, and CI/CD workflows.

The focus is **evidence first**: production/operational experience is kept separate from laboratory work and technical reference material.

```text
                         STORAGE & ARTIFACT PLATFORM
                                      │
             ┌────────────────────────┼────────────────────────┐
             │                        │                        │
       Persistent Storage       Object Storage          Artifact Storage
             │                        │                        │
        ┌────┴────┐                  MinIO              ┌───────┴───────┐
        │         │                    │                │               │
     Longhorn   Ceph              S3-compatible      Harbor           Nexus
        │         │                    │                │               │
      PV/PVC   K8s PV/PVC          ELK snapshots     Images        Packages
             │                        │                │               │
             └────────────────────────┴────────────────┴───────────────┘
                                      │
                                Platform Services
```

## 🧭 Experience Scope

| Technology | Experience | Scope |
|---|---|---|
| **Longhorn** | 🟢 Operational | Existing Kubernetes platform; StorageClass/PV/PVC, application integration, troubleshooting, capacity management |
| **Ceph** | 🔵 Hands-on lab | Personally deployed 6-node test environment (3+3), integrated with Kubernetes, PV/PVC validation |
| **MinIO** | 🟣 Hands-on integration | Docker Compose deployment used as S3-compatible storage for daily Elasticsearch snapshots |
| **Harbor** | 🟢 Operational | Private container registry experience supporting Kubernetes and CI/CD workflows |
| **Nexus** | 🟢 Operational | Artifact/package repository experience; documented according to the implementation evidence available |

> **Evidence boundary:** This repository does not present laboratory work as production experience and does not claim platform ownership where the underlying platform was implemented by another engineer.

---

## 🧩 Storage Models

### Persistent / Block Storage

Used when Kubernetes workloads need persistent volumes exposed through the Kubernetes storage model.

**Longhorn** is documented primarily from an operational Kubernetes perspective, including StorageClasses, PV/PVC usage, application integration, troubleshooting, and capacity management.

### Distributed Storage

**Ceph** is documented as a personally deployed laboratory environment used to understand distributed storage and validate Kubernetes integration through PV/PVC test scenarios.

### Object Storage

**MinIO** provides the object-storage layer in the documented ELK snapshot workflow. The implementation used Docker Compose and persistent local storage rather than a distributed MinIO deployment.

### Artifact Storage

**Harbor** and **Nexus** cover a related but distinct problem: storing and serving build artifacts, container images, and packages used by platform and CI/CD workflows.

---

## ☸️ Kubernetes Storage Flow

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
      Storage Provisioner
             │
             ▼
             PV / Backend
```

The repository uses this flow as the common foundation for explaining Kubernetes storage behavior before moving into technology-specific implementations.

---

## 🟢 Longhorn — Kubernetes Storage Operations

Environment: Kubernetes cluster with **3 control-plane nodes and 18 workers**.

The underlying Longhorn platform was implemented by another engineer. My hands-on work was at the Kubernetes consumption and operations layer:

- Created and configured Kubernetes storage resources.
- Worked with **StorageClass, PersistentVolume, and PersistentVolumeClaim** objects.
- Integrated persistent storage with application Deployments.
- Performed storage troubleshooting.
- Managed storage capacity as part of Kubernetes operations.

📁 Detailed documentation: [`docs/kubernetes-storage/longhorn/`](docs/kubernetes-storage/longhorn/)

---

## 🔵 Ceph — Six-Node Kubernetes Storage Lab

A dedicated test environment was personally deployed to evaluate Ceph and its Kubernetes integration.

```text
                    Ceph Test Environment
                             │
                    ┌────────┴────────┐
                    │                 │
                 Group A           Group B
                 3 nodes           3 nodes
                    │                 │
                    └────────┬────────┘
                             │
                           Ceph
                             │
                        Kubernetes
                             │
                        PV / PVC
                           Tests
```

Scope is intentionally limited to the lab work performed:

- Six-node Ceph environment.
- 3+3 node layout.
- Kubernetes integration.
- PV/PVC storage tests.

📁 Detailed documentation: [`docs/kubernetes-storage/ceph/`](docs/kubernetes-storage/ceph/)

---

## 🟣 MinIO — S3 Storage for ELK Snapshots

MinIO was implemented with Docker Compose as a single-node S3-compatible object-storage service with persistent Docker storage.

```text
              Elasticsearch / ELK
                       │
                Daily Snapshot
                       │
                       ▼
                  S3-compatible
                       API
                       │
                       ▼
                    MinIO
                       │
                       ▼
                 Persistent Data
```

The documented use case is **daily Elasticsearch snapshots** written to an S3-compatible MinIO backend.

> Credentials are intentionally excluded from this repository. Configuration examples use environment variables/placeholders.

📁 Detailed documentation: [`docs/object-storage/minio/`](docs/object-storage/minio/)

---

## 📦 Harbor & Nexus — Artifact Storage

Artifact repositories belong in this platform because they provide the storage layer for software delivery rather than application runtime data.

### Harbor

Focus areas will include:

- Private container image storage.
- Image distribution to Kubernetes environments.
- Registry usage in CI/CD workflows.
- Air-gapped/offline image workflows where supported by the actual experience.

📁 [`docs/artifact-storage/harbor/`](docs/artifact-storage/harbor/)

### Nexus

Focus areas will include:

- Artifact/package repository concepts.
- Repository consumption from build pipelines.
- Package caching/proxy workflows where supported by the implementation evidence.
- Separation between container registry responsibilities and general artifact repository responsibilities.

📁 [`docs/artifact-storage/nexus/`](docs/artifact-storage/nexus/)

---

## 🔍 Operations & Troubleshooting

The operational documentation follows a repeatable format:

```text
Symptom
   │
   ▼
Investigation
   │
   ▼
Evidence
   │
   ▼
Resolution / Action
   │
   ▼
Validation
   │
   ▼
Lesson Learned
```

Topics will include:

- PV/PVC lifecycle problems
- StorageClass and provisioning checks
- Capacity management
- Application/storage integration
- Distributed-storage validation
- Object-storage snapshot workflows
- Registry and artifact-repository operations

Only issues and procedures supported by real experience will be labelled as hands-on troubleshooting.

---

## 🗂️ Repository Structure

```text
.
├── README.md
├── docs/
│   ├── architecture/
│   ├── kubernetes-storage/
│   │   ├── longhorn/
│   │   └── ceph/
│   ├── object-storage/
│   │   └── minio/
│   └── artifact-storage/
│       ├── harbor/
│       └── nexus/
├── examples/
├── manifests/
├── diagrams/
└── scripts/
```

---

## 🧪 Evidence & Safety Principles

- Production and laboratory experience are explicitly separated.
- Sensitive infrastructure details are not committed.
- Credentials, tokens, passwords, and private keys are never stored in examples.
- Configuration examples are sanitized and labelled when they are illustrative rather than production exports.
- Technology capabilities are not presented as personal implementation experience unless supported by evidence.

---

## 🚀 Roadmap

- [x] Define storage/artifact platform scope
- [x] Document Longhorn experience boundary
- [x] Document Ceph lab experience
- [x] Document MinIO + ELK snapshot workflow
- [ ] Add detailed Longhorn operational documentation
- [ ] Add Ceph lab deployment documentation
- [ ] Add MinIO snapshot configuration example
- [ ] Add Harbor documentation from existing platform experience
- [ ] Add Nexus documentation from existing platform experience
- [ ] Add architecture diagrams
- [ ] Add sanitized test manifests and examples
- [ ] Add troubleshooting runbooks

---

## 📌 Portfolio Positioning

This repository demonstrates practical understanding of how different storage and artifact systems fit into an infrastructure platform:

**Kubernetes persistent storage → distributed storage → object storage → artifact storage → CI/CD and platform integration.**

It is intentionally built around real implementation evidence rather than presenting a collection of disconnected tutorials.
