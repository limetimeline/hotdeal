from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import random
import requests

ppomppu_url = "https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu"
site = "ppomppu"
# driver = webdriver.Chrome()
# driver.get(ppomppu_url)

html = driver.find_element(By.ID,'revolution_main_table')
common_lists0 = html.find_elements(By.CLASS_NAME, 'common-list0')
common_lists1 = html.find_elements(By.CLASS_NAME, 'common-list1')

# [id, date, nickname, img_src, title, href, comment, category, good, bad, viewer, expire]
lists = []

# 
def goodbad(score):
    if len(score) == 3:
        if score[0] == '':
            good = 0
        else:
            good = score[0]
        bad = score[2]
    else:
        if score[0] == '':
            good = 0
        else:
            good = score[0]
        bad = 0
    return good, bad

for i in common_lists1:
    id = i.find_element(By.CLASS_NAME, 'eng.list_vspace').text
    nickname = i.find_element(By.CLASS_NAME, 'baseList-name').text
    img_src = i.find_element(By.TAG_NAME, 'img').get_attribute('src')
    title = i.find_element(By.CLASS_NAME, 'baseList-title').text
    href = i.find_element(By.CLASS_NAME, 'baseList-title').get_attribute('href')
    date = i.find_element(By.XPATH, 'td[4]').get_attribute('title')
    viewer = i.find_element(By.XPATH, 'td[6]').text

    score = i.find_element(By.XPATH, 'td[5]').text.split(' ')
    good, bad = goodbad(score)

    try:
        comment = i.find_element(By.CLASS_NAME, 'list_comment2').text
        category = i.find_element(By.XPATH, 'td[3]/table/tbody/tr/td[2]/div/span[2]').text
    except NoSuchElementException:
        # print("Element does not exist")
        comment = 0
        category = i.find_element(By.XPATH, 'td[3]/table/tbody/tr/td[2]/div/span').text
    
    try:
        print(i.find_element(By.XPATH, 'td[3]/table/tbody/tr/td[2]/div/img'))
        expire = 1
    except NoSuchElementException:
        # print("Element does not exist")
        expire = 0

    a = [id, site, date, nickname, img_src, title, href, comment, category, good, bad, viewer, expire]
    lists.append(a)

for i in common_lists0:
    id = i.find_element(By.CLASS_NAME, 'eng.list_vspace').text
    nickname = i.find_element(By.CLASS_NAME, 'baseList-name').text
    img_src = i.find_element(By.TAG_NAME, 'img').get_attribute('src')
    title = i.find_element(By.CLASS_NAME, 'baseList-title').text
    href = i.find_element(By.CLASS_NAME, 'baseList-title').get_attribute('href')
    date = i.find_element(By.XPATH, 'td[4]').get_attribute('title')
    viewer = i.find_element(By.XPATH, 'td[6]').text

    score = i.find_element(By.XPATH, 'td[5]').text.split(' ')
    good, bad = goodbad(score)

    try:
        comment = i.find_element(By.CLASS_NAME, 'list_comment2').text
        category = i.find_element(By.XPATH, 'td[3]/table/tbody/tr/td[2]/div/span[2]').text
    except NoSuchElementException:
        # print("Element does not exist")
        comment = 0
        category = i.find_element(By.XPATH, 'td[3]/table/tbody/tr/td[2]/div/span').text
    
    try:
        print(i.find_element(By.XPATH, 'td[3]/table/tbody/tr/td[2]/div/img'))
        expire = 1
    except NoSuchElementException:
        # print("Element does not exist")
        expire = 0

    a = [id, site, date, nickname, img_src, title, href, comment, category, good, bad, viewer, expire]
    lists.append(a)
    
sorted_list = sorted(lists, key = lambda x: [x[0]])
print(sorted_list)