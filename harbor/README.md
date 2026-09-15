# 🔴 Harbor Container Registry

<p align="center"><strong>Private Container Registry • Kubernetes Image Distribution</strong></p>

This section documents Harbor usage as a private container registry in DevOps workflows.

## Project Usage

Harbor is used for:

- storing application container images
- providing private image distribution
- supporting Kubernetes deployments
- integrating with CI/CD pipelines

Architecture:

```text
GitLab CI/CD
      |
      v
 Container Build
      |
      v
 Harbor Registry
      |
      v
 Kubernetes Pull
```

## Kubernetes Integration

Typical workflow:

1. Build image in CI/CD
2. Push image to Harbor
3. Create image pull secret
4. Deploy workload using private image

Example validation:

```bash
kubectl get secret
kubectl describe pod <pod-name>
```

## Scope

This section focuses on practical registry usage and Kubernetes integration.
