from __future__ import annotations
import hashlib, json
from typing import Any

COMPETENT_ISSUERS = {
    'developed_by': {'developer', 'authorized_publisher'},
    'published_by': {'publisher'},
    'deployed_by': {'deployer', 'governance_authority'},
    'operated_by': {'operator', 'governance_authority'},
    'controlled_by': {'current_controller', 'governance_authority'},
    'accountable_to': {'accountable_entity', 'governance_authority'},
    'assured_by': {'assurance_provider'},
    'governed_by': {'governance_authority'},
    'acts_for': {'principal'},
    'recognized_by': {'recognizing_governance_authority'},
}

NON_TRANSFERABLE = {
    'delegations', 'assurance_claims', 'runtime_credentials',
    'accountable_entity_status', 'sponsor_endorsements',
    'confidential_evidence_access', 'governance_recognition',
    'downstream_authority',
}

def canonical_digest(document: dict[str, Any], excluded: set[str] | None = None) -> str:
    body = {k: v for k, v in document.items() if k not in (excluded or {'proof'})}
    canonical = json.dumps(body, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
    return 'sha256:' + hashlib.sha256(canonical).hexdigest()

def issuer_competent(relationship_type: str, issuer_role: str) -> bool:
    return issuer_role in COMPETENT_ISSUERS.get(relationship_type, set())

def transfer_outcomes(assertions: list[str], explicit_novations: list[str]) -> dict[str, str]:
    novated = set(explicit_novations)
    return {name: ('requires_reissuance' if name in NON_TRANSFERABLE and name not in novated else 'remains_valid') for name in assertions}

def detect_event_gap(sequences: list[int]) -> bool:
    return any(b != a + 1 for a, b in zip(sequences, sequences[1:]))

def resolve_alias_graph(start: str, bindings: dict[str, list[str]], max_depth: int = 8) -> tuple[str, list[str]]:
    visited=[]; current=start
    for _ in range(max_depth):
        if current in visited: return 'conflict', ['alias_loop']
        visited.append(current)
        targets=bindings.get(current, [])
        if not targets: return 'resolved', [current]
        unique=sorted(set(targets))
        if len(unique)>1: return 'conflict', ['alias_conflict']
        current=unique[0]
    return 'indeterminate', ['alias_depth_exceeded']

def delegation_chain_valid(chain: list[dict[str, Any]]) -> tuple[bool, list[str]]:
    for parent, child in zip(chain, chain[1:]):
        if not set(child.get('actions', [])).issubset(parent.get('actions', [])):
            return False, ['downstream_action_expansion']
        if parent.get('resources') and not set(child.get('resources', [])).issubset(parent['resources']):
            return False, ['downstream_resource_expansion']
        if parent.get('jurisdictions') and not set(child.get('jurisdictions', [])).issubset(parent['jurisdictions']):
            return False, ['downstream_jurisdiction_expansion']
        if child.get('per_transaction', 0) > parent.get('per_transaction', float('inf')):
            return False, ['downstream_limit_expansion']
        if not set(parent.get('prohibitions', [])).issubset(child.get('prohibitions', [])):
            return False, ['prohibition_not_inherited']
    return True, ['delegation_chain_narrowed']

def recognition_effective(status: str, at: str, effective_until: str | None = None) -> tuple[bool, list[str]]:
    if status == 'withdrawn': return False, ['recognition_withdrawn']
    if effective_until and at > effective_until: return False, ['recognition_expired']
    return True, ['recognition_active']

def lifecycle_transition_allowed(prior: str, new: str) -> bool:
    allowed = {
        'active': {'restricted','suspended','quarantined','retired','superseded','under_investigation'},
        'suspended': {'active','restricted','revoked','under_investigation'},
        'under_investigation': {'active','restricted','suspended','revoked'},
        'restricted': {'active','suspended','retired','revoked'},
    }
    return new in allowed.get(prior, set())
