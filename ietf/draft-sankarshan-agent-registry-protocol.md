---
title: "Agent Registry Protocol"
abbrev: "ARPA"
docname: draft-sankarshan-agent-registry-protocol-00
category: std
ipr: trust200902
submissiontype: IETF
area: "Applications and Real-Time"
workgroup: "Individual Submission"
keyword:
  - software agents
  - agent registry
  - delegated authority
  - lifecycle
  - resolution
  - authorization
stand_alone: yes
pi:
  toc: yes
  sortrefs: yes
  symrefs: yes
  compact: yes
author:
  -
    ins: S. Mukhopadhyay
    name: Sankarshan Mukhopadhyay
    org: Independent
normative:
  RFC2119:
  RFC8174:
  RFC9110:
  RFC9111:
  RFC8259:
  RFC3339:
  RFC3986:
  RFC9457:
informative:
  RFC6749:
  RFC8414:
  RFC8615:
  RFC9421:
  ARPA-SPEC:
    title: "Agent Registry Protocol and Architecture (ARPA) Candidate Specification"
    author:
      -
        ins: S. Mukhopadhyay
        name: Sankarshan Mukhopadhyay
    date: 2026-07-16
    target: https://sankarshanmukhopadhyay.github.io/agent-registry-protocol/spec/agent-registry-protocol-v0.9.0.html
---

--- abstract

Software agents increasingly act on behalf of people and organizations across administrative and security boundaries. Existing discovery mechanisms can identify an endpoint or advertise a capability, but they do not by themselves provide a common way to resolve who operates an agent, the bounded authority under which it acts, whether that authority is current, or what evidence supports a reliance decision.

This document defines the Agent Registry Protocol (ARPA), an HTTP and JSON protocol for publishing and resolving information about software agents, their operational deployments, typed relationships, bounded delegated authority, lifecycle status, and associated evidence. ARPA separates identification, authentication, authorization, assurance, and lifecycle state. Registration, successful authentication, capability advertisement, or proof verification does not by itself establish authority to perform an action.

The protocol is designed to support deterministic fail-safe behavior when material authority information is revoked, suspended, expired, stale, conflicting, unavailable, or unverifiable.

--- middle

# Introduction

Software agents can retrieve protected information, invoke tools, modify workflows, initiate transactions, coordinate other agents, and otherwise cause effects on behalf of principals. A relying system evaluating such an action needs more than endpoint discovery. It needs protocol-visible information sufficient to determine which agent is involved, which deployment is executing, who operates or controls it, what delegated authority applies, whether that authority remains effective, and where supporting evidence can be obtained.

ARPA provides a registry and resolution protocol for those questions. It does not define a universal trust score, a universal legal theory of agency, a new authentication protocol, or a mandatory credential format. It also does not treat successful registry resolution as an authorization decision. A relying party combines ARPA resolution results with local policy and any external authentication, credential, or assurance mechanisms required for its context.

The protocol intentionally preserves several non-implication rules:

* discovering an agent does not imply authorization to invoke it;
* control of an identifier or cryptographic key does not imply authority to act for a principal;
* an advertised capability does not imply permission to exercise that capability;
* successful proof verification does not imply that the asserted authority is current or sufficient;
* technical federation does not imply governance recognition; and
* historical registry state is evidence for evaluation, not by itself a legal determination about a historical act.

The wider ARPA project specification {{ARPA-SPEC}} defines additional governance, assurance, conformance, federation, redress, implementation, and deployment material. This Internet-Draft deliberately narrows that work to interoperable protocol behavior.

## Conventions and Requirements Language

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and **OPTIONAL** in this document are to be interpreted as described in BCP 14 {{RFC2119}} {{RFC8174}} when, and only when, they appear in all capitals, as shown here.

HTTP terminology follows {{RFC9110}}. JSON follows {{RFC8259}}. Timestamps use the `date-time` form of {{RFC3339}}.

# Scope

ARPA defines protocol behavior for:

* persistent agent identifiers and deployment identifiers;
* registration and update of agent records;
* typed relationships between agents, principals, operators, controllers, accountable entities, and other actors;
* representation of bounded delegated authority;
* capability and assurance references without treating either as authorization;
* multidimensional lifecycle and authority status;
* current and point-in-time resolution;
* registry discovery and query behavior;
* event publication sufficient to communicate material status changes;
* deterministic processing of stale, conflicting, unavailable, and unsupported state;
* error representation;
* extension and version negotiation rules; and
* evidence references supporting later audit or reliance evaluation.

ARPA does not define a universal agent-to-agent messaging protocol, task protocol, reputation system, liability regime, credential format, signature suite, policy language, distributed ledger, or mandatory storage architecture.

# Terminology

**Agent:** A software entity capable of performing actions with some degree of autonomy.

**Agent Identifier:** A persistent URI identifying a logical agent independently of a particular version or deployment.

**Deployment:** An operational instance of an agent version in a particular execution context.

**Principal:** A person or organization on whose behalf an agent may act.

**Operator:** The entity responsible for running an agent deployment.

**Controller:** An entity with material technical or administrative control over an agent or deployment.

**Accountable Entity:** An entity identified by the registry as accepting a defined accountability role for an agent or class of actions.

**Relationship:** A typed, scoped, time-bounded statement linking two registry subjects.

**Authority Envelope:** A bounded representation of authority delegated from an issuer to a subject, including permitted actions, resources, conditions, prohibitions, delegation depth, and validity interval.

**Resolver:** A client that queries one or more ARPA registries.

**Relying Party:** A system or actor that uses ARPA data as one input to a local trust or authorization decision.

**Registry:** A service that publishes ARPA records and resolution responses.

**Authoritative Record:** A record for which the publishing registry is identified as an authoritative source within the applicable scope.

**Derived Record:** A cached, indexed, projected, or federated representation whose authoritative source is elsewhere.

**Material State:** State whose absence or change can alter an authorization or reliance outcome.

# Protocol Model

## Separation of Resolution, Decision, and Enforcement

ARPA separates three functions:

1. **Resolution** obtains registry state and evidence references.
2. **Decision** evaluates that state against action context and relying-party policy.
3. **Enforcement** permits, restricts, or denies an actual action.

A registry response MUST NOT claim that a relying party is required to authorize an action unless the registry is itself the applicable policy decision authority for that action and this role is explicitly represented. A resolver MUST NOT infer authorization solely from successful resolution.

## Protocol Roles

An implementation can act as one or more of:

* registry publisher;
* resolver or registry consumer;
* authority evaluator;
* event publisher;
* event consumer or enforcement point; or
* federation participant.

An implementation claiming conformance to one role MUST NOT imply conformance to another role.

## Authority Invariants

An authority evaluator conforming to this document:

* MUST verify that a delegation issuer possessed the effective authority being delegated;
* MUST NOT allow delegation to expand the issuer's effective scope;
* MUST apply explicit validity intervals, conditions, prohibitions, resource limits, action limits, and delegation-depth limits;
* MUST treat revoked, suspended, expired, stale, conflicting, unavailable, or unverifiable material authority as non-affirmative;
* MUST NOT infer transitive recognition unless a transitive relationship is explicitly declared and permitted by policy; and
* MUST retain enough input and result information to explain an affirmative or negative authority evaluation.

# Identifier Model

## Agent Identifiers

An Agent Identifier MUST be a URI conforming to {{RFC3986}}. Its scheme and dereference behavior are deployment choices unless another specification defines them. ARPA does not define a new URI scheme in this document.

An Agent Identifier MUST identify the logical agent rather than a single software build, process, network endpoint, or ephemeral runtime session.

Registries MUST NOT silently reassign an Agent Identifier to a different logical agent. If an identifier becomes unusable, the registry SHOULD publish a terminal status or supersession relationship rather than reuse it.

## Deployment Identifiers

A deployment MUST have an identifier unique within the scope of the authoritative registry. A deployment identifier SHOULD be globally unique when deployments are expected to move between registries or administrative domains.

A deployment record MUST identify the logical Agent Identifier and SHOULD identify the agent version from which the deployment was created.

# Record Envelope

Every ARPA record returned by the protocol MUST contain an envelope with at least:

~~~~ json
{
  "record_type": "agent",
  "record_id": "urn:example:record:1234",
  "subject": "https://registry.example/agents/7f6a",
  "issuer": "https://registry.example",
  "issued_at": "2026-08-18T12:00:00Z",
  "valid_from": "2026-08-18T12:00:00Z",
  "version": "1",
  "source": "https://registry.example/records/1234"
}
~~~~

A record that expires MUST contain `valid_until`. A record that supersedes another record SHOULD contain a reference to the superseded record. A derived record MUST identify the authoritative source and SHOULD identify when the derived representation was produced.

The `record_type` value identifies the record semantics. Unknown record types MUST NOT be interpreted as a known type. A resolver MAY retain unknown record types as opaque evidence.

# Agent Resource Model

An agent resource SHOULD contain:

* the Agent Identifier;
* human-readable labels, if available;
* current version and deployment references;
* relationship references;
* service endpoint references;
* capability declaration references;
* authority references;
* lifecycle status;
* evidence references; and
* representation metadata including source and freshness.

A capability declaration MUST NOT be interpreted as authorization. An endpoint reference MUST NOT be interpreted as proof that the endpoint is controlled by the principal for whom an action is proposed.

# Relationship Model

A relationship record MUST contain:

* a relationship type;
* a source subject;
* a target subject;
* an issuer;
* scope;
* effective time; and
* current status.

Where absence of a relationship would change an authorization outcome, the response MUST provide either the relationship or a machine-readable indication that authoritative relationship state could not be established.

Registries MUST NOT infer a broader relationship from a narrower one. For example, an `operated-by` relationship MUST NOT be interpreted as an `authorized-by` relationship unless a separate specification explicitly defines such equivalence.

# Authority Envelope

An authority envelope represents bounded authority. It MUST contain:

* `issuer`;
* `subject`;
* `actions` or an equivalent action scope;
* `valid_from`;
* status information; and
* a stable identifier for the authority statement.

When applicable it MUST also contain:

* resources or resource classes;
* purpose restrictions;
* conditions;
* prohibitions;
* monetary, rate, geographic, or other limits;
* `valid_until`;
* delegation depth or prohibition on further delegation;
* evidence references; and
* the authority statement from which the issuer derives the delegated scope.

An authority envelope MUST NOT be interpreted independently of its current status and applicable parent authority. Delegation MUST NOT increase the issuer's effective action, resource, purpose, temporal, geographic, monetary, or delegation scope.

# Lifecycle and Status

ARPA represents lifecycle state as multiple dimensions rather than a single `active` flag. A response MAY expose dimensions including registration, operational, security, authority, and assurance status.

A registry MUST distinguish at least the following effects when they are applicable:

* active or current;
* suspended;
* revoked;
* expired;
* superseded;
* retired; and
* indeterminate or unavailable.

A resolver MUST NOT map `indeterminate`, `unavailable`, `conflicting`, or `stale` material authority state to an affirmative authorization outcome.

A registry publishing revocation or suspension SHOULD expose an event or other freshness mechanism enabling consumers to discover the change promptly. A publisher MUST NOT describe revocation as fully converged merely because the registry record changed if downstream enforcement acknowledgements are required by the applicable profile.

# HTTP API

ARPA uses HTTP semantics as defined by {{RFC9110}}. Registries MUST use HTTPS for network deployments that carry non-public data or authority information unless an equivalent authenticated and confidential transport is provided by the deployment environment.

This document defines the following logical resources. Deployments MAY choose different path layouts if discoverable metadata maps the logical operations unambiguously.

| Operation | Example target | Purpose |
|---|---|---|
| Registry metadata | `GET /.well-known/agent-registry` | Discover protocol metadata |
| List/discover agents | `GET /agents` | Query discoverable agents |
| Resolve agent | `GET /agents/{id}` | Resolve current agent state |
| Historical resolution | `GET /agents/{id}?at={time}` | Resolve effective-time state |
| Resolve authority | `GET /agents/{id}/authority` | Resolve authority statements |
| Resolve status | `GET /agents/{id}/status` | Resolve lifecycle/status state |
| Register agent | `POST /agents` | Create an agent registration |
| Update registration | `PUT /agents/{id}` | Replace an owned registration |

Use of `/.well-known/agent-registry` requires an IANA registration before Standards Track publication; see [IANA Considerations](#iana-considerations).

## Registry Metadata

A registry metadata response SHOULD contain:

~~~~ json
{
  "protocol": "arpa",
  "protocol_version": "1",
  "issuer": "https://registry.example",
  "api_base": "https://registry.example/api",
  "supported_record_types": [
    "agent", "relationship", "authority", "status"
  ],
  "historical_resolution": true,
  "events_endpoint": "https://registry.example/events"
}
~~~~

The metadata endpoint MUST NOT imply that every advertised optional feature is authorized for every caller. Access control remains operation-specific.

## Registration

A client creating a registration sends `POST` to the registration collection with a JSON representation of the requested agent record.

The registry MUST authenticate and authorize the registration request according to local policy. ARPA does not define that authentication mechanism.

On successful creation, the registry SHOULD return `201 Created` and a `Location` header identifying the new agent resource. A retry-safe deployment SHOULD support an application-level idempotency mechanism and MUST document its semantics.

A registry MUST reject a request that would reassign an existing persistent Agent Identifier to a different logical agent.

## Current Resolution

A successful current-state resolution returns `200 OK` with the current representation and sufficient freshness/provenance metadata for the client to distinguish authoritative from derived state.

A response MUST identify when material state is derived or cached. Derived material authority state MUST include the authoritative source and freshness information.

`404 Not Found` means that the queried registry has no resolvable resource for the supplied identifier. It MUST NOT be interpreted as evidence that the agent does not exist in any other registry.

## Historical Resolution

Historical resolution uses an `at` query parameter containing an {{RFC3339}} timestamp. The response MUST distinguish:

* the requested effective time;
* the time at which the resolution was performed;
* records selected as effective at the requested time;
* later material events known at evaluation time; and
* reconstruction completeness or limitations.

A historical response MUST NOT silently apply current status to the requested historical time or silently ignore later events that materially affect interpretation.

If the registry cannot reconstruct material historical state with sufficient confidence, it MUST return an indeterminate reconstruction status and MUST NOT present the result as an authoritative affirmative determination.

## Discovery

Discovery endpoints are informational. Search or list results MUST NOT imply authorization, endorsement, assurance, or permission to invoke an agent.

A registry SHOULD minimize information disclosed through unauthenticated discovery. Sensitive relationships, principal linkage, delegated authority details, or operational metadata SHOULD require authorization when disclosure creates material privacy or security risk.

## Authority Resolution

Authority resolution returns one or more authority envelopes and their status. If the registry knows that required parent authority, status, or evidence is missing, stale, conflicting, or unavailable, the response MUST expose that condition rather than omit it in a way that could be interpreted as affirmative authority.

## Conditional Requests and Caching

Registries SHOULD provide validators such as `ETag` where stable representation validators are available. Resolvers SHOULD use conditional requests to reduce load while retaining freshness.

Responses containing authority or security status MUST define cache behavior appropriate to the revocation and freshness requirements of the deployment. Shared caches MUST NOT store confidential responses unless explicitly permitted by applicable HTTP caching rules {{RFC9111}} and response directives.

A stale cached response MUST NOT be used to produce an affirmative authority result when the applicable freshness policy requires newer authoritative state.

# Error Handling

Protocol errors SHOULD use Problem Details for HTTP APIs {{RFC9457}} with an ARPA-specific problem type when interoperable handling is required.

An error response SHOULD contain a stable machine-readable reason code. Registries MUST distinguish at least:

* malformed request;
* unsupported protocol version;
* unsupported record type;
* unauthorized operation;
* forbidden disclosure;
* unknown identifier;
* stale material state;
* conflicting material state;
* authoritative source unavailable; and
* historical reconstruction indeterminate.

Clients MUST NOT convert an error indicating stale, conflicting, unavailable, or indeterminate material authority into an affirmative authority outcome.

# Versioning and Extensibility

A registry MUST identify the ARPA protocol version it implements. Extension fields MUST be namespaced or otherwise collision-resistant.

An extension MUST NOT redefine the semantics of a core field. An extension MUST NOT weaken a core fail-safe requirement while claiming conformance to this specification.

Recipients MUST ignore unknown optional extension fields unless their local policy requires rejection. Unknown fields that are marked critical by a future extension mechanism MUST cause processing to fail unless understood.

New relationship types, record types, reason codes, and other extensible values SHOULD be defined through registries with explicit change control. This draft currently maintains project registries; the [IANA Considerations](#iana-considerations) section identifies which registries require IANA action before publication as an RFC.

# Event Semantics

A registry MAY expose an event stream for lifecycle, authority, relationship, and other material changes. This document does not mandate a specific event transport.

Events MUST be persistently sequenceable within a publisher scope. Consumers MUST be able to detect replay and duplicates. Event processing MUST be idempotent with respect to an event identifier.

An event MUST identify:

* the event type;
* event identifier;
* publisher;
* affected subject or record;
* effective time;
* sequence or ordering information; and
* a reference or representation sufficient to obtain the resulting authoritative state.

Receiving an event is not equivalent to completing enforcement. Where revocation convergence is material, the applicable profile SHOULD define acknowledgement and convergence semantics.

# Processing Requirements

A conforming resolver or authority evaluator MUST maintain the following processing order where the steps apply:

1. validate the response syntax and supported protocol version;
2. establish the response source and whether it is authoritative or derived;
3. evaluate freshness and requested effective time;
4. establish lifecycle/status applicability;
5. validate relationship and authority scope;
6. apply parent-authority and delegation constraints;
7. evaluate conflicts or missing material inputs;
8. produce an affirmative, negative, or indeterminate result; and
9. retain reason codes and evidence references sufficient to explain the outcome.

A later step MUST NOT override an earlier fail-safe condition unless the protocol explicitly defines a valid restoration or supersession transition supported by authoritative evidence.

# Security Considerations

ARPA carries data that can influence authorization and high-impact relying decisions. Implementers MUST therefore treat registry integrity, freshness, provenance, and authorization as security properties rather than descriptive metadata.

## Identifier and Endpoint Substitution

Attackers can attempt to replace an Agent Identifier, key binding, deployment, or service endpoint while preserving superficially valid metadata. Registries MUST authenticate modification requests and MUST maintain provenance sufficient to detect unauthorized reassignment. Resolvers SHOULD bind endpoint use to separately authenticated identity mechanisms appropriate to the application.

## Authority Escalation

A malicious or defective issuer can attempt to delegate actions or resources beyond its own effective scope. Evaluators MUST intersect delegated authority with the issuer's effective authority and MUST NOT allow delegation to expand scope.

## Stale-State and Revocation Races

Cached or replicated data can remain affirmative after a suspension, revocation, compromise, or operator change. Registries SHOULD expose freshness and event mechanisms appropriate to the risk. Evaluators MUST apply relying-party freshness policy and MUST fail safely when required current state cannot be established.

## Replay and Event Reordering

Events and evidence can be replayed or delivered out of order. Events MUST contain stable identifiers and sequence information. Consumers MUST deduplicate events and MUST NOT treat an older event as superseding a known later authoritative state.

## Federation and Recognition Confusion

Receiving records from another registry does not establish governance recognition. Implementations MUST separate transport federation from any recognition relationship and MUST NOT infer transitive trust.

## Confused Deputy

An agent or intermediary can present a technically valid delegation outside its intended principal, purpose, resource, or action context. Evaluators MUST bind authority evaluation to the action context and MUST apply all applicable restrictions.

## Registry Compromise

A compromised authoritative registry can publish false state. Deployments requiring stronger assurance SHOULD use authenticated records, append-only transparency mechanisms, independent evidence sources, or other controls appropriate to the threat model. This specification does not mandate a single cryptographic proof format.

# Privacy Considerations

Agent registries can reveal organizational structures, principal-agent relationships, operational deployments, capabilities, delegated authority, and historical activity. Implementers SHOULD expose the minimum information necessary for the relying purpose.

Unauthenticated discovery SHOULD avoid disclosing sensitive relationships or authority details. Registries SHOULD support access-controlled resolution and SHOULD separate public discovery metadata from protected authority evidence.

Historical resolution creates additional correlation and retention risks. Deployments SHOULD define retention periods and access policy for historical state. The existence of a protocol capability for historical resolution does not require every registry to make all historical records public.

Resolvers and registries SHOULD minimize logging of sensitive query parameters and identifiers where operationally feasible. Logs that reveal which agents or principals a caller is investigating can themselves be sensitive.

# Operational Considerations

Registries SHOULD publish operational metadata describing supported protocol versions, limits, historical-resolution capability, freshness guarantees, and event availability.

Deployments SHOULD define availability and recovery objectives for material authority and status data. If an authoritative source is unavailable, consumers MUST distinguish unavailability from a negative or affirmative authority state.

Registry operators SHOULD monitor replication lag, event delivery gaps, stale caches, failed status propagation, and conflicting authoritative records because each can alter reliance outcomes.

# Implementation Status
{: removeinrfc="true"}

This section records implementation experience for the current Internet-Draft and is intended to be removed before RFC publication.

The ARPA project currently maintains Python and TypeScript implementation tracks over shared schemas, controlled registries, and conformance vectors. Repository release v0.9.5 reports deterministic and historical cross-runtime outcome checks and loopback HTTP interoperability testing.

Both implementation tracks are maintained within the same project governance boundary. They therefore provide implementation diversity and executable conformance evidence, but they are not claimed as independently operated implementations.

The implementation and evidence repositories are available from the ARPA project referenced by {{ARPA-SPEC}}.

# IANA Considerations
{: #iana-considerations}

This document currently anticipates, but does not request in version `-00`, the following IANA actions. The exact registrations and registration policies require working-group or community review before Standards Track publication:

1. registration of the `agent-registry` well-known URI suffix if `/.well-known/agent-registry` is retained, using the registry established by {{RFC8615}};
2. evaluation of whether a dedicated ARPA JSON media type is justified; and
3. evaluation of whether core ARPA registries such as record types, relationship types, and reason codes require IANA-managed registries or can remain specification-defined extensibility points.

Before this document advances beyond early individual-draft review, this section MUST be replaced with concrete registration requests or an explicit statement that no IANA actions are required.

# Relationship to Existing IETF Mechanisms

ARPA is intended to compose with, rather than replace, existing authentication and authorization mechanisms.

OAuth 2.0 {{RFC6749}} can convey authorization grants and access tokens. ARPA addresses persistent registry-resolvable agent, relationship, authority, lifecycle, and evidence state. An OAuth token can be evidence used by an ARPA-aware relying party, but token validity alone does not establish that all ARPA authority conditions remain satisfied.

HTTP Message Signatures {{RFC9421}} can authenticate signed HTTP messages. ARPA does not define a competing HTTP signature mechanism.

Well-known URIs {{RFC8615}} can provide discovery of registry metadata if the corresponding IANA registration is made. OAuth 2.0 Authorization Server Metadata {{RFC8414}} establishes precedent for a well-known-URI-based metadata document with a similar structure and update model; the ARPA registry metadata response follows a comparable pattern without asserting equivalence to OAuth server metadata.

Future revisions are expected to document relationships with current IETF workload identity, secure credential, attestation, and supply-chain transparency work after community review.

# Acknowledgements
{:unnumbered}

The author thanks contributors and reviewers of the ARPA project whose implementation, assurance, security, privacy, and interoperability feedback informed this protocol extraction.

--- back

# Design Notes

The ARPA project contains additional governance, redress, federation, assurance profiles, conformance catalogues, and implementation guidance that are intentionally not made normative by this document. This separation is intended to keep the Internet protocol surface independently implementable while allowing stronger deployment profiles to be developed separately.