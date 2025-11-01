"""Super Hub Simulator

This script registers a Super Hub with the IG-Hub control panel (admin key required),
receives an issued API key, then publishes an anonymized metadata payload.

Designed to run against a local IG-Hub instance (default http://localhost:8080) or
inside CI where the IG-Hub server is started in the workflow.
"""
import os
import requests
import json
import time
import sys

BASE = os.environ.get('IG_HUB_BASE', 'http://localhost:8080')
ADMIN_KEY = os.environ.get('IG_HUB_ADMIN_KEY', 'admin-secret-example')


def register(super_id='sh-sim-001', country='NG'):
    url = f"{BASE}/superhubs/register"
    headers = {'X-API-KEY': ADMIN_KEY}
    payload = {'superHubId': super_id, 'countryCode': country, 'publicKey': 'sim-pk'}
    r = requests.post(url, json=payload, headers=headers, timeout=10)
    r.raise_for_status()
    return r.json()['apiKey']


def publish(api_key, super_id='sh-sim-001'):
    url = f"{BASE}/metadata/publish"
    headers = {'X-API-KEY': api_key}
    payload = {'superHubId': super_id, 'datasetId': 'sim-d-1', 'anonymizedPayload': {'count': 1, 'ts': int(time.time())}}
    r = requests.post(url, json=payload, headers=headers, timeout=10)
    r.raise_for_status()
    return r.json()


def main():
    print('Simulator: registering Super Hub...')
    try:
        api_key = register()
        print('Simulator: received api_key:', api_key)
    except Exception as e:
        print('Registration failed:', e)
        sys.exit(2)

    print('Simulator: publishing metadata...')
    try:
        res = publish(api_key)
        print('Publish response:', res)
    except Exception as e:
        print('Publish failed:', e)
        sys.exit(3)

    print('Simulator: success')
    return 0


if __name__ == '__main__':
    sys.exit(main())
