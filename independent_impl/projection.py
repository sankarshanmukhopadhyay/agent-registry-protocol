"""Independent table-driven implementation of the informative projection profile."""
TABLE={'active':'candidate','suspended':'negative','revoked':'negative','expired':'negative','unknown':'indeterminate','conflicting':'indeterminate','unavailable':'indeterminate'}
def project(v):
    result=TABLE.get(v.get('state'),'indeterminate')
    if result!='candidate': return result
    guards=[v.get('scope_match',True),v.get('evidence_current',True)]
    if v.get('kind')=='recognition': guards += [not v.get('withdrawn',False),not v.get('transitive',False)]
    if not v.get('evidence_current',True): return 'indeterminate'
    return 'affirmative' if all(guards) else 'negative'
