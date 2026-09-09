# 🔧 Storage Troubleshooting Runbook

A technology-neutral workflow for Kubernetes storage incidents.

## 1. Identify the symptom

Typical symptoms:

- PVC remains `Pending`
- Pod remains `Pending` because a volume cannot attach/mount
- Application reports filesystem or I/O errors
- Volume capacity is exhausted

## 2. Inspect the Kubernetes objects

```bash
kubectl get pvc -A
kubectl get pv
kubectl get storageclass
kubectl describe pvc <pvc-name> -n <namespace>
kubectl describe pod <pod-name> -n <namespace>
```

## 3. Check events

```bash
kubectl get events -A --sort-by=.lastTimestamp
```

Look for provisioning, attachment, mount, authentication, or scheduling errors.

## 4. Trace the storage layer

```text
Pod
 │
 ▼
PVC
 │
 ▼
StorageClass
 │
 ▼
CSI / Provisioner
 │
 ▼
PV
 │
 ▼
Backend
```

The exact commands after the CSI/provisioner layer depend on the storage technology.

## 5. Validate after remediation

```bash
kubectl get pvc -n <namespace>
kubectl get pv
kubectl get pod -n <namespace>
kubectl describe pod <pod-name> -n <namespace>
```

Then validate application-level read/write behavior.

## Safety

Do not paste credentials, tokens, private keys, or sensitive production logs into tickets or documentation. Record sanitized symptoms and relevant non-secret evidence instead.
