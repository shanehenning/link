from contentful_management import Client
import os, binascii, json

client = Client('CFPAT-b9d0bb66831b4cee396847c0467eace39cd05611526064d7079b3e57653928d6')
space_id = 'wjuty07n9kzp'
environment_id = 'master'

all_media = []
media_ids = []

with open('streaming-media.json') as f:
    data = json.load(f)


def createEntry(content):
    entry = client.entries(space_id, environment_id).create(content['id'], {
        'content_type_id': content['content_type'],
        'fields': content['fields']
    })
    # entry.publish()


def uploadMedia(content, asset_array, locale):
    asset = client.assets(space_id, environment_id).create(content['id'], {
        'fields': {
            'title': {
                locale: content['file_name']
            },
            'description': {
                locale: content['description']
            },
            'file': {
                locale: {
                    'contentType': content['content_type'],
                    'fileName': content['file_name'],
                    'upload': content['file_path']
                }
            }
        }
    })
    asset.process()
    asset_array.append(content['id'])


# this whole image thing is a cluster


def createImage(pic, location):
    if pic['id'] is None:
        pic['id'] = binascii.b2a_hex(os.urandom(11))
    new_pic = {
        'id': pic['id'],
        'file_name': pic['image-src'].split('/')[-1],
        'description': pic['image-alt'],
        'content_type': pic['type'],
        'file_path': pic['image-src']
    }
    uploadMedia(new_pic, asset_array, location)
    media_ids.append({'image': new_pic['file_name'], 'id': new_pic['id']})


def createThumbnailImage(thumb, location):
    new_thumb = {
        'id': binascii.b2a_hex(os.urandom(11)),
        'file_name': thumb['thumbnail-image-src'].split('/')[-1],
        'description': thumb['thumbnail-image-alt'],
        'content_type': thumb['thumbnail-type'],
        'file_path': 'http://www.secondstep.org' + thumb['thumbnail-image-src']
    }
    uploadMedia(new_thumb, asset_array, location)
    media_ids.append({'thumbnail-image': new_thumb['file_name'], 'id': new_thumb['id']})


def createVideoEntry(video, locale):
    fields = {
        'title': {
            locale: video['title']
        },
        'videoType': {
            locale: 'Video'
        },
        'poster': {
            locale: {
                'sys': {
                    'type': 'Link',
                    'linkType': 'Asset',
                    'id': video['poster-id']
                }
            }
        }
    }
    entry = client.entries(space_id, environment_id).create(video['id'], {
        'content_type_id': 'video',
        'fields': fields
    })
    # entry.publish()


for item_idx, item in enumerate(data):
    categories = []
    for english_category_idx, english_category in enumerate(item['content']['english']['categories']):
        for english_media_idx, english_media in enumerate(item['content']['english']['categories']['media-resource']):
            if isinstance(english_media['modal-media'], list):
                images = True
                for im_idx, im in enumerate(english['modal-media']):
                    loc = 'en-US'
                    createImage(im, 'en-US')
            else:
                if english_media['modal-media']['media-poster'] is None:
                    image = True
                    createImage(english_media['modal-media'], 'en-US')
                    createThumbnailImage(english_media, 'en-US')
                else:
                    video = True
                    vid = english_media['modal-media']
                    poster_extension = vid['media-poster'].split('.')[-1]
                    poster_image = {
                        'id': binascii.b2a_hex(os.urandom(11)),
                        'file_name': english_media['media-resource-title'] + '-poster.' + poster_extension,
                        'image-alt': ''
                        'content_type': 'image/' + poster_extension,
                        'file_path': vid['media-poster'],
                    }
                    createImage(poster_image, 'en-US')
                    new_vid = {
                        'id': binascii.b2a_hex(os.urandom(11)),
                        'title': english_media['media-resource-title'],
                        'content_type': vid['type'],
                        'file_path': vid['image-src'],
                        'poster-id': poster_image['id']
                    }
                    createVideoEntry(new_vid, locale)
                    # media_ids.append({'video': new_vid['file_name'], 'id': new_vid['id']})


# end image cluster


            # uploadMedia(media, all_media, 'en-US')

            new_category = {
                'title': {
                    'en-US': english_category['category-title']
                },
                'mediaResources': {
                    'en-US': english_category['media-resource']
                }
            }
        categories.append(new_category)
    for spanish_category_idx, spanish_category in enumerate(item['content']['spanish']['categories']):
        categories[spanish_category_idx]['title']['es-US'] = spanish_category['category-title']
        categories[spanish_category_idx]['mediaResources']['es-US'] = spanish_category['media-resource']

    new_object = {
        'title': {
            'en-US': item['page']
        },
        'description': {
            'en-US': 'Streaming Lesson Media songs, photos and videos for ' + item['page']
        },
        'categories': categories
    }
    print('new_object: ', new_object)
