from contentful_management import Client
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import collections, json, re, time, os, binascii, tomd

client = Client('CFPAT-b9d0bb66831b4cee396847c0467eace39cd05611526064d7079b3e57653928d6')

driver = webdriver.Chrome()


URL = 'http://www.secondstep.org/Early-Learning/Program-Coordinators/Second-Step-Kit/Evaluation-Guide/Evaluating-Implementation'
LOGIN_URL = 'http://login.secondstep.org/account/login'
USERNAME = 'mfahmy@cfchildren.org'
PASSWORD = 'forthechildren'

def site_login():
    driver.get(LOGIN_URL)
    driver.find_element_by_id('Email').send_keys(USERNAME)
    driver.find_element_by_id('Password').send_keys(PASSWORD)
    driver.find_element_by_class_name('login-bt').click()


def publishContent(fields, entry_id, content_type):
    entry = client.entries('wjuty07n9kzp', 'master').create(entry_id, {
        'content_type_id': content_type,
        'fields': fields
    })
    # entry.publish()

def uploadResource(file, file_path, asset_id, title, resource_type):
    asset = client.assets('wjuty07n9kzp', 'master').create(asset_id, {
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


def scrape_content():
    WebDriverWait(driver, 15).until(lambda driver: driver.find_elements_by_xpath('//div[contains(@class, "LeftTwoThirdsPane")]'))
    soup = BeautifulSoup(driver.page_source.encode('utf-8'), 'html.parser')

    pdf_links = driver.find_elements_by_xpath('//div[contains(@class, "LeftTwoThirdsPane")]//a[contains(@href, ".pdf")]')
    pdfs = []
    for pdf_link_idx, pdf_link in enumerate(pdf_links):
        new_pdf = {}
        new_pdf['file_name'] = pdf_link.get_attribute('href').split('/')[-1]
        new_pdf['title'] = pdf_link.text
        new_pdf['id'] = binascii.b2a_hex(os.urandom(11))
        uploadResource(new_pdf['file_name'], pdf_link.get_attribute('href'), new_pdf['id'], new_pdf['title'], 'application/pdf')




site_login()
driver.get(URL)
scrape_content()
