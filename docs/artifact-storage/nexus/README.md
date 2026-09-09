# 📦 Nexus — Artifact Repository

## Role

Nexus is documented here as an artifact/package repository layer that can sit beside a container registry in a software-delivery platform.

```text
Developer / CI
      │
      ▼
 Build / Package
      │
      ▼
Nexus Repository
      │
 ┌────┴─────────┐
 ▼              ▼
Publish       Consume
Artifacts     Artifacts
```

## Portfolio scope

This section is intentionally **evidence-controlled**. It provides architecture, operational concepts, and sanitized placeholders without inventing repository formats, deployment topology, or production implementation details that have not been validated.

## Fictional endpoint standard

Use the portfolio-wide domain:

```text
nexus.moein.local
```

Credentials, tokens, and certificates containing private keys must remain outside Git.

## Implementation pattern

```text
CI Pipeline
   │
   ├── download dependency ──► Nexus
   │
   └── publish artifact ─────► Nexus
```

When a concrete repository format is added, document:

1. Repository type
2. Client configuration
3. Authentication mechanism
4. Publish example
5. Consume example
6. Validation commands

## Boundary with Harbor

- **Harbor:** container images.
- **Nexus:** general artifact/package repository responsibilities.

Do not use a container-registry example as evidence of a Nexus implementation.
