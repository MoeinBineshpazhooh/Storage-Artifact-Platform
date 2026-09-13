# Pools, PGs and Replication

## Pool

A pool is a logical RADOS namespace.

## PG

Placement Groups provide indirection between objects and OSD sets:

```
Object → Pool → PG → CRUSH → OSDs
```

This allows Ceph to redistribute data when topology changes.

## Replication

For a replicated pool:

```
size = 3
```

means three desired copies.

```
min_size = 2
```

defines the minimum replica availability required for I/O under the pool policy.

## Recovery

```
OSD failure
 ↓
PG degraded
 ↓
Peering / recovery / backfill
 ↓
replicas restored
 ↓
active+clean
```

Monitor with:

```bash
ceph -s
ceph health detail
ceph pg stat
ceph osd df
```

Capacity planning must leave enough headroom for recovery and rebalancing.
