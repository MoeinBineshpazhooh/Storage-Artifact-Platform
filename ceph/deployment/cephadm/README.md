# ⚙️ cephadm Deployment

cephadm is the modern Ceph-native lifecycle/orchestration approach.

## Practical flow

```
Prepare hosts
 ↓
cephadm bootstrap
 ↓
MON + MGR
 ↓
Add hosts
 ↓
Discover devices
 ↓
Deploy OSDs
 ↓
Configure pools/CRUSH
 ↓
Validate
 ↓
Optional: integrate Ceph-CSI with Kubernetes
```

Reference commands:

```bash
cephadm bootstrap --mon-ip <MON_IP>
ceph orch host ls
ceph orch device ls
ceph orch daemon add osd <HOST>:<DEVICE>
ceph status
```

Use current official documentation for version-specific prerequisites and syntax.
