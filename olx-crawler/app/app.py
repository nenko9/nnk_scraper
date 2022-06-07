from http.cookiejar import Cookie
from bs4 import BeautifulSoup
import requests

class Advertisment:
    def __init__(self, url, title, price,location):
        self.url=url
        self.title=title
        self.price=price
        self.location=location

def GetRequest():
    host='https://www.olx.ua'
    query=input('[?] Type what to find: ')
    print('[+] Your request: {}'.format(query))
    URL="{}/d/list/q-{}".format(host,query)
    print('[+] Your URL: {}'.format(URL))
    return URL

def ParsePage(url):
    # olx return max 25 pages with advertisement
    max_page=1
    # get advertisments page count
    page = requests.get(url, timeout=20)
    page_text = page.text
    soup = BeautifulSoup(page_text, 'html.parser')
    pages_html=soup.find_all('a', class_='css-1mi714g')
    for _ in pages_html:
        if int(_.get_text())==25:
          max_page=25
        else:
            for _n in pages_html:
                if int(_n.get_text()) > int(max_page):
                    max_page=_n.get_text()
    for page_number in range(int(max_page)):
        URL=url+'/?page={}'.format(page_number)
        page=requests.get(URL, timeout=20)
        page_content = page.text
        soup = BeautifulSoup(page_content, 'html.parser')
        # get all <div>-s with adwertisment
        ll=soup.find_all('div', class_='css-19ucd76')
    return ll

def GetAdvertisement(url):
    advertisments=list()
    div_list = ParsePage(url)
    for el in div_list:
        try:
            title=el.find('h6', class_='css-v3vynn-Text eu5v0x0').text
            url=el.find('a', class_='css-1bbgabe').get('href')
            price = el.find('p', class_='css-l0108r-Text eu5v0x0').text
            location= el.find('p', class_='css-p6wsjo-Text eu5v0x0').text
            adv = Advertisment(url,title,price,location)
            advertisments.append(adv)
        except:
            pass
    return advertisments


def main():
    a = GetAdvertisement(GetRequest())
    for el in a:
        print(el.title,' ', el.price)
if __name__=='__main__':
    main()