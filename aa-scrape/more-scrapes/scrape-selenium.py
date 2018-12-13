from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

driver = webdriver.Firefox()

URL = 'http://www.secondstep.org/Streaming-Media/Second-Step/grade-4/Lesson-2'
USERNAME = 'mfahmy@cfchildren.org'
PASSWORD = 'forthechildren'

soups = {}

def site_login():
    driver.get(URL)
    driver.find_element_by_id('Email').send_keys(USERNAME)
    driver.find_element_by_id('Password').send_keys(PASSWORD)
    driver.find_element_by_class_name('login-bt').click()

def get_soups():
    page = driver.current_url
    href = page.split('/')
    name = (href[len(href) - 2] + '-' + href[len(href) - 1]).lower()
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    contentPane = soup.find('div', attrs={'id': 'dnn_ContentPane'})
    lesson_materials_all = contentPane.find_all('div', attrs={'class': 'lesson-materials'})
    all_buttons = driver.find_elements_by_xpath('//div[@class="button-container width-auto"]/a')
    buttons_modals = ['a'] * len(all_buttons)
    for all_buttons_idx, button in enumerate(all_buttons):
        button.click()
        print('all_buttons_idx: ', all_buttons_idx)
        media = ''
        try:
            img = WebDriverWait(driver, 0.75).until(
                EC.presence_of_element_located((By.XPATH, '//img[@class="fancybox-image"]'))
            )
            # print('img: ', img)
            media = 'https://www.secondstep.org' + img.get_attribute('src')
            print('media: ', media)
        except:
            element = WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="vjs-poster"]'))
            )
            # print('element: ', element)
            media = element.get_attribute('style').split('media/')[1].split('/')[0]
            print('media: ', media)
        buttons_modals[all_buttons_idx] = media
        close = driver.find_element_by_xpath('//div[@class="fancybox-overlay fancybox-overlay-fixed"]')
        action = webdriver.common.action_chains.ActionChains(driver)
        action.move_to_element_with_offset(close, 10, 10)
        action.click()
        action.perform()
        time.sleep(0.75)
    data = []
    counter = 0
    print('buttons_modals: ', buttons_modals)
    for material_idx, material in enumerate(lesson_materials_all):
        heading = material.find('p', attrs={'class': 'gray-header'}).text.strip()
        buttons = material.find_all('div', attrs={'class': 'button-container'})
        lesson_materials_buttons = []
        for button_idx, button in enumerate(buttons):
            button_title = button.find('p', attrs={'class': 'bt-small'}).text.strip()
            button_preview = button.find('img')['src']
            new_button = {
                'index': button_idx,
                'button-title': button_title,
                'button-preview': button_preview,
                'button-modal': buttons_modals[counter]
            }
            lesson_materials_buttons.append(new_button)
        new_material = {
            'index': material_idx,
            'heading': heading,
            'buttons': lesson_materials_buttons
        }
        data.append(new_material)
        counter += 1
    # print('data: ', data)
    driver.quit()


site_login()
get_soups()
