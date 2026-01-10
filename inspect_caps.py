#!/usr/bin/env python3
import json
import collections
from pathlib import Path
from dedupe_cap_coverage import get_caps_waec, get_caps_nerdc, load_json, normalize_subject

w = json.load(open('wave3_content_database.json','r',encoding='utf-8'))
caps_w = get_caps_waec(load_json(Path('curriculum_map.json')))
counts_w = collections.Counter([normalize_subject(i.get('subject','Unknown')) for i in w['content']])
print('WAEC caps:', caps_w)
print('WAEC counts:', dict(counts_w))

n = json.load(open('connected_stack/backend/content_data.json','r',encoding='utf-8'))
caps_n = get_caps_nerdc(load_json(Path('nerdc_curriculum_map.json')))
counts_n = collections.Counter([normalize_subject(i.get('subject','Unknown')) for i in n['content']])
print('NERDC caps:', caps_n)
print('NERDC counts:', dict(counts_n))
