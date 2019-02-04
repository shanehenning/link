# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import collections, json, re, time
from lxml import etree


driver = webdriver.Firefox()

BASE_URL = 'http://www.secondstep.org/Streaming-Media/Second-Step/'
LOGIN_URL = 'http://login.secondstep.org/account/login'
USERNAME = 'mfahmy@cfchildren.org'
PASSWORD = 'forthechildren'

pages = []


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
            time.sleep(.55)
    if(lang == 'spanish'):
        if driver.find_element_by_class_name('spanishContent').value_of_css_property('display') == 'none':
            driver.find_element_by_xpath('//label[@for="spanish"]').click()
            currentLanguage = 'spanish'
            time.sleep(.55)


def checkForNextImage(selenium_driver, media_array):
    img = ''
    img = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "fancybox-opened")]//img[@class="fancybox-image"]'))
    )
    image_src = img.get_attribute('src')
    image_type = 'image/' + image_src.split('.')[-1]
    image_alt = img.get_attribute('alt')
    if img != '':
        media_title = selenium_driver.find_element_by_xpath('//div[contains(@class, "fancybox-opened")]//div[contains(@class, "fancybox-title")]').text
    else:
        media_title = ''
    media_array.append({'type': image_type, 'image-src': image_src, 'media-title': media_title, 'image-alt': image_alt})
    try:
        if check_exists_by_xpath(driver, '//a[contains(@class, "fancybox-next")]') == True:
            driver.find_element_by_xpath('//a[contains(@class, "fancybox-next")]').click()
            checkForNextImage(selenium_driver, media_array)
    except:
        return media_array


def check_exists_by_xpath(entry, xpath):
    try:
        entry.find_element_by_xpath(xpath)
        return True
    except:
        return False


def openModals(bs, page):
    content_containers = []
    languageToggle = driver.find_elements_by_xpath('//div[@class="langToggle"]//label')
    if len(languageToggle) > 0:
        multilingual = True
    else:
        multilingual = False
    if multilingual == True:
        english = bs.find_all('div', attrs={'class': 'englishContent'})
        # the last div is the one with the page content we want
        english = english[-1]
        content_containers.append({'language': 'english', 'soup': english, 'xpath': '//div[contains(@class, "DNNModuleContent")]//div[contains(@class, "englishContent")]'})
        spanish = bs.find_all('div', attrs={'class': 'spanishContent'})
        spanish = spanish[-1]
        content_containers.append({'language': 'spanish', 'soup': spanish, 'xpath': '//div[contains(@class, "DNNModuleContent")]//div[contains(@class, "spanishContent")]'})
    else:
        currentLanguage = 'english'
        content_containers.append({'language': 'english', 'soup': bs.find('div', attrs={'id': 'dnn_ContentPane'}), 'xpath': '//div[@id="dnn_ContentPane"]'})
    lesson_materials_all = [{}] * len(content_containers)
    buttons_modals = []
    modal_counter = 0
    for container_idx, container in enumerate(content_containers):
        if multilingual == True:
            checkLanguageToggle(container['language'])
        lesson_materials_all[container_idx] = {'language': container['language'], 'content' : container['soup'].find_all('div', attrs={'class': 'lesson-materials'})}
        all_buttons = []
        all_buttons_initial = driver.find_elements_by_xpath(container['xpath'] + '//div[contains(@class, "button-container")]/a')
        for button_initial_idx, button_initial in enumerate(all_buttons_initial):
            if check_exists_by_xpath(button_initial, './/img'):
                all_buttons.append(button_initial)
        for all_buttons_idx, button in enumerate(all_buttons):
            buttons_modals.append({})
            medias = []
            multiple_media = False
            button.click()
            try: # look for image
                img = WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "fancybox-opened")]//img[@class="fancybox-image"]'))
                )
                image_src = img.get_attribute('src')
                image_type = 'image/' + image_src.split('.')[-1]
                image_alt = img.get_attribute('alt')
                if check_exists_by_xpath(driver, '//a[contains(@class, "fancybox-next")]') == True:
                    checkForNextImage(driver, medias)
                    multiple_media = True
                else:
                    media = {'type': image_type, 'image-src': image_src, 'media-title': img.text, 'image-alt': image_alt}

            except: # look instead for video
                if multiple_media == True:
                    pass
                else:
                    element = WebDriverWait(driver,5).until(
                        EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "fancybox-opened")]//div[@class="vjs-poster"]'))
                    )
                    if len(element.get_attribute('style').split('media/')) > 1:
                        media_id = element.get_attribute('style').split('media/')[1].split('/')[0]
                        media_poster = element.get_attribute('style').split('url("')[1].split('");')[0]
                        poster_type = 'image/' + media_poster.split('.')[-1]
                        media = {
                            'type': 'video',
                            'limelight-id': media_id,
                            'limelight-poster': media_poster,
                            'poster-type': poster_type
                        }
                    else:
                        media = ' '
            if multiple_media == True:
                buttons_modals[modal_counter] = medias
            else:
                buttons_modals[modal_counter] = media
            modal_counter += 1

            # below actions click a little bit off of the button (to close the modal) because another element obscures and prevents a click
            close_modal_button = driver.find_element_by_xpath('//div[@class="fancybox-overlay fancybox-overlay-fixed"]')
            action = webdriver.common.action_chains.ActionChains(driver)
            action.move_to_element_with_offset(close_modal_button, 10, 10)
            action.click()
            action.perform()
            # wait for modal to close before next index
            time.sleep(.55)

    data = []
    counter = 0
    for materials_idx, materials in enumerate(lesson_materials_all):
        # data[materials['language']] = {}
        items = {}
        items['categories'] = [{}] * len(materials['content'])
        # items['categories'] = {}
        for item_idx, item in enumerate(materials['content']):
            buttons = []
            heading = item.find('p', attrs={'class': 'gray-header'}).text.strip()
            fancybox_buttons = item.find_all('a', attrs={'class': 'dm-bt'})
            for fancybox_idx, fancybox in enumerate(fancybox_buttons):
                if fancybox.find('img') is None:
                    pass
                else:
                    buttons.append(fancybox)

            new_material = []

            for button_idx, button in enumerate(buttons):
                button_title = button.find('p', attrs={'class': 'bt-small'})
                if hasattr(button_title, 'text'):
                    button_title = button_title.text.strip()
                    thumbnail_img = button.find('img')['src']
                    thumbnail_alt = button.find('img')['alt']
                    thumbnail_type = 'image/' + thumbnail_img.split('.')[-1]
                else:
                    button_title = button['title']
                    thumbnail_img = ' '
                    thumbnail_alt = ' '
                button_title = re.sub(' +', ' ', button_title.replace('\n', ' '))
                new_button = {
                    'media-resource-title': button_title,
                    'thumbnail-image-src': thumbnail_img,
                    'thumbnail-image-alt': thumbnail_alt,
                    'thumbnail-type': thumbnail_type,
                    'modal-media': buttons_modals[counter]
                }
                new_material.append(new_button)
                counter += 1
            items['categories'][item_idx] = { 'category-title': heading, 'media-resource': new_material }
        # data[materials['language']] = items
        data.append({'language': materials['language'], 'items': items})
    pages.append({'page': page, 'content': data})

    # [materials['language']]

def scrape_content(name_of_page):
    soup = BeautifulSoup(driver.page_source.encode('utf-8'), 'html.parser')
    openModals(soup, name_of_page)


def navigate(max_page_number, address):
    page_number = 6
    while page_number < max_page_number:
        driver.get(address + str(page_number))
        # dynamically create name based upon url, for ex: grade-4-lesson-1
        path = driver.current_url
        href = path.split('/')
        page_name = (href[len(href) - 2] + ' ' + href[len(href) - 1])
        page_name = page_name.replace('-', ' ')
        scrape_content(page_name)
        page_number += 1


site_login()
grade_count = 4
while grade_count < 5:
    if grade_count == 1:
        URL = BASE_URL + 'Early-Learning/Weekly-Theme-'
        page_count_max = 7
    if grade_count == 2:
        URL = BASE_URL + 'Kindergarten/Lesson-'
        page_count_max = 7
    if grade_count > 2:
        grade = 'Grade-' + str(grade_count - 2)
        URL = BASE_URL + grade + '/Lesson-'
        page_count_max = 7
    navigate(page_count_max, URL)
    grade_count += 1

with open('streaming-media.json', 'w') as f:
    f.write(json.dumps(pages, ensure_ascii=False).encode('utf8'))
driver.quit()
