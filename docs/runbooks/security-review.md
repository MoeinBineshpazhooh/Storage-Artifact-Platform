# Storage and Artifact Review — 2026-10-12

Scope: tracked storage consumer manifests, Compose examples, reverse-proxy configurations, deployment/operation documentation, validation tooling and GitHub branch-rule state. This is a source review with offline checks and CI, not a live platform audit or container vulnerability assessment.

| Area | Finding | Change or remaining requirement |
|---|---|---|
| Persistent volumes | New classes used Delete; deleting a PVC could remove backing data | Examples now use Retain; existing PV policies and backups need separate review |
| Storage validation | Startup rewrote the health file; initial reads did not prove persistence | Preserve initial files, fail on write errors, test a unique marker after Pod replacement |
| Single-volume Deployments | Rolling updates could overlap volume consumers | Single-replica Recreate test examples; deliberate lab downtime |
| MinIO Compose | Moving image, host networking, optional credentials, implicit environment lookup | Require selected image/credentials; loopback ports; explicit env-file commands |
| MinIO Helm | Outdated credential options, sample console user, all-interface forwarding | Existing Secret, users disabled, selected chart version, local forwarding; no backup data in ephemeral example |
| Nexus | Untagged images, direct registry HTTP port, writable cert/config mounts | Explicit image variables, loopback exposure, registry reachable through TLS proxy, read-only mounts |
| Harbor | Reduced Compose/config looked deployable; proxy sketch lacks full installer routing/auth wiring | Use official release-matched installer; keep sketches as reference and exclude generated secrets |
| Artifactory | NuGet v3 endpoint lacked the expected API path | Corrected standard endpoint; verify custom reverse-proxy prefix with target service |
| External Ceph | Consumer examples lack driver installation and cluster config | Explicit prerequisites; expansion Secret fields aligned in detailed guide |
| Rook | Operator/cluster files contain comments only | Explicitly non-installable scaffolds; full chosen-release install and pool needed |
| Repository credentials | No recurring secret-pattern checks or dependency updates | Pinned Gitleaks workflow and Dependabot configuration; investigate findings before merging |
| GitHub main | Public storage repo unprotected; no rulesets at review time | Importable ruleset proposed, not enabled by committed files |

## Operational limits and compatibility

The changes are source defaults for new/reviewed lab deployments. They do not modify running clusters, existing StorageClasses/PVs or Docker volumes. For existing StorageClasses, choose a new class name when configuration changes; preserve bound PVCs. A retained backing volume needs manual cleanup and is not a backup.

Changing host networking to published loopback ports prevents remote MinIO access by default. Remote Elasticsearch consumers require a reviewed interface plus TLS/firewall configuration. Keep the same Compose project name so existing named volumes remain attached. Required empty environment-template fields intentionally stop an unconfigured launch; fill them locally with tested image versions/digests and fresh credentials.

Nexus still requires a configured Docker repository connector, authentication realm and certificates. Harbor's hand-written proxy is architecture reference, not a replacement for the installer-generated proxy and token service. Neither stack has been brought up during this review.

The MinIO chart schema was checked against upstream 5.4.0 source; this is not a recommendation to deploy that historical application image. Select and inspect a supported/tested release and scan its server/client images. Restore backups into an isolated destination and verify application data before relying on snapshot success. Test node failures, volume reattachment, capacity thresholds, Ceph quorum/failure domains and storage recovery in a lab.

## Validation

Offline YAML/identity/reference/link checks, regression mutations, simulated persistence success/failure cases and Python compilation are run before publication. GitHub validation and secret scan outcomes are reported in the pull request checks. A clean pattern scan is not proof of absence of every credential, and it does not check image CVEs or detect every insecure deployment option.

## Protection status

The GitHub connection can publish branches and pull requests but has no administration-write operation for rulesets. The public storage repo can use an administrator-enabled main ruleset. The private Argo CD repo's ruleset query returned a plan restriction requiring GitHub Pro or public visibility; visibility is preserved. See [SECURITY.md](../../SECURITY.md) for exact proposed rules. GitHub main protection does not configure the external GitLab `devops` branch or Kubernetes production RBAC.

Sources: [Docker interpolation](https://docs.docker.com/reference/compose-file/interpolation/), [Kubernetes PV lifecycle](https://kubernetes.io/docs/concepts/storage/persistent-volumes/), [MinIO chart values](https://github.com/minio/minio/blob/master/helm/minio/values.yaml), [JFrog NuGet API](https://docs.jfrog.com/artifactory/docs/nuget-repositories), [Harbor installation](https://goharbor.io/docs/main/install-config/), and [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets).
