from contentful_management import Client
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import collections, json, re, time, os, binascii, tomd

with open('metadata.json') as f:
    page_metadata = json.load(f)

client = Client('CFPAT-b9d0bb66831b4cee396847c0467eace39cd05611526064d7079b3e57653928d6')
space_id = 'wjuty07n9kzp'
environment_id = 'master'

driver = webdriver.Firefox()

URL = 'http://www.secondstep.org/Early-Learning/Program-Coordinators/Second-Step-Kit/Evaluation-Guide'
LOGIN_URL = 'http://login.secondstep.org/account/login'
USERNAME = 'mfahmy@cfchildren.org'
PASSWORD = 'forthechildren'

def site_login():
    driver.get(LOGIN_URL)
    driver.find_element_by_id('Email').send_keys(USERNAME)
    driver.find_element_by_id('Password').send_keys(PASSWORD)
    driver.find_element_by_class_name('login-bt').click()


def publishContent(fields, entry_id):
    client = Client('CFPAT-b9d0bb66831b4cee396847c0467eace39cd05611526064d7079b3e57653928d6')
    entry = client.entries(space_id, environment_id).create(entry_id, {
        'content_type_id': 'sitePage',
        'fields': fields
    })
    # entry.publish()

def uploadResource(file, file_path, asset_id, title, resource_type):
    asset = client.assets(space_id, environment_id).create(asset_id, {
        'fields': {
            'title': {
                'en-US': title
            },
            'file': {
                'en-US': {
                    'contentType': resource_type,
                    'fileName': file,
                    'upload': file_path
                }
            }
        }
    })
    asset.process()

# find pdfs and upload to contentful as assets
def findPdfs(containing_class, pdf_array):
    pdf_links = driver.find_elements_by_xpath('//div[contains(@class, ' + containing_class + ')]//a[contains(@href, ".pdf")]')
    for pdf_link_idx, pdf_link in enumerate(pdf_links):
        new_pdf = {}
        new_pdf['file_name'] = pdf_link.get_attribute('href').split('/')[-1]
        new_pdf['title'] = pdf_link.text
        new_pdf['id'] = binascii.b2a_hex(os.urandom(11))
        pdf_array.append(new_pdf)
        uploadResource(new_pdf['file_name'], pdf_link.get_attribute('href'), new_pdf['id'], new_pdf['title'], 'application/pdf')


def pairMetadata(matcher):
    for metadata_idx, metadata in enumerate(page_metadata):
        if metadata['title'] == matcher:
            return metadata_idx


def scrape_content():
    main_page = {}
    soup = BeautifulSoup(driver.page_source.encode('utf-8'), 'html.parser')
    main_page['title'] = {}
    main_page['title']['en-US'] = soup.find('h1').text.strip()
    content = soup.find('div', attrs={'class': 'mainbox'})
    main_page['pageContentMarkdown'] = {}
    main_page['pageContentMarkdown']['en-US'] = tomd.convert(str(content)).strip()

    index = pairMetadata(main_page['title']['en-US'])
    main_page['product'] = {}
    # print('index: ', index)
    # print('page_metadata[index]: ', page_metadata[index])
    main_page['product']['en-US'] = page_metadata[index]['product']
    main_page['audience'] = {}
    main_page['audience']['en-US'] = page_metadata[index]['audience']
    main_page['gradeRange'] = {}
    main_page['gradeRange']['en-US'] = page_metadata[index]['gradeRange']


    main_page_pdfs = []
    findPdfs('mainbox', main_page_pdfs)
    time.sleep(1)
    for pdf_idx, pdf in enumerate(main_page_pdfs):
        asset = client.assets(space_id, environment_id).find(pdf['id'])

    links = driver.find_elements_by_xpath('//div[contains(@class, "mainbox")]//li//a')
    length = len(links)
    counter = 0
    entry_ids = []
    # navigate to sub-pages
    while counter < length:
        new_page = {}
        new_id = ''
        WebDriverWait(driver, 15).until(lambda driver: driver.find_elements_by_xpath('//div[contains(@class, "mainbox")]//li//a'))
        links = driver.find_elements_by_xpath('//div[contains(@class, "mainbox")]//li//a')
        links[counter].click()

        WebDriverWait(driver, 15).until(lambda driver: driver.find_elements_by_xpath('//h1'))
        newSoup = BeautifulSoup(driver.page_source.encode('utf-8'), 'html.parser')
        new_page_title = newSoup.find('h1').text.strip()
        new_page['title'] = {}
        new_page['title']['en-US'] = new_page_title
        new_content = newSoup.find('div', attrs={'class': 'LeftTwoThirdsPane'})
        new_content = tomd.convert(str(new_content)).strip()
        new_page['pageContentMarkdown'] = {}
        new_page['pageContentMarkdown']['en-US'] = new_content

        index = pairMetadata(new_page['title']['en-US'])
        new_page['product'] = {}
        new_page['product']['en-US'] = page_metadata[index]['product']
        new_page['audience'] = {}
        new_page['audience']['en-US'] = page_metadata[index]['audience']
        new_page['gradeRange'] = {}
        new_page['gradeRange']['en-US'] = page_metadata[index]['gradeRange']


        new_page_pdfs = []
        findPdfs('LeftTwoThirdsPane', new_page_pdfs)

        new_id = binascii.b2a_hex(os.urandom(11))
        print('new_page: ', new_page)
        publishContent(new_page, new_id)
        entry_ids.append(new_id)


        driver.execute_script('window.history.go(-1)')
        counter += 1

    main_page['internalLinks'] = {}
    main_page['internalLinks']['en-US'] = []
    for id_idx, id in enumerate(entry_ids):
        main_page['internalLinks']['en-US'].append({'sys' : {"type": "Link", "linkType": "Entry", "id": id}})
    publishContent(main_page, binascii.b2a_hex(os.urandom(11)))

site_login()
driver.get(URL)
scrape_content()






    # curl --include \
    #      --request GET \
    #      https://cdn.contentful.com/spaces/wjuty07n9kzp/environments/master/entry/5nuNxy1PluCvgensQ7uNTD?&access_token=de842675273a862fc0578632df2c95cf97ea6590de1820075c0abf2853e5ac22
# curl --include \
#      --request GET \
#      https://api.contentful.com/spaces/wjuty07n9kzp/environments/master/assets?access_token=CFPAT-b9d0bb66831b4cee396847c0467eace39cd05611526064d7079b3e57653928d6
