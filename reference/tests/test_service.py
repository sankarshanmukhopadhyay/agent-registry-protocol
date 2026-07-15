from fastapi.testclient import TestClient
from reference.app import app, store
client=TestClient(app)

def test_health(): assert client.get('/health').json()['status']=='ok'
def test_registry_separates_modules():
    data=client.get('/registry').json(); assert 'ARPA-Core' in data['supported_modules']; assert 'ARPA-Assurance' not in data['supported_modules']

def test_register_resolve_and_non_reassignable():
    r={'record_id':'test-core-1','record_type':'agent_core','schema_version':'1.0.0','issuer':'registry:reference','subject':'agentreg:test:one','issued_at':'2026-07-15T00:00:00Z','effective_from':'2026-07-15T00:00:00Z','effective_until':None,'status':'active','agent_id':'agentreg:test:one','name':'Test Agent','agent_class':'informational','registration_status':'active'}
    assert client.post('/agents',json=r).status_code==201
    assert client.get('/agents/agentreg:test:one').status_code==200
    assert client.post('/agents',json=r).status_code==409

def test_alias_conflict_is_not_silent():
    base={'record_type':'identifier-alias','schema_version':'1.0.0','issuer':'registry:reference','subject':'agentreg:test:one','issued_at':'2026-07-15T00:00:00Z','effective_from':'2026-07-15T00:00:00Z','effective_until':None,'status':'active','alias':'did:example:shared','namespace':'did','binding_type':'equivalent_subject','competence_basis':'registry-policy','alias_status':'active'}
    a=dict(base,record_id='alias-1',canonical_id='agentreg:test:one'); b=dict(base,record_id='alias-2',canonical_id='agentreg:test:two',subject='agentreg:test:two')
    client.post('/records',json=a); client.post('/records',json=b)
    assert client.get('/aliases/did:example:shared').status_code==409
