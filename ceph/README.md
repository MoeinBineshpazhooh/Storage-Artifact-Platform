# 🔵 Ceph Storage Platform

<p align="center"><strong>Practical Ceph Deployment • RBD • CSI • Kubernetes • Operations</strong></p>

Ceph is a distributed storage platform. This section is a practical implementation repository: understand the architecture, choose a deployment method, build a cluster, expose RBD storage, connect it to Kubernetes, validate it, and operate it.

## 🧭 Practical Paths

| Path | Use |
|---|---|
| [Manual deployment](deployment/manual/README.md) | Traditional external Ceph cluster; closest to the historical hands-on model |
| [cephadm](deployment/cephadm/README.md) | Modern Ceph-native lifecycle management |
| [Rook](deployment/rook/README.md) | Kubernetes-native Ceph lifecycle |
| [External Ceph → Kubernetes](kubernetes/external-ceph/README.md) | Consume an externally managed Ceph cluster from Kubernetes |
| [Rook Ceph → Kubernetes](kubernetes/rook-ceph/README.md) | Build and consume Ceph inside Kubernetes |

## 🧠 Knowledge

- [Components](concepts/components.md)
- [RADOS](concepts/rados.md)
- [CRUSH](concepts/crush.md)
- [Pools, PGs and replication](concepts/pools-pgs-replication.md)
- [RBD](concepts/rbd.md)

## 🔧 Operations

- Add/remove/replace OSDs
- Capacity management
- Recovery and rebalancing
- Health validation
- Kubernetes CSI troubleshooting

All examples use placeholders such as `moein.local`, `<MON_IP>`, and `<CEPHX_KEY>`. Never commit real credentials or internal infrastructure values.
