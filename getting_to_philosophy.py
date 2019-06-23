import requests
from bs4 import BeautifulSoup
import re
import time


def test_getting_to_philosophy(url):
    max_hops = 50
    count = 0
    href = re.compile('^/wiki/')  # red links start with '/w/'
    try:
        while count < max_hops:
            if url is None:
                break

            response = requests.get(url)
            content = BeautifulSoup(response.content,'html.parser')
            title = content.find(id="firstHeading").text

            #print('Hop Count: ',count)
            print('URL Visited: ',response.url)
            #print('Title: ',title)
            #print('----------------------------------')

            if title == "Philosophy":
                break
            url = None
            main_body = content.find("div", {"id": "mw-content-text"})

            for a in main_body.select("p > a"):
                if href.match(a['href']):
                    outer_brackets = re.compile('\\([^\\(\\)]*(\\([^\\(\\)]+\\))*[^\\(\\)]*' + str(a) + '[^\\(\\)]*(\\([^\\(\\)]+\\))*[^\\(\\)]*\\)')
                    inner_brackets = re.compile('\\(\s*' + str(a.text) + '\s*\\)')

                    if outer_brackets.search(str(a.parent)) is None and inner_brackets.search(str(a)) is None:
                        url = 'http://en.wikipedia.org' + a.get('href')
                        break

            count += 1
            time.sleep(0.5)

    except requests.exceptions.RequestException as e:
        print('An error has occurred when trying ',url)
        print(e)


#url = "http://en.wikipedia.org/wiki/Special:Random"
url = input()
test_getting_to_philosophy(url)
