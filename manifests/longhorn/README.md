# Longhorn Manifests

Implementation-ready **consumer-side** Kubernetes examples for a cluster where Longhorn is already installed.

## Apply

```bash
kubectl apply -f storageclass-pvc.yaml
kubectl get storageclass
kubectl get pvc
kubectl get pods
```

## Validate initial read/write

```bash
kubectl exec deploy/longhorn-storage-test -- cat /data/health.txt
```

> The StorageClass example is intentionally generic. If your cluster already provides a Longhorn StorageClass, use that existing class instead of creating another one.

To prove data survives Pod replacement, use the [persistence validation runbook](../../docs/runbooks/persistence-validation.md). The helper restarts the selected test Deployment and preserves its PVC.
