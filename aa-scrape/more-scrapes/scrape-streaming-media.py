from openpyxl import load_workbook
from bs4 import BeautifulSoup
import tomd
import requests
from lxml import html, etree

USERNAME = 'mfahmy@cfchildren.org'
PASSWORD = 'forthechildren'
LOGIN_URL = 'https://login.secondstep.org/account/login'

def main():
    counter = 1

    #authentication
    session_requests = requests.session()

    navigation_to_login = session_requests.get(LOGIN_URL)
    tree_login_url = html.fromstring(navigation_to_login.text)
    authentication_token = list(set(tree_login_url.xpath("//input[@name='__RequestVerificationToken']/@value")))[0]

    creds = {
        'Email': USERNAME,
        'Password': PASSWORD,
        '__RequestVerificationToken': authentication_token
    }

    login = session_requests.post(LOGIN_URL, data = creds, headers = dict(referer=LOGIN_URL))
    #end authentication

    #page scrape
    while counter < 2:
        PAGE = 'http://www.secondstep.org/Streaming-Media/Second-Step/grade-4/Lesson-' + str(counter)
        result_page = session_requests.get(PAGE, headers = dict(referer = PAGE))
        tree_page = html.fromstring(result_page.content)
        contentPane = tree_page.xpath("//div[@id='dnn_ContentPane']")
        contentPaneString = etree.tostring(contentPane[0], method='html', with_tail=False)
        soup = BeautifulSoup(contentPaneString, 'html.parser')

        print('soup: ', soup)
        

        counter += 1
        #end page scrape

main()
