# Harbor — Private Container Registry

## Role

Harbor is treated as the container-image storage and distribution layer for Kubernetes and CI/CD workflows.

```text
CI/CD
  │
  ▼
Build Image
  │
  ▼
Harbor Registry
  │
  ├────────► Kubernetes Pull
  │
  └────────► Offline / Air-Gapped Image Workflow
```

## Operational concerns

- Image naming and repository organization
- Authentication and pull access
- Image availability for Kubernetes workloads
- Registry usage from CI/CD
- Offline image preparation and distribution

## Kubernetes example

See [`manifests/harbor/image-pull-secret.example.yaml`](../../../manifests/harbor/image-pull-secret.example.yaml).

The example contains placeholders only. Keep real registry credentials and tokens outside Git.
