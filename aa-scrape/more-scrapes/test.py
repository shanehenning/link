from bs4 import BeautifulSoup
import requests

URL = 'https://www.secondstep.org/what-is-second-step'

page_response = requests.get(URL, timeout=5)

page_content = BeautifulSoup(page_response.content, 'html.parser')

print(page_content.find('h1'))
print(page_content.find_all('h1'))
