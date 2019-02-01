# -*- coding: utf-8 -*-

from contentful_management import Client
import json, binascii, os

client = Client('CFPAT-b9d0bb66831b4cee396847c0467eace39cd05611526064d7079b3e57653928d6')
space_id = 'wjuty07n9kzp'
environment_id = 'master'

with open('streaming-media.json') as f:
    data = json.load(f)

new_text = data['kindergarten-lesson-16']['spanish']['categories'][2]['Dar seguimiento'][0]['item-title']
print('new_text: ', new_text)

def convertText(text):
    return ('u"' + text + '"').encode("utf-8")

print(convertText(new_text))
convertedText = {'text': convertText(new_text)}

# with open('streaming-media2.json', 'w') as f:
#     f.write(json.dumps(convertedText))

id = binascii.b2a_hex(os.urandom(11))

test = {
    'title': {
        'en-US': convertedText
    }
}

def createEntry(content):
    entry = client.entries(space_id, environment_id).create(id, {
        'content_type_id': 'sitePage',
        'fields': content
    })
    # entry.publish()

createEntry(test)
