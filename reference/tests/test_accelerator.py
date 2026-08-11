import json
from pathlib import Path
from fastapi.testclient import TestClient
from reference.app import app, store

client=TestClient(app)
ROOT=Path(__file__).resolve().parents[2]

def test_accelerator_metadata_version():
    assert client.get('/health').json()['version']=='0.9.4'
    assert client.get('/registry').json()['arpa_version']=='0.9.0'
    assert client.get('/registry').json()['implementation_release']=='0.9.4'

def test_acme_fixture_lifecycle():
    fixture_dir=ROOT/'implementation-accelerator/fixtures/acme'
    core=json.loads((fixture_dir/'agent-core.json').read_text())
    response=client.post('/agents',json=core)
    assert response.status_code in (201,409)
    for name in ['status.json','governance.json','service-endpoint.json','identifier-alias.json','authority-envelope.json']:
        response=client.post('/records',json=json.loads((fixture_dir/name).read_text()))
        assert response.status_code==201
    resolved=client.get('/agents/agentreg:acme.example:procurement-review')
    assert resolved.status_code==200
    assert resolved.json()['authoritativeness']=='authoritative'
    alias=client.get('/aliases/acme:procurement-review')
    assert alias.status_code==200

def test_allow_and_deny_requests_produce_receipts():
    for name in ['authority-allow.json','authority-deny.json']:
        payload=json.loads((ROOT/'implementation-accelerator/requests'/name).read_text())
        result=client.post('/authority/evaluate',json=payload)
        assert result.status_code==200
        assert 'decision_receipt' in result.json()


def test_publication_discovery_has_no_authority_implication():
    result=client.get('/agents')
    assert result.status_code==200
    for item in result.json()['items']:
        assert item['authority_implication'] is False
        assert item['disclosure_class']=='public'


def test_historical_resolution_separates_requested_and_current_state():
    fixture_dir=ROOT/'implementation-accelerator/fixtures/acme'
    core=json.loads((fixture_dir/'agent-core.json').read_text())
    client.post('/agents',json=core)
    status=json.loads((fixture_dir/'status.json').read_text())
    client.post('/records',json=status)
    result=client.get('/agents/agentreg:acme.example:procurement-review/historical-resolution',params={'at':status['effective_at']})
    assert result.status_code==200
    body=result.json()
    assert body['requested_time']==status['effective_at']
    assert 'state_at_requested_time' in body
    assert 'current_state' in body
    assert body['reconstruction_status']=='authoritative_complete'
