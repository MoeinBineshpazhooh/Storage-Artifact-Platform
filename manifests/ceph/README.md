# Ceph Kubernetes Integration

This directory contains sanitized examples for validating a Ceph-backed Kubernetes storage integration.

> **Scope:** laboratory/reference material. The six-node Ceph environment described in the repository was a test environment, not a production deployment.

## Implementation model

```text
Ceph Cluster
     │
     ▼
 Kubernetes Storage Integration
     │
     ▼
 PV / PVC
     │
     ▼
 Test Workload
```

Use the manifests here only after the Ceph/Kubernetes integration layer has been configured for the target environment.
