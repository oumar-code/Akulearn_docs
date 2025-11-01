import json
from infra.examples.data_sanitizer import anonymize_pii


def test_anonymize_basic_fields():
    record = {
        'user_id': 42,
        'name': 'Test User',
        'email': 'test.user@example.com',
        'phone_number': '+1234567890',
        'address': '1 Test St'
    }
    out = anonymize_pii(record)
    assert out.get('name') == '[ANONYMIZED_NAME]'
    assert out.get('email') == '[ANONYMIZED_EMAIL]'
    assert out.get('phone_number') == '[ANONYMIZED_PHONE]'
    assert out.get('address') == '[ANONYMIZED_ADDRESS]'
    # user_id should be removed and replaced with a hash
    assert 'user_id' not in out
    assert 'user_id_hash' in out
