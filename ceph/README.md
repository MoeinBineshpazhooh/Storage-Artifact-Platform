# 🔵 Ceph Storage Platform

<p align="center"><strong>Practical Ceph Deployment • RBD • CSI • Kubernetes • Operations</strong></p>

A practical Ceph implementation area covering multiple deployment models, component knowledge, Kubernetes integration, operations, and troubleshooting.

## 🧭 Practical Paths

| Path | Purpose |
|---|---|
| [Manual](deployment/manual/README.md) | Externally managed Ceph; closest to the historical implementation model |
| [cephadm](deployment/cephadm/README.md) | Modern Ceph-native lifecycle management |
| [Rook](deployment/rook/README.md) | Kubernetes-native Ceph lifecycle |
| [External Ceph → Kubernetes](kubernetes/external-ceph/README.md) | Consume an externally managed Ceph cluster through RBD/CSI |
| [Rook Ceph → Kubernetes](kubernetes/rook-ceph/README.md) | Build and consume Ceph from Kubernetes |

## 🧠 Component Knowledge

Start with [Components](concepts/components.md), then follow [RADOS](concepts/rados.md), [CRUSH](concepts/crush.md), [Pools/PGs/Replication](concepts/pools-pgs-replication.md), and [RBD](concepts/rbd.md).

## 🔧 Operations

The [Ceph guide](../docs/kubernetes-storage/ceph/README.md) documents the lab and integration model. Use the [storage troubleshooting runbook](../docs/runbooks/storage-troubleshooting.md) to inspect PVC, attachment and backend symptoms, and the [persistence test](../docs/runbooks/persistence-validation.md) to check data survival after Pod replacement. Dedicated OSD lifecycle and maintenance runbooks remain future work.

All examples are sanitized and use placeholders. Never commit real credentials, internal hostnames or production IPs.
