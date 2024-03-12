from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from datetime import datetime

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'

option = Options()
option.add_argument("disable-infobars")
option.add_argument("disable-extensions")
option.add_argument('disable-gpu')
option.add_argument('headless')
option.add_argument('--no-sandbox')

s = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=s, options=option)


ppomppu_url = "https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu&page="
site = "ppomppu"

# [site, id, date, img_src, title, href, comment, category, good, bad, viewer, expire]
lists = []
now = datetime.now()

def goodbad(score):
    if len(score) == 3:
        if score[0] == '':
            good = 0
        else:
            good = score[0].strip()
        bad = score[2].strip()
    else:
        if score[0] == '':
            good = 0
        else:
            good = score[0].strip()
        bad = 0
    return good, bad

for index in range(5):
        driver.get(ppomppu_url+str(index+1))

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        revolution_main_table = soup.find('table',id = 'revolution_main_table')
        time.sleep(5)

        common_lists0 = revolution_main_table.find_all('tr','common-list0')
        common_lists1 = revolution_main_table.find_all('tr','common-list1')


        try:
                for i in common_lists0:
                        img_src = 'https:'+i.find('img', 'thumb_border')['src']
                        title = i.find('a', 'baseList-title').text
                        href = 'https://www.ppomppu.co.kr/zboard/'+i.find('a', 'baseList-title')['href']
                        eng_listVspace = i.find_all('td', 'eng list_vspace')
                        id = eng_listVspace[0].text.strip()
                        date = '20'+eng_listVspace[1]['title'].replace('.', '-')
						date_diff = now - datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

						if date_diff > 7:
							continue

                        score = eng_listVspace[2].text.split(' ')
                        good, bad = goodbad(score)
                        viewer = eng_listVspace[3].text.strip()

                        Is_expire = str(i).find('src="/zboard/skin/DQ_Revolution_BBS_New1/end_icon.PNG"')
                        expire = 0
                        if Is_expire.days > 7:
                                expire = 0 # expired
                        else:
                                expire = 1 # available

                        Is_comment = str(i).find('<span class="list_comment2">')
                        comment = 0
                        if Is_comment < 0:
                                comment = 0
                        else:
                                comment = i.find('span', 'list_comment2').text.strip()

                        category = i.find('span', attrs={'style':'color:#999;font-size:11px;'}).text

                        # [site, id, date, img_src, title, href, comment, category, good, bad, viewer, expire]
                        temp = [site, id, date, img_src, title, href, comment, category, good, bad, viewer, expire]
                        lists.append(temp)
        except AttributeError as e:
                pass

        try:
                for i in common_lists1:
                        img_src = 'https:'+i.find('img', 'thumb_border')['src']
                        title = i.find('a', 'baseList-title').text
                        href = 'https://www.ppomppu.co.kr/zboard/'+i.find('a', 'baseList-title')['href']
                        eng_listVspace = i.find_all('td', 'eng list_vspace')
                        id = eng_listVspace[0].text.strip()
                        date = '20'+eng_listVspace[1]['title'].replace('.', '-')
						date_diff = now - datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

						if date_diff.days > 7:
							continue
						
                        score = eng_listVspace[2].text.split(' ')
                        good, bad = goodbad(score)
                        viewer = eng_listVspace[3].text.strip()

                        Is_expire = str(i).find('src="/zboard/skin/DQ_Revolution_BBS_New1/end_icon.PNG"')
                        expire = 0
                        if Is_expire < 0:
                                expire = 0 # expired
                        else:
                                expire = 1 # available

                        Is_comment = str(i).find('<span class="list_comment2">')
                        comment = 0
                        if Is_comment < 0:
                                comment = 0
                        else:
                                comment = i.find('span', 'list_comment2').text.strip()

                        category = i.find('span', attrs={'style':'color:#999;font-size:11px;'}).text

                        # [site, id, date, img_src, title, href, comment, category, good, bad, viewer, expire]
                        temp = [site, id, date, img_src, title, href, comment, category, good, bad, viewer, expire]
                        lists.append(temp)
        except AttributeError as e:
                pass
driver.quit()
ppomppu_lists = sorted(lists, key = lambda x: [x[1]])