import re
import json

def anonymize_pii(data_record: dict) -> dict:
    """
    Anonymizes simple Personally Identifiable Information (PII) fields from a data record.
    This is intentionally conservative — production-grade sanitization should use
    a policy-driven engine (with schema-awareness) and proper hashing/salting.
    """
    anonymized_record = data_record.copy()
    # Anonymize name
    if 'name' in anonymized_record and anonymized_record['name']:
        anonymized_record['name'] = '[ANONYMIZED_NAME]'
    # Anonymize email using simple regex replacement
    if 'email' in anonymized_record and anonymized_record['email']:
        anonymized_record['email'] = re.sub(r'(.+)@(.+)\.(.+)', r'[ANONYMIZED_EMAIL]', anonymized_record['email'])
    # Phone: remove digits
    if 'phone_number' in anonymized_record and anonymized_record['phone_number']:
        anonymized_record['phone_number'] = '[ANONYMIZED_PHONE]'
    # Address: remove street-level detail
    if 'address' in anonymized_record and anonymized_record['address']:
        anonymized_record['address'] = '[ANONYMIZED_ADDRESS]'

    # Example of pseudonymization via hashing (optional)
    if 'user_id' in anonymized_record:
        try:
            import hashlib
            uid = str(anonymized_record['user_id']).encode('utf-8')
            anonymized_record['user_id_hash'] = hashlib.sha256(uid).hexdigest()
            # remove original
            anonymized_record.pop('user_id', None)
        except Exception:
            pass

    return anonymized_record


if __name__ == '__main__':
    sample = {
        'user_id': 12345,
        'name': 'Aisha Bello',
        'email': 'aisha.bello@example.org',
        'phone_number': '+2348012345678',
        'address': '12 Example St, Lagos'
    }
    print('Original:', json.dumps(sample, indent=2))
    print('Anonymized:', json.dumps(anonymize_pii(sample), indent=2))
