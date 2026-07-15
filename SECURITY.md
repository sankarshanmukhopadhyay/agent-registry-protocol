# Security Policy

## Supported versions

The project is pre-1.0. Security corrections apply to the latest draft and, where practical, the most recent tagged release.

## Reporting a vulnerability

Do not open a public issue for vulnerabilities that could enable exploitation of an implementation or disclose sensitive deployment information.

Use GitHub private vulnerability reporting when enabled. If private reporting is unavailable, contact the repository maintainer through a private channel listed on the maintainer's GitHub profile.

A useful report includes:

- affected specification section, schema, code, or workflow;
- threat actor and preconditions;
- attack steps;
- expected and observed behavior;
- impact;
- suggested mitigation; and
- disclosure constraints.

## Security scope

Security issues may include:

- identifier or controller takeover;
- delegation escalation;
- revocation propagation failure;
- stale-state reliance;
- forged status, decision, or execution receipts;
- registry equivocation;
- unsafe endpoint resolution;
- schema-processing attacks;
- federation and recognition abuse;
- privacy leakage or correlation; and
- governance or recovery mechanisms that enable unauthorized restoration.

## Coordinated disclosure

Maintainers will acknowledge valid reports, assess impact, prepare corrections, and coordinate disclosure. No guaranteed response time is offered while the project remains volunteer-maintained, but security reports receive priority.

## v0.4.0 implementation threats

Security review should explicitly test alias hijacking and loops, issuer-competence confusion, unauthorized control changes, projection poisoning, stale status, event gaps and replay, malicious critical extensions, authority expansion, transfer abuse, key compromise and incomplete revocation convergence. The reference implementation is not a production security boundary.
