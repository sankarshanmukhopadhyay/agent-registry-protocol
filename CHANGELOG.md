---
layout: default
title: "Changelog"
nav_exclude: true
---

# Changelog

## [0.9.1] - 2026-07-18

### Added
- Implementation Accelerator with a 15-minute executable quickstart.
- Canonical Acme pilot registry fixtures and API consumer collections.
- Automated pilot-readiness evidence generation.
- Pilot governance, security, operations and exit checklists.
- Deployment profiles, delegation tutorial and production-hardening guidance.

### Changed
- Reference implementation metadata now advertises implementation release 0.9.1.
- GitHub Pages navigation exposes an implementation-first journey.


## [Unreleased]

### Fixed

- Replaced the brittle GitHub Pages minimum HTML-count assertion with deterministic required-page, Mermaid, and unresolved-link checks.

### Changed

- Hardened GitHub Pages publication so Markdown documentation across the repository, including the Candidate Specification, profiles, conformance material, governance documents, and worked scenarios, is rendered as HTML.
- Added a complete documentation catalogue and updated the site landing page.
- Added deterministic Pages build assertions for required pages, Mermaid rendering, rendered-page coverage, and unresolved Markdown links.
- Updated GitHub-hosted JavaScript actions to Node 24-capable major versions where applicable.

## [0.9.0] - 2026-07-16

### Added

- Candidate Specification requirements and conformance targets.
- Machine-readable requirement traceability and compatibility matrix.
- Two separately structured ARPA–TRQP projection implementations.
- Network-boundary metadata discovery and durable event replay/deduplication/checkpoint evidence.
- Informative ARPA–TRQP architecture, machine-readable mapping, discovery declaration model and 13 projection vectors.
- Candidate validation report and evidence bundle.
- Migration guidance from v0.5.0.

### Changed

- Repository status advanced from interoperability draft to Candidate Specification.
- Release gate now includes candidate mapping, adapter equivalence, network and durable-event validation.

### Assurance boundary

The release does not claim external implementation independence, formal TRQP conformance, production deployment assurance, certification or legal recognition.


## [0.5.0] - 2026-07-15

### Added

- six composable protocol modules and explicit non-implication rules;
- normative ARPA-Core Identity and Discovery, Identifier/Alias, and Agent Card interoperability profiles;
- Capability Declaration, Capability Verification, Redress Record, Conformance Declaration, Agent Description Reference, Identifier Alias, Agent Card extension and Registry Metadata schemas;
- controlled registries for record, relationship, lifecycle, event, error, reason, proof-purpose, extension and profile identifiers;
- OpenAPI 3.1 REST contract and AsyncAPI event contract;
- runnable FastAPI/SQLite reference registry, resolver, event replay service and policy decision point;
- multidimensional implementation-report schema and generator;
- identifier, implementor, deployment, security, privacy, conformance, governance and migration guidance;
- twelve end-to-end governance scenarios;
- Makefile, Dockerfile, Compose configuration and expanded CI.

### Changed

- advanced the community draft to v0.5.0;
- clarified that Profile A is independently implementable and unsupported higher-module operations return a deterministic error;
- formalized self-declared Agent Card capabilities as distinct from verification, authorization and assurance;
- strengthened transfer, issuer-competence and alias conflict semantics;
- reframed conformance as protocol, semantic, cryptographic, operational, governance and enforcement evidence.

### Security

- documented alias hijacking, issuer confusion, projection poisoning, replay, event gaps, malicious extensions, transfer abuse and revocation-convergence risks;
- added negative validation and service tests for non-reassignment and alias conflict.

## [0.3.0] - 2026-07-15

- Initial machine-readable schemas, examples, profile matrices and executable conformance vectors.

### Candidate specification consolidation correction

- Consolidated the v0.9.0 Candidate requirements into the authoritative protocol specification.
- Removed the unchanged v0.5.0 draft and detached candidate overlay to eliminate competing specification surfaces.
- Updated all repository references, schemas, manifests, validation rules, and documentation to point to `spec/agent-registry-protocol-v0.9.0.md`.
