# 🟢 JFrog Artifactory — Dependency & Artifact Proxy

> **Experience:** Operational usage
>
> **Focus:** Repository consumption, dependency proxying, remote/private/local repositories, and GitLab CI/CD integration.

---

## 🎯 What It Does

JFrog Artifactory acts as an internal repository layer between CI/CD jobs and package sources.

Instead of every pipeline reaching external package sources directly, GitLab CI/CD can consume dependencies through an internal Artifactory endpoint.

```text
                    ┌──────────────────────┐
                    │      GitLab CI/CD     │
                    └──────────┬───────────┘
                               │
                         Dependency restore
                               │
                               ▼
                    ┌──────────────────────┐
                    │  JFrog Artifactory   │
                    │   Repository Layer   │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼─────────────────┐
             ▼                 ▼                 ▼
       Remote Repos       Private Repos      Local Repos
             │                 │                 │
             └─────────────────┼─────────────────┘
                               ▼
                         Build Dependency
```

---

## 🧩 Repository Model

The practical model used in the project included three repository roles:

| Repository role | Purpose |
|---|---|
| 🌐 **Remote** | Proxy/cache packages from an upstream source |
| 🔒 **Private** | Controlled internal packages and dependencies |
| 📦 **Local** | Packages/artifacts published into the internal repository |

This creates a controlled package-consumption path for CI/CD.

---

## 🔗 GitLab CI/CD Integration

The important integration is the connection between the package manager and the pipeline's dependency-restore stage.

```text
GitLab Runner
     │
     │ restore dependencies
     ▼
Artifactory
     │
     ├── remote package source
     ├── private package repository
     └── local package repository
     │
     ▼
Dependency available to build
```

The pipeline should reference the sanitized internal endpoint rather than a real production address.

Example:

```text
artifactory.moein.local
```

Credentials must be injected through GitLab CI/CD variables or an appropriate secret-management mechanism and must never be committed to the repository.

---

## 🛠️ Implementation Pattern

### 1. Configure repository endpoints

Define the internal Artifactory repositories required by the project.

```text
REMOTE_REPOSITORY = artifactory.moein.local/<remote-repository>
PRIVATE_REPOSITORY = artifactory.moein.local/<private-repository>
LOCAL_REPOSITORY  = artifactory.moein.local/<local-repository>
```

### 2. Configure the package client

The package manager used by the application should point to the appropriate Artifactory repository.

For example, a .NET project can use a sanitized NuGet source such as:

```text
https://artifactory.moein.local/<nuget-repository>/v3/index.json
```

### 3. Restore through CI/CD

```text
Pipeline
  │
  ├── checkout
  ├── restore dependencies ─────► Artifactory
  ├── build
  ├── test
  └── package
```

### 4. Validate

The useful validation is not simply "the repository is reachable". Confirm that the complete dependency path works:

```text
GitLab Runner
      │
      ▼
Package Client
      │
      ▼
Artifactory Repository
      │
      ▼
Dependency Resolution
      │
      ▼
Build succeeds
```

---

## 🔍 Troubleshooting

| Symptom | First checks |
|---|---|
| Dependency not found | Repository URL, package name/version, repository routing |
| Restore authentication failure | CI variable availability and repository permissions |
| Remote dependency unavailable | Remote repository connectivity and cached artifact availability |
| Private package unavailable | Repository path and package publication state |
| Pipeline works locally but not in CI | Runner configuration, package source configuration, CI variables |
| Slow restore | Remote proxy/cache state and repository connectivity |

Useful non-secret checks:

```bash
# Confirm the configured package source
# Use the package manager's source-list command for your project.

# Inspect the CI job's dependency-restore stage.
# Do not print credentials or secret variables.
```

---

## 🧠 Operational Lessons

- Centralizing dependencies gives CI/CD a predictable internal package path.
- Remote repositories can reduce repeated upstream downloads through repository caching/proxying.
- Private and local repositories should be separated according to artifact ownership and lifecycle.
- Package-manager configuration belongs in the build workflow, not hard-coded credentials.
- A successful repository connection is not enough; dependency resolution and the build must also be validated.

---

## 🔐 Portfolio Boundary

This documentation represents **hands-on operational usage and integration** of JFrog Artifactory.

It does **not** claim that the Artifactory platform itself was designed or installed by the author.

All endpoints, credentials, repository names and organization-specific configuration shown here are sanitized.

---

## 📁 Related Areas

- [`manifests/jfrog-artifactory/`](../../../manifests/jfrog-artifactory/)
- [`GitLab CI/CD Platform`](https://github.com/MoeinBineshpazhooh/gitlab-ci-cd-platform)
- [`MinIO object storage`](../../object-storage/minio/)
- [`Harbor container registry`](../harbor/)
