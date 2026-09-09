# Harbor Registry Examples

Sanitized examples and operational notes for using a private Harbor registry with Kubernetes and CI/CD.

## Reference flow

```text
Build Pipeline
     │
     ▼
  Build Image
     │
     ▼
 Push to Harbor
     │
     ▼
 Kubernetes
     │
     ▼
 Pull Image
```

Never commit registry credentials, robot tokens, certificates containing private keys, or internal production endpoints.

Use an environment-specific registry hostname such as `registry.example.internal` in examples.
