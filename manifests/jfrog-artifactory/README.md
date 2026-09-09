# JFrog Artifactory Manifests

Sanitized reference material for connecting GitLab CI/CD dependency restoration to JFrog Artifactory.

## Fictional endpoint

```text
artifactory.moein.local
```

## Repository roles

```text
Remote  → proxy/cache upstream packages
Private → controlled internal packages
Local   → internally published artifacts
```

## Client configuration pattern

Use the package-manager configuration appropriate for the project and point it to the required Artifactory repository.

Example NuGet source:

```text
https://artifactory.moein.local/<nuget-repository>/v3/index.json
```

## GitLab CI/CD

The dependency-restore stage consumes the internal repository:

```text
GitLab Runner → Artifactory → Dependency Restore → Build
```

Authentication must be supplied externally through CI/CD variables or secret management. Never commit credentials.

> This directory documents operational integration patterns; it is not a claim that the Artifactory platform itself was deployed by the author.
