"""
Simple Super Hub client demo script:
- Register a Super Hub (requires admin API key)
- Publish anonymized metadata using the issued Super Hub API key

Usage:
  python client.py register --admin-key admin-secret-example --id sh-demo --country NG
  python client.py publish --api-key <issued> --id sh-demo --dataset d1 --payload '{"count":1}'
"""
import argparse
import requests
import json

BASE = 'http://localhost:8080'


def register(admin_key, shid, country, public_key='demo-pk'):
    url = f'{BASE}/superhubs/register'
    headers = {'X-API-KEY': admin_key}
    payload = {'superHubId': shid, 'countryCode': country, 'publicKey': public_key}
    r = requests.post(url, json=payload, headers=headers)
    print(r.status_code, r.text)
    return r


def publish(api_key, shid, dataset, payload_json):
    url = f'{BASE}/metadata/publish'
    headers = {'X-API-KEY': api_key}
    payload = {'superHubId': shid, 'datasetId': dataset, 'anonymizedPayload': payload_json}
    r = requests.post(url, json=payload, headers=headers)
    print(r.status_code, r.text)
    return r


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest='cmd')
    reg = sub.add_parser('register')
    reg.add_argument('--admin-key', required=True)
    reg.add_argument('--id', required=True)
    reg.add_argument('--country', required=True)

    pub = sub.add_parser('publish')
    pub.add_argument('--api-key', required=True)
    pub.add_argument('--id', required=True)
    pub.add_argument('--dataset', required=True)
    pub.add_argument('--payload', required=True)

    args = p.parse_args()
    if args.cmd == 'register':
        register(args.admin_key, args.id, args.country)
    elif args.cmd == 'publish':
        publish(args.api_key, args.id, args.dataset, json.loads(args.payload))
*** End Patch