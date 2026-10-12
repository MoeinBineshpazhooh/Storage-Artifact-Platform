# Repository Checks

From the repository root, with Python 3.12 or newer:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-validation.txt
python scripts/validate.py
python -m py_compile scripts/check-persistence.py
```

The GitHub Actions workflow runs these offline checks on pushes and pull requests with read-only permissions. It does not execute the persistence helper or contact Kubernetes, Ceph or artifact services.

Checks cover YAML parsing and duplicate keys, resource identity fields, matching Deployment selectors, volume-mount references, PVC references within each example directory/namespace, single-replica `Recreate` storage test Deployments, local inline Markdown file links and unsupported chat rendering markup. Compose and Harbor installer examples receive YAML syntax checks, not full configuration or runtime validation.

Only the two documented comment-only Rook scaffolds are exempt from resource checks. They remain non-installable placeholders. External StorageClasses, Ceph pools, credentials and CSI configuration must be supplied separately.

Full Kubernetes/CRD schemas, external links, heading anchors, image availability, storage backend health and recovery behavior are not verified here. Run [persistence validation](persistence-validation.md) in the intended lab after backend setup. That test requires `kubectl`, deliberately restarts a selected lab Deployment, and is separate from CI.
