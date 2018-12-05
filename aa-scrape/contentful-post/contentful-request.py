from contentful_management import Client
client = Client('CFPAT-b9d0bb66831b4cee396847c0467eace39cd05611526064d7079b3e57653928d6')

import os, binascii, json
with open('test2.json') as f:
    data = json.load(f)

for val in data:
    # print('id: ', val['id'])
    entry_id = binascii.b2a_hex(os.urandom(11))
    entry = client.entries('wjuty07n9kzp', 'Feature').create(entry_id, {
    'content_type_id': 'advisoryActivityServiceLearning',
    'fields': val
    })
    # entry.publish()
