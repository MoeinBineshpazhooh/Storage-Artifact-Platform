# 🐳 Harbor — Private Container Registry

## Role

Harbor is the container-image storage and distribution layer documented in this portfolio for Kubernetes and CI/CD workflows.

```text
Developer / CI
      │
      ▼
 Build Image
      │
      ▼
Harbor Registry
      │
 ┌────┴──────────┐
 ▼               ▼
Kubernetes     Offline / Air-Gapped
Pull           Image Workflow
```

## Operational scope

- Image repository organization
- Authentication and pull access
- Kubernetes image consumption
- CI/CD registry integration
- Offline/air-gapped image preparation and distribution

## Sanitized implementation

The repository standardizes fictional infrastructure names around **`moein.local`**. The Kubernetes example uses a Harbor-style registry endpoint such as `harbor.moein.local`.

```bash
kubectl apply -f manifests/harbor/image-pull-secret.example.yaml
kubectl apply -f manifests/harbor/pod-pull-example.yaml
kubectl get pod harbor-pull-test
```

The secret manifest contains placeholders only. Create real credentials through the deployment or secret-management process; never commit them.

## Validation

```bash
kubectl describe pod harbor-pull-test
kubectl get events --sort-by=.lastTimestamp
```

For an air-gapped environment, verify that every required image is available in the internal registry before deployment.

## Evidence boundary

This documentation describes operational registry usage and integration. It does not claim that the Harbor platform itself was originally designed or installed by the author.

## Files

- [`manifests/harbor/image-pull-secret.example.yaml`](../../../manifests/harbor/image-pull-secret.example.yaml)
- [`manifests/harbor/pod-pull-example.yaml`](../../../manifests/harbor/pod-pull-example.yaml)
