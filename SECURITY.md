# Security and Repository Protection

Use only sanitized examples in this repository. Report a real credential exposure privately to the repository owner; use GitHub private vulnerability reporting if it is enabled. Do not paste the credential into a public issue or pull request. Revoke/rotate it first; removing a file does not remove a leaked secret from commit history.

## Checks

`validate` checks example consistency and lab defaults. `secrets` uses pinned Gitleaks to detect credential patterns in pushed/PR commits. A manual Secret scanning workflow run scans available Git history. Reports are redacted, with automatic PR comments, summary output and report artifacts disabled. Scanning is pattern-based and does not prove that all credentials are absent. Do not allowlist entire directories to hide findings; investigate and narrowly document any verified false positive.

Dependabot proposes weekly GitHub Actions and Python dependency updates after its configuration reaches the default branch. Updates still need review and passing checks; there is no automatic merge. Image choices in local environment files require a separate vulnerability/compatibility review.

## Main branch rules

`.github/rulesets/main.json` is a proposed, importable GitHub branch ruleset. **Committing this file does not enable protection.** After merging the workflows and seeing `validate` and `secrets` pass, an administrator must import/enable the ruleset in repository Settings → Rules → Rulesets and verify its active state.

The rules require pull requests, successful up-to-date checks, and resolved review conversations; they block branch deletion and force pushes. Zero required approvals supports a solo-maintained repository where the owner cannot approve their own pull request. Add one required independent approval when another maintainer is available. No bypass actor is proposed.

On 2026-10-12, `main` was unprotected and the public storage repository had no rulesets. The connected GitHub tools cannot mutate repository protection settings. The private Argo CD repository's ruleset request returned a GitHub plan restriction; do not make private code public just to enable protection. GitHub Pro or another eligible plan is needed for that private-repository feature. See [GitHub ruleset availability](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets).

## Deployment boundaries

- Compose labs bind ports to localhost by default. Remote access needs an explicit interface, trusted TLS and firewall rules.
- Set reviewed versioned/digest image references and new local credentials. Environment files and certificates stay outside Git. Environment variables are not encrypted secrets and may be visible to host administrators.
- Retain avoids automatic backing-volume deletion for new example StorageClasses, but requires manual cleanup and separate backups. It does not change existing PV policies.
- Harbor installer sketches and Rook scaffolds are incomplete. CSI controllers, backend disks, CephX credentials, TLS and artifact service authentication need environment-specific setup.
- CI does not test running services, restore backups or scan container images. Use a disposable lab for those checks.
