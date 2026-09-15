# 🟠 JFrog Artifactory

<p align="center"><strong>Artifact Repository • Dependency Management • CI/CD Integration</strong></p>

This section documents practical JFrog Artifactory usage in DevOps workflows.

## Project Usage

JFrog Artifactory can act as an artifact repository and proxy layer between development tools and external repositories.

Example flow:

```text
Developer / CI Pipeline
          |
          v
   JFrog Artifactory
          |
  +-------+-------+
  |       |       |
Remote  Local  Virtual
Repo    Repo    Repo
```

## Repository Types

- Local repositories: internal artifacts
- Remote repositories: proxy external sources
- Virtual repositories: unified access endpoint

## CI/CD Usage

Typical usage:

1. Pipeline requests dependencies
2. Artifacts are resolved through Artifactory
3. Builds publish internal artifacts
4. Deployments consume approved versions

## Scope

This section documents practical artifact repository usage, not full Artifactory administration.
