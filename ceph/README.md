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

[Operations](operations/README.md) covers OSD lifecycle, capacity, recovery and maintenance. [Troubleshooting](troubleshooting/README.md) follows the complete path from host/network through MON, OSD, PG/CRUSH, RBD, CephX, CSI and Kubernetes.

All examples are sanitized and use placeholders. Never commit real credentials, internal hostnames or production IPs.
