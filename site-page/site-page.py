from contentful_management import Client
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import collections, json, re, time, os, binascii, tomd

all_media = []
with open('metadata.json') as f:
    excel_metadata = json.load(f)

client = Client('CFPAT-b9d0bb66831b4cee396847c0467eace39cd05611526064d7079b3e57653928d6')
space_id = 'wjuty07n9kzp'
environment_id = 'master'

driver = webdriver.Firefox()

URL = 'http://www.secondstep.org/Kindergarten/Program-Coordinators/Second-Step-Kit/Evaluation-Guide'
LOGIN_URL = 'http://login.secondstep.org/account/login'
USERNAME = 'mfahmy@cfchildren.org'
PASSWORD = 'forthechildren'


def site_login():
    driver.get(LOGIN_URL)
    driver.find_element_by_id('Email').send_keys(USERNAME)
    driver.find_element_by_id('Password').send_keys(PASSWORD)
    driver.find_element_by_class_name('login-bt').click()


def createEntry(content):
    entry = client.entries(space_id, environment_id).create(content['id'], {
        'content_type_id': content['content_type'],
        'fields': content['fields']
    })
    # entry.publish()


def uploadMedia(content, asset_array):
    asset = client.assets(space_id, environment_id).create(content['id'], {
        'fields': {
            'title': {
                'en-US': content['file_name']
            },
            'description': {
                'en-US': content['description']
            },
            'file': {
                'en-US': {
                    'contentType': content['content_type'],
                    'fileName': content['file_name'],
                    'upload': content['file_path']
                }
            }
        }
    })
    asset.process()
    asset_array.append(content['id'])


def publishAsset(id):
    processed_asset = client.assets(space_id, environment_id).find(id)
    processed_asset.publish()


def createPdfEntry(pdf):
    fields = {
        'title': {
            'en-US': pdf['fileName']
        },
        'descriptionMarkdown': {
            'en-US': pdf['title']
        },
        'file': {
            'en-US': {
                'sys': {
                    'type': 'Link',
                    'linkType': 'Asset',
                    'id': pdf['asset_id']
                }
            }
        },
        'product': {
            'en-US': pdf['product']
        },
        'gradeRange': {
            'en-US': pdf['gradeRange']
        },
        'resourceLibrary': {
            'en-US': pdf['resourceLibrary']
        },
        'audience': {
            'en-US': pdf['audience']
        },
        'writeable': {
            'en-US': pdf['writeable']
        }
    }
    entry = client.entries(space_id, environment_id).create(pdf['id'], {
        'content_type_id': 'pdf',
        'fields': fields
    })
    # entry.publish()


def pairMetadata(given, to_match, type):
    for metadata_idx, metadata in enumerate(excel_metadata[type]):
        if metadata[to_match] == given:
            return metadata_idx


# find pdfs and upload to contentful as assets, and create entries from those assets
def findPdfs(containing_class, pdf_array):
    pdf_links = driver.find_elements_by_xpath('//div[contains(@class, "' + containing_class + '")]//a[contains(@href, ".pdf")]')
    for pdf_link_idx, pdf_link in enumerate(pdf_links):
        new_pdf_asset = {
            'file_name': pdf_link.get_attribute('href').split('/')[-1],
            'file_path': pdf_link.get_attribute('href'),
            'id': binascii.b2a_hex(os.urandom(11)),
            'description': pdf_link.text,
            'content_type': 'application/pdf'
        }
        uploadMedia(new_pdf_asset, all_media)
        new_pdf_entry = {
            'title': new_pdf_asset['file_name'],
            'id': binascii.b2a_hex(os.urandom(11)),
            'asset_id': new_pdf_asset['id']
        }
        # add metadata from excel spreadsheet to pdf
        index = pairMetadata(new_pdf_asset['file_name'], 'fileName', 'pdf')
        pdf_exists = True
        if index is None:
            pdf_exists = False
            index = 0
        pdf_metadata = excel_metadata['pdf'][index]
        for key in pdf_metadata:
            new_pdf_entry[key] = pdf_metadata[key]
        if pdf_exists == False:
            new_pdf_entry['title'] = new_pdf_asset['description']
            new_pdf_entry['fileName'] = new_pdf_asset['file_name']
        pdf_array.append(new_pdf_entry)
        createPdfEntry(new_pdf_entry)


def scrape_content():
    soup = BeautifulSoup(driver.page_source.encode('utf-8'), 'html.parser')
    title = str(soup.find('h1').text).strip()
    content = soup.find('div', attrs={'class': 'cmt-two-third-pane'})
    index = pairMetadata(title, 'title', 'page')
    page_metadata = excel_metadata['page'][index]
    main_page = {
        'fields': {
            'title': { 'en-US': title },
            'pageContentMarkdown': { 'en-US': tomd.convert(str(content)).strip() },
            'product': { 'en-US': page_metadata['product'] },
            'audience': { 'en-US': page_metadata['audience'] },
            'gradeRange': { 'en-US': page_metadata['gradeRange'] },
            'internalLinks': { 'en-US': []},
            'pdf': { 'en-US': [] }
        },
        'id': binascii.b2a_hex(os.urandom(11)),
        'content_type': 'sitePage',
        'pdf_array': []
    }

    findPdfs('cmt-two-third-pane', main_page['pdf_array'])


    # navigate to sub-pages
    links = driver.find_elements_by_xpath('//div[contains(@class, "cmt-two-third-pane")]//li//a')
    length = len(links)
    counter = 0
    new_page_entry_ids = []
    while counter < length:
        # wait until main_page has loaded
        WebDriverWait(driver, 15).until(lambda driver: driver.find_elements_by_xpath('//div[contains(@class, "cmt-two-third-pane")]//li//a'))
        links = driver.find_elements_by_xpath('//div[contains(@class, "cmt-two-third-pane")]//li//a')
        links[counter].click()

        # wait until new_page has loaded
        WebDriverWait(driver, 15).until(lambda driver: driver.find_elements_by_xpath('//h1'))
        newSoup = BeautifulSoup(driver.page_source.encode('utf-8'), 'html.parser')
        title = newSoup.find('h1').text.strip()
        new_content = tomd.convert(str(newSoup.find('div', attrs={'class': 'cmt-two-third-pane'}))).strip()
        index = pairMetadata(title, 'title', 'page')
        page_metadata = excel_metadata['page'][index]
        new_page = {
            'fields': {
                'title': { 'en-US': title },
                'pageContentMarkdown': { 'en-US': new_content },
                'product': { 'en-US': page_metadata['product'] },
                'audience': { 'en-US': page_metadata['audience'] },
                'gradeRange': { 'en-US': page_metadata['gradeRange'] },
                'pdf': { 'en-US': [] }
            },
            'id': binascii.b2a_hex(os.urandom(11)),
            'content_type': 'sitePage',
            'pdf_array': []
        }
        findPdfs('cmt-two-third-pane', new_page['pdf_array'])
        for new_page_pdf_idx, new_page_pdf in enumerate(new_page['pdf_array']):
            new_page['fields']['pdf']['en-US'].append({'sys' : {"type": "Link", "linkType": "Entry", "id": new_page_pdf['id']}})

        new_page_entry_ids.append(new_page['id'])
        createEntry(new_page)

        driver.execute_script('window.history.go(-1)')
        counter += 1

    for id_idx, id in enumerate(new_page_entry_ids):
        main_page['fields']['internalLinks']['en-US'].append({'sys' : {"type": "Link", "linkType": "Entry", "id": id}})
    # end navigate to sub-pages


    for main_page_pdf_idx, main_page_pdf in enumerate(main_page['pdf_array']):
        main_page['fields']['pdf']['en-US'].append({'sys' : {"type": "Link", "linkType": "Entry", "id": main_page_pdf['id']}})
    createEntry(main_page)
    # for media_idx, media in enumerate(all_media):
        # publishAsset(media)



site_login()
driver.get(URL)
scrape_content()
driver.quit()
