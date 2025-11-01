import json
from fastapi.testclient import TestClient

from infra.examples.ig_hub_control_panel import main as ig_main


client = TestClient(ig_main.app)


def test_register_and_status_with_admin_key(monkeypatch):
    # ensure DB is init'd in a temp location
    monkeypatch.setenv('IGHUB_DB_PATH', ':memory:')
    monkeypatch.setenv('IGHUB_ADMIN_API_KEY', 'admin-test-key')
    # reinit app DB
    ig_main.init_db()

    payload = {
        'superHubId': 'sh-001',
        'countryCode': 'NG',
        'publicKey': 'pubkey-xyz'
    }
    r = client.post('/superhubs/register', json=payload, headers={'X-API-KEY': 'admin-test-key'})
    assert r.status_code == 200
    data = r.json()
    assert data.get('status') == 'ok'
    assert 'apiKey' in data
    api_key = data['apiKey']

    status = client.get('/connectivity/status')
    assert status.status_code == 200
    data2 = status.json()
    assert data2['registeredSuperHubs'] >= 1


def test_publish_metadata_requires_registration():
    payload = {
        'superHubId': 'unknown',
        'datasetId': 'd-1',
        'anonymizedPayload': {'count': 1}
    }
    r = client.post('/metadata/publish', json=payload, headers={'X-API-KEY': 'nope'})
    assert r.status_code == 403


def test_publish_after_registration(monkeypatch):
    monkeypatch.setenv('IGHUB_DB_PATH', ':memory:')
    monkeypatch.setenv('IGHUB_ADMIN_API_KEY', 'admin-test-key')
    ig_main.init_db()

    reg = {
        'superHubId': 'sh-002',
        'countryCode': 'GH',
        'publicKey': 'pk-2'
    }
    r = client.post('/superhubs/register', json=reg, headers={'X-API-KEY': 'admin-test-key'})
    assert r.status_code == 200
    api_key = r.json()['apiKey']

    payload = {
        'superHubId': 'sh-002',
        'datasetId': 'd-2',
        'anonymizedPayload': {'metric': 42}
    }
    r2 = client.post('/metadata/publish', json=payload, headers={'X-API-KEY': api_key})
    assert r2.status_code == 200
    assert r2.json().get('status') == 'accepted'
