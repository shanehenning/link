# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import collections, json, re, time

driver = webdriver.Firefox()

URL = 'http://www.secondstep.org/Streaming-Media/Second-Step/grade-1/Lesson-'
LOGIN_URL = 'http://login.secondstep.org/account/login'
USERNAME = 'mfahmy@cfchildren.org'
PASSWORD = 'forthechildren'

pages = collections.OrderedDict()

# def replace_text(text):
#     return text.replace(u'\u00f3', 'ó')

def site_login():
    driver.get(LOGIN_URL)
    driver.find_element_by_id('Email').send_keys(USERNAME)
    driver.find_element_by_id('Password').send_keys(PASSWORD)
    driver.find_element_by_class_name('login-bt').click()

def checkLanguageToggle(lang):
    if lang == 'english':
        if driver.find_element_by_class_name('englishContent').value_of_css_property('display') == 'none':
            driver.find_element_by_xpath('//label[@for="english"]').click()
            currentLanguage = 'english'
            # print('toggled to english')
            time.sleep(.55)
    if(lang == 'spanish'):
        if driver.find_element_by_class_name('spanishContent').value_of_css_property('display') == 'none':
            driver.find_element_by_xpath('//label[@for="spanish"]').click()
            currentLanguage = 'spanish'
            # print('toggled to spanish')
            time.sleep(.55)

def openModals(bs):
    content_containers = []
    currentLanguage = 'english'
    content_containers.append({'language': 'english', 'soup': bs.find('div', attrs={'id': 'dnn_ContentPane'}), 'xpath': '//div[@id="dnn_ContentPane"]'})
    languageToggle = driver.find_elements_by_xpath('//div[@class="langToggle"]//label')
    if languageToggle > 0:
        content_containers = []
        english = bs.find_all('div', attrs={'class': 'englishContent'})
        # the last div is the one with the content we care about
        english = english[-1]
        content_containers.append({'language': 'english', 'soup': english, 'xpath': '//div[contains(@class, "DNNModuleContent")]//div[contains(@class, "englishContent")]'})
        spanish = bs.find_all('div', attrs={'class': 'spanishContent'})
        spanish = spanish[-1]
        # print('spanish: ', spanish.decode('latin1'))
        content_containers.append({'language': 'spanish', 'soup': spanish, 'xpath': '//div[contains(@class, "DNNModuleContent")]//div[contains(@class, "spanishContent")]'})
    languages = [{'language': 'a'}] * len(content_containers)
    # all_buttons = []
    lesson_materials_all = ['a'] * len(content_containers)
    for container_idx, container in enumerate(content_containers):
        checkLanguageToggle(container['language'])
        languages[container_idx] = container['language']

        lesson_materials_all[container_idx] = {'language': container['language'], 'content' : container['soup'].find_all('div', attrs={'class': 'lesson-materials'})}

        all_buttons = {'buttons': driver.find_elements_by_xpath(container['xpath'] + '//div[contains(@class, "button-container")]/a'), 'language': container['language']}
        buttons_modals = [{}] * len(all_buttons['buttons'])
        for all_buttons_idx, button in enumerate(all_buttons['buttons']):
            # checkLanguageToggle(button['language'])
            button.click()
            try: # look for image
                img = WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "fancybox-opened")]//img[@class="fancybox-image"]'))
                )
                media = 'https://www.secondstep.org' + img.get_attribute('src')
            except: # look instead for video
                element = WebDriverWait(driver,5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "fancybox-opened")]//div[@class="vjs-poster"]'))
                )
                if len(element.get_attribute('style').split('media/')) > 1:
                    media = element.get_attribute('style').split('media/')[1].split('/')[0]
                else:
                    media = ' '
            buttons_modals[all_buttons_idx] = media
            # below actions click a little bit off of the button (to close the modal) because another element obscures and prevents a click
            close_modal_button = driver.find_element_by_xpath('//div[@class="fancybox-overlay fancybox-overlay-fixed"]')
            action = webdriver.common.action_chains.ActionChains(driver)
            action.move_to_element_with_offset(close_modal_button, 10, 10)
            action.click()
            action.perform()

            # wait for modal to close before next index
            time.sleep(.55)

    data = ['a'] * len(lesson_materials_all)
    for materials_idx, materials in enumerate(lesson_materials_all):
        counter = 0
        items = ['a'] * len(materials['content'])
        for item_idx, item in enumerate(materials['content']):
            heading = item.find('p', attrs={'class': 'gray-header'}).text.strip()
            buttons = item.find_all('a', attrs={'class': 'dm-bt'})
            lesson_materials_buttons = ['a'] * len(buttons)
            for button_idx, button in enumerate(buttons):
                button_title = button.find('p', attrs={'class': 'bt-small'})
                print('button_title: ', button_title)
                if hasattr(button_title, 'text'):
                    button_title = button_title.text.strip()
                    print('button_title: ', button_title)
                    thumbnail_img = button.find('img')['src']
                else:
                    button_title = button['title']
                    thumbnail_img = ' '
                button_title = re.sub(' +', ' ', button_title.replace('\n', ' '))
                new_button = {
                    'item-title': button_title,
                    'thumbnail-image-src': thumbnail_img,
                    'modal-media': buttons_modals[counter]
                }
                counter += 1
            new_material = {
                'heading': heading,
                'content': new_button
            }
            items[item_idx] = new_material
        data[materials_idx] = {materials['language'] : items}
        print('data: ', data)
    pages[name] = data

def scrape_content():
    soup = BeautifulSoup(driver.page_source.encode('utf-8'), 'html.parser')
    print('soup encode: ', soup.original_encoding)
    openModals(soup)




site_login()
# grade_count = 1
# while grade_count < 7:
#     if grade_count == 1:
#         URL = URL + 'Early-Learning/Weekly-Theme-'
#     if grade_count == 2:
#         URL = URL + 'Kindergarten/Lesson-'
#     if grade_count > 2:
#         grade = 'grade-' + str(grade_count - 2)
#         URL = URL + grade + '/Lesson-'
page_count = 2
while page_count < 3:
    driver.get(URL + str(page_count))
    # dynamically create name based upon url, for ex: grade-4-lesson-1
    address = driver.current_url
    href = address.split('/')
    name = (href[len(href) - 2] + '-' + href[len(href) - 1]).lower()
    scrape_content()
    page_count += 1
with open('streaming-media.json', 'w') as f:
    f.write(json.dumps(pages))
driver.quit()
