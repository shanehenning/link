from contentful_management import Client
import os, binascii, json

client = Client('CFPAT-b9d0bb66831b4cee396847c0467eace39cd05611526064d7079b3e57653928d6')
space_id = 'wjuty07n9kzp'
environment_id = 'master'

all_media = []
media_ids = []

with open('streaming-media-transformed.json') as f:
    data = json.load(f)


for page_idx, page in enumerate(data):
    for category_idx, category in enumerate(data['content']['categories']):
        
