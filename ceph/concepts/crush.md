# CRUSH

CRUSH (**Controlled Replication Under Scalable Hashing**) determines where objects and PGs are placed.

```
Object
 ↓
PG
 ↓
CRUSH rule
 ↓
Failure domain
 ↓
OSD set
```

Example hierarchy:

```
root
├── host=ceph01
│   ├── osd.0
│   └── osd.1
├── host=ceph02
│   ├── osd.2
│   └── osd.3
└── host=ceph03
    ├── osd.4
    └── osd.5
```

Three replicas provide three copies; the CRUSH rule determines whether copies are separated across hosts/racks.

```bash
ceph osd tree
ceph osd crush tree
ceph osd crush rule ls
ceph osd crush rule dump
```

When designing production storage, decide the failure domain before choosing replica count.
