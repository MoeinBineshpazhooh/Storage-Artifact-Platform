# 🟢 Harbor — Private Container Registry

<p align="center"><strong>Container Images • Kubernetes Pulls • CI/CD • Offline & Air-Gapped Workflows</strong></p>

---

## 🎯 01 • What This Component Solves

Harbor provides the private container-image storage and distribution layer between CI/CD systems and Kubernetes workloads.

```text
Source Code
    │
    ▼
GitLab CI/CD
    │
    │ Build / Push
    ▼
Harbor Registry
    │
    │ Pull
    ▼
Kubernetes
```

---

## 🧑‍💻 02 • My Hands-On Experience

My experience is **operational registry usage and integration**, including:

- Private image repositories
- Kubernetes image pulls
- CI/CD registry integration
- Offline/air-gapped image workflows
- Image availability troubleshooting

> **Evidence boundary:** this repository does not claim that I originally designed or installed the Harbor platform itself.

---

## 🏗️ 03 • Architecture

```text
                         ┌─────────────────┐
                         │   GitLab CI/CD  │
                         └────────┬────────┘
                                  │
                              Build / Push
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ Harbor Registry │
                         └────────┬────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
               Kubernetes                 Air-Gapped
                  Pull                    Distribution
```

---

## ⚙️ 04 • Implement

The repository provides sanitized Kubernetes examples for authenticating to and pulling from a private registry.

### Registry convention

```text
harbor.moein.local
```

### Apply the example

```bash
kubectl apply -f manifests/harbor/image-pull-secret.example.yaml
kubectl apply -f manifests/harbor/pod-pull-example.yaml
```

Then inspect:

```bash
kubectl get pod harbor-pull-test
```

📁 [`image-pull-secret.example.yaml`](../../../manifests/harbor/image-pull-secret.example.yaml)

📁 [`pod-pull-example.yaml`](../../../manifests/harbor/pod-pull-example.yaml)

> The manifests contain placeholders only. Real credentials must be supplied through the environment's secret-management process.

---

## 🧪 05 • Validate

The validation chain is:

```text
Registry Reachable
       │
       ▼
Authentication Works
       │
       ▼
Image Exists
       │
       ▼
Kubernetes Pulls Image
       │
       ▼
Pod Starts
```

Useful checks:

```bash
kubectl get pod harbor-pull-test
kubectl describe pod harbor-pull-test
kubectl get events --sort-by=.lastTimestamp
```

For an air-gapped environment, validate that **every required image and tag** is available internally before deployment.

---

## 🔧 06 • Operate

Day-2 registry operations commonly involve:

- Repository/image organization
- Image availability checks
- Authentication and pull access
- Kubernetes image-pull troubleshooting
- CI/CD push/pull verification
- Offline image preparation

---

## 🚨 07 • Troubleshoot

```text
ImagePullBackOff
      │
      ├──► Image / tag exists?
      ├──► Registry reachable?
      ├──► Pull secret correct?
      ├──► Namespace has access?
      └──► Image available in offline registry?
```

Start with non-secret evidence:

```bash
kubectl describe pod <pod-name> -n <namespace>
kubectl get events -n <namespace> --sort-by=.lastTimestamp
```

Do not print or commit registry credentials.

---

## 🧠 08 • Lessons Learned

For Kubernetes in restricted environments, registry availability becomes part of the deployment dependency chain:

**CI/CD → Registry → Kubernetes → Workload**

In air-gapped environments, image preparation must happen before the workload reaches the cluster; a correct Kubernetes manifest cannot compensate for a missing internal image.

---

## 🔐 Portfolio Boundary

All examples use fictional infrastructure names such as `harbor.moein.local` and placeholders for credentials and image paths.

Real production endpoints, credentials and private configuration are intentionally excluded.
