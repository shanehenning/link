from contentful_management import Client
import os, binascii, json

client = Client('CFPAT-b9d0bb66831b4cee396847c0467eace39cd05611526064d7079b3e57653928d6')
space_id = 'wjuty07n9kzp'
environment_id = 'master'

pages = []

with open('streaming-media.json') as f:
    data = json.load(f)


for page_idx, page in enumerate(data):
    new_object = {
        'categories': []
    }
    placeholder = page['content'][0]

    for category_idx, category in enumerate(page['content'][1]['items']['categories']):
        new_object['categories'].append({})
        if category['category-title'] == placeholder['items']['categories'][category_idx]['category-title']:
            new_object['categories'][category_idx]['category-title'] = {
                'en-US': category['category-title']
            }
        else:
            new_object['categories'][category_idx]['category-title'] = {
                'en-US': placeholder['items']['categories'][category_idx]['category-title'],
                'es-US': category['category-title']
            }
            new_object['categories'][category_idx]['media-resource'] = []
        for media_resource_idx, media_resource in enumerate(category['media-resource']):
            new_object['categories'][category_idx]['media-resource'].append({})
            if media_resource['thumbnail-image-src'] == placeholder['items']['categories'][category_idx]['media-resource'][media_resource_idx]['thumbnail-image-src']:
                new_object['categories'][category_idx]['media-resource'][media_resource_idx]['thumbnail-image-src'] = {
                    'en-US': 'http://www.secondstep.org' + media_resource['thumbnail-image-src']
                }
            else:
                new_object['categories'][category_idx]['media-resource'][media_resource_idx]['thumbnail-image-src'] = {
                    'en-US': 'http://www.secondstep.org' + placeholder['items']['categories'][category_idx]['media-resource'][media_resource_idx]['thumbnail-image-src'],
                    'es-US': 'http://www.secondstep.org' + media_resource['thumbnail-image-src']
                }
            if media_resource['thumbnail-image-alt'] == placeholder['items']['categories'][category_idx]['media-resource'][media_resource_idx]['thumbnail-image-alt']:
                new_object['categories'][category_idx]['media-resource'][media_resource_idx]['thumbnail-image-alt'] = {
                    'en-US': media_resource['thumbnail-image-alt']
                }
            else:
                new_object['categories'][category_idx]['media-resource'][media_resource_idx]['thumbnail-image-alt'] = {
                    'en-US': placeholder['items']['categories'][category_idx]['media-resource'][media_resource_idx]['thumbnail-image-alt'],
                    'es-US': media_resource['thumbnail-image-alt']
                }
            if media_resource['thumbnail-type'] == placeholder['items']['categories'][category_idx]['media-resource'][media_resource_idx]['thumbnail-type']:
                new_object['categories'][category_idx]['media-resource'][media_resource_idx]['thumbnail-type'] = media_resource['thumbnail-type']
            else:
                new_object['categories'][category_idx]['media-resource'][media_resource_idx]['thumbnail-type'] = {
                    'en-US': placeholder['items']['categories'][category_idx]['media-resource'][media_resource_idx]['thumbnail-type'],
                    'es-US': media_resource['thumbnail-type']
                }
            if media_resource['media-resource-title'] == placeholder['items']['categories'][category_idx]['media-resource'][media_resource_idx]['media-resource-title']:
                new_object['categories'][category_idx]['media-resource'][media_resource_idx]['media-resource-title'] = {
                    'en-US': media_resource['media-resource-title']
                }
            else:
                new_object['categories'][category_idx]['media-resource'][media_resource_idx]['media-resource-title'] = {
                    'en-US': placeholder['items']['categories'][category_idx]['media-resource'][media_resource_idx]['media-resource-title'],
                    'es-US': media_resource['media-resource-title']
                }

            if isinstance(media_resource['modal-media'], list):
                new_object['categories'][category_idx]['media-resource'][media_resource_idx]['modal-media'] = []
                for im_idx, im in enumerate(media_resource['modal-media']):
                    new_object['categories'][category_idx]['media-resource'][media_resource_idx]['modal-media'].append({})
                    if im['image-src'] == placeholder['items']['categories'][category_idx]['media-resource'][media_resource_idx]['modal-media'][im_idx]['image-src']:
                        new_object['categories'][category_idx]['media-resource'][media_resource_idx]['modal-media'][im_idx]['image-src'] = {
                            'en-US': im['image-src']
                        }
                    else:
                        new_object['categories'][category_idx]['media-resource'][media_resource_idx]['modal-media'][im_idx]['image-src'] = {
                            'en-US': placeholder['items']['categories'][category_idx]['media-resource'][media_resource_idx]['modal-media'][im_idx]['image-src'],
                            'es-US': im['image-src']
                        }
                    if im['image-alt'] == placeholder['items']['categories'][category_idx]['media-resource'][media_resource_idx]['modal-media'][im_idx]['image-alt']:
                        new_object['categories'][category_idx]['media-resource'][media_resource_idx]['modal-media'][im_idx]['image-alt'] = {
                            'en-US': im['image-alt']
                        }
                    else:
                        new_object['categories'][category_idx]['media-resource'][media_resource_idx]['modal-media'][im_idx]['image-alt'] = {
                            'en-US': placeholder['items']['categories'][category_idx]['media-resource'][media_resource_idx]['modal-media'][im_idx]['image-alt'],
                            'es-US': im['image-alt']
                        }
                    if im['media-title'] == placeholder['items']['categories'][category_idx]['media-resource'][media_resource_idx]['modal-media'][im_idx]['media-title']:
                        new_object['categories'][category_idx]['media-resource'][media_resource_idx]['modal-media'][im_idx]['media-title'] = {
                            'en-US': im['media-title']
                        }
                    else:
                        new_object['categories'][category_idx]['media-resource'][media_resource_idx]['modal-media'][im_idx]['media-title'] = {
                            'en-US': placeholder['items']['categories'][category_idx]['media-resource'][media_resource_idx]['modal-media'][im_idx]['media-title'],
                            'es-US': im['media-title']
                        }
        else:
            new_object['categories'][category_idx]['media-resource'][media_resource_idx]['modal-media'] = {}
            if media_resource['modal-media']['limelight-id'] == placeholder['items']['categories'][category_idx]['media-resource'][media_resource_idx]['modal-media']['limelight-id']:
                new_object['categories'][category_idx]['media-resource'][media_resource_idx]['modal-media']['limelight-id'] = {
                    'en-US': media_resource['modal-media']['limelight-id']
                }
            else:
                new_object['categories'][category_idx]['media-resource'][media_resource_idx]['modal-media']['limelight-id'] = {
                    'en-US': placeholder['items']['categories'][category_idx]['media-resource'][media_resource_idx]['modal-media']['limelight-id'],
                    'es-US': media_resource['modal-media']['limelight-id']
                }
            if media_resource['modal-media']['limelight-poster'] == placeholder['items']['categories'][category_idx]['media-resource'][media_resource_idx]['modal-media']['limelight-poster']:
                new_object['categories'][category_idx]['media-resource'][media_resource_idx]['modal-media']['limelight-poster'] = {
                    'en-US': media_resource['modal-media']['limelight-poster']
                }
            else:
                new_object['categories'][category_idx]['media-resource'][media_resource_idx]['modal-media']['limelight-poster'] = {
                    'en-US': placeholder['items']['categories'][category_idx]['media-resource'][media_resource_idx]['modal-media']['limelight-poster'],
                    'es-US': media_resource['modal-media']['limelight-poster']
                }
            if media_resource['modal-media']['type'] == placeholder['items']['categories'][category_idx]['media-resource'][media_resource_idx]['modal-media']['type']:
                new_object['categories'][category_idx]['media-resource'][media_resource_idx]['modal-media']['type'] = media_resource['modal-media']['type']
            else:
                new_object['categories'][category_idx]['media-resource'][media_resource_idx]['modal-media']['type'] = {
                    'en-US': placeholder['items']['categories'][category_idx]['media-resource'][media_resource_idx]['modal-media']['type'],
                    'es-US': media_resource['modal-media']['type']
                    }
            if media_resource['modal-media']['poster-type'] == placeholder['items']['categories'][category_idx]['media-resource'][media_resource_idx]['modal-media']['poster-type']:
                new_object['categories'][category_idx]['media-resource'][media_resource_idx]['modal-media']['poster-type'] = media_resource['modal-media']['poster-type']
            else:
                new_object['categories'][category_idx]['media-resource'][media_resource_idx]['modal-media']['poster-type'] = {
                    'en-US': placeholder['items']['categories'][category_idx]['media-resource'][media_resource_idx]['modal-media']['poster-type'],
                    'es-US': media_resource['modal-media']['poster-type']
                }

    pages.append({'page': page['page'], 'content': new_object })

with open('streaming-media-transformed.json', 'w') as f:
    f.write(json.dumps(pages, ensure_ascii=False).encode('utf8'))
