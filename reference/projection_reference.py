from __future__ import annotations

def project(vector: dict) -> str:
    state=vector['state']
    if state in {'unknown','conflicting','unavailable'}: return 'indeterminate'
    if state in {'revoked','suspended','expired'}: return 'negative'
    if not vector.get('scope_match',True): return 'negative'
    if vector['kind']=='recognition' and (vector.get('withdrawn') or vector.get('transitive')): return 'negative'
    if not vector.get('evidence_current',True): return 'indeterminate'
    return 'affirmative'
