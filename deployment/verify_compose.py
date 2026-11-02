"""Verify a real Compose database survives application and DB container recreation.

Run only against a disposable test Compose stack. Never deletes volumes.
"""
import json
import subprocess
import time
import urllib.request
from uuid import uuid4

BASE = 'http://127.0.0.1:8000'


def request(path, method='GET', body=None):
    payload = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=payload, method=method,
                                 headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=10) as response:
        data = response.read()
        return json.loads(data) if data else None


def main():
    group = request('/api/groups', 'POST', dict(name='Persistence ' + uuid4().hex[:8], currency='KZT', description='CI restart verification'))
    try:
        member = request(f'/api/groups/{group["id"]}/members', 'POST', {'name': 'Restart member'})
        debtor = request(f'/api/groups/{group["id"]}/members', 'POST', {'name': 'Restart debtor'})
        ledger_path = f'/api/groups/{group["id"]}'
        request(ledger_path + '/expenses', 'POST', dict(
            description='Restart dinner', amount_minor=1001, payer_id=member['id'],
            category='Food', date='2026-11-02', split_type='equal',
            split_values={member['id']: 1, debtor['id']: 1}))
        request(ledger_path + '/settlements', 'POST', dict(
            from_member_id=debtor['id'], to_member_id=member['id'],
            amount_minor=200, date='2026-11-02', note='Partial restart repayment'))
        before = {resource: request(ledger_path + '/' + resource)
                  for resource in ('members', 'expenses', 'settlements', 'balances', 'analytics')}
        subprocess.run(['docker', 'compose', 'up', '-d', '--force-recreate', '--wait', '--wait-timeout', '180'], check=True)
        for attempt in range(30):
            try:
                assert request('/api/health')['status'] == 'ok'
                break
            except (OSError, AssertionError):
                if attempt == 29:
                    raise
                time.sleep(1)
        groups = request('/api/groups')
        assert any(item['id'] == group['id'] for item in groups), 'Group lost on recreation'
        members = request(f'/api/groups/{group["id"]}/members')
        assert any(item['id'] == member['id'] for item in members), 'Member lost on recreation'
        assert request(ledger_path) == group, 'Group fields changed on recreation'
        after = {resource: request(ledger_path + '/' + resource) for resource in before}
        assert after == before, 'Ledger records or calculated balances changed on recreation'
        print('PASS: groups, members, expense shares, partial settlement, balances and analytics survived Compose recreation')
    finally:
        request(f'/api/groups/{group["id"]}', 'DELETE')


if __name__ == '__main__':
    main()
