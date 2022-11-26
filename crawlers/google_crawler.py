import csv
import time
import json
import os
import requests
from lxml import etree
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pymysql
from urllib import parse, request
# from pyvirtualdisplay import Display
import sys
import random
import redis
import codecs
import math
# sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
print (sys.stdout.encoding)

from utils import *

API_KEY = ''
# site_key = ''  # site-key, read the 2captcha docs on how to get this
count = -1

def handle_captcha(url, site_key):
    s = requests.Session()

    # here we post site key to 2captcha to get captcha ID (and we parse it here too)
    captcha_id = s.post(
        "http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}".format(API_KEY, site_key, url),
        ).text
    print(captcha_id)
    captcha_id = captcha_id.split('|')[1]
    # then we parse gresponse from 2captcha response
    recaptcha_answer = s.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(API_KEY, captcha_id)).text
    print("solving ref captcha...")
    wait_time = 0
    while ('CAPCHA_NOT_READY' in recaptcha_answer) and (wait_time < 90):
        time.sleep(2)
        wait_time += 5
        recaptcha_answer = s.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(API_KEY, captcha_id)).text

    if 'CAPCHA_NOT_READY' in recaptcha_answer:
        return None
    else:
        recaptcha_answer = recaptcha_answer.split('|')[1]
        return recaptcha_answer
    # we make the payload for the post data here, use something like mitmproxy or fiddler to see what is needed


def get_author_profile(url):
    # print(url)
    try:
        driver.get(url)
        try_times = 0
        sleep_time = random.randint(10, 30)
        time.sleep(sleep_time)
        while (try_times < 5) and driver.page_source.find("无人机") == -1 and (driver.page_source.find("人机") != -1 or driver.page_source.find("not a robot") != -1):
            # Add these values
            try_times += 1
            try:
                site_key = driver.find_element_by_id("recaptcha").get_attribute('data-sitekey')
            except:
                site_key = '6LfFDwUTAAAAAIyC8IeC3aGLqVpvrB6ZpkfmAibj'
            ans = handle_captcha(url, site_key)
            try:
                form_id = driver.find_element_by_xpath(".//body/div/form").get_attribute('id')
            except:
                form_id = 'gs_captcha_f'
            print (form_id)
            if ans:
                command = "document.getElementById('g-recaptcha-response').innerHTML='" + ans + "';"
                driver.execute_script(command)
                driver.execute_script('document.getElementById("' + form_id + '").submit()')
                print("2captcha succeed!")

        if (driver.page_source.find("无人机") == -1) and (driver.page_source.find("人机") != -1 or driver.page_source.find("not a robot") != -1):
            return False, None
        else:
            return True, None
    except Exception as e:
        # print (url)
        if ("Cannot navigate to invalid URL" in e.__dict__['msg']):
            return True, url
        else:
            return False, url

def get_citations(driver):
    citation_tags = driver.find_elements_by_xpath(".//div[@id='gsc_art']//div[@id='gsc_a_tw']/table[@id='gsc_a_t']/tbody[@id='gsc_a_b']/tr[@class='gsc_a_tr']/td[@class='gsc_a_c']/a")
    paper_citations_search = []
    citation_number = []
    for citation_tag in citation_tags:
        try:
            citation_number.append(int(citation_tag.text))
        except:
            citation_number.append(0)
        # print (citation_number)
        paper_citations_search.append(citation_tag.get_attribute('href'))
    return paper_citations_search, citation_number

def get_author_list(author_count):
    author_url_tags = driver.find_elements_by_xpath(
        ".//div[@id='gs_res_ccl']/div[@id='gs_res_ccl_mid']/div[@class='gs_r gs_or gs_scl']/div[@class='gs_ri']/div[@class='gs_a']/a")
    paper_tags = driver.find_elements_by_xpath(".//div[@class='gs_r gs_or gs_scl']")
    if len(paper_tags) == 0:
        is_empty = True
    else:
        is_empty = False
    for author_url_tag in author_url_tags:
        # print (author_url_tag.text)
        href = author_url_tag.get_attribute('href')
        # print (href)
        if href not in author_count:
            author_count[href] = 0
        author_count[href] += 1
    # print(author_count)
    return author_count, is_empty

def write_file(file_name, contents):
    with open('./author_list/' + file_name + '.json', 'w') as fp:
        fp.write(json.dumps(contents))
    fp.close()

def search_citations(paper_citation_search, citation_number, uid):
    author_count = {}
    paper_num = len(paper_citation_search)
    error_flag = False
    for idx in range(paper_num):
        search_url = paper_citation_search[idx]
        citation = citation_number[idx]
        pages = math.ceil(float(citation) / 10)
        res, url_wrong = get_author_profile(search_url)

        if url_wrong is not None: continue
        if res:
            author_count, is_empty = get_author_list(author_count)
            if is_empty:
                continue
            write_file(uid, author_count)
            url_first_page = driver.current_url.split('?')
            js = "var q=document.documentElement.scrollTop=100000"
            driver.execute_script(js)
            for page in range(2, pages+1):
                url_next_page = url_first_page[0] + '?start=' + str(page * 10 - 10) + '&' + url_first_page[1]
                res, url_wrong = get_author_profile(url_next_page)
                if url_wrong is not None: continue
                if res:
                    author_count, is_empty = get_author_list(author_count)
                    if is_empty:
                        break
                    write_file(uid, author_count)
                else:
                    print ('Error!')
                    error_flag = True
                    break
                time.sleep(1)
                js = "var q=document.documentElement.scrollTop=10000"
                driver.execute_script(js)
        else:
            print ('Error!')
            error_flag = True
        if error_flag:
            break
    if error_flag:
        return None
    else:
        return author_count

if __name__ == '__main__':
    driver = initial()
    r = redis.Redis(host='184.170.214.178', port=6379, db=0)

    # with open('author_list.json', 'r') as fp:
    #     # authors_dirs = ['https://scholar.google.com.hk/citations?user=HmyM5B8AAAAJ&hl=zh-CN&oi=sra']
    #     authors_dirs = json.loads(fp.read())
    # fp.close()
    # example_list = ['4OvOdSgAAAAJ', '5JE9m1EAAAAJ', 'ak35bjgAAAAJ', 'CZyWk8kAAAAJ', 'dcDrhzMAAAAJ',
    #                 'dsPXcxsAAAAJ', 'Dzh5C9EAAAAJ', 'Ec222JgAAAAJ', 'G2EJz5kAAAAJ', 'GXJqtYUAAAAJ',
    #                 'hNfaJTMAAAAJ', 'I1EvjZsAAAAJ', 'nxF4XdQAAAAJ', 'PkfChMgAAAAJ', 'V05Jz1oAAAAJ',
    #                 'wuGjSFsAAAAJ']
    #
    # failed_list = []
    # for author_dir in authors_dirs:
    # with open('author_idx.txt', 'r') as fp:
    #     idx = int(fp.read()) - 1
    # fp.close()
    # idx = 0
    # while idx < len(authors_dirs):
    #     author_dir = authors_dirs[idx]
    #     idx += 1
    url = r.lpop("author_url_list_backup")
    print (url)
    while url is not None:
        # with open('author_idx.txt', 'w') as fp:
        #     fp.write(str(idx-1))
        # fp.close()
        # url = author_dir
        print (url)
        url = bytes.decode(url)
        # url = str(url)
        uid = url.split('user=')[1].split('&')[0]
        print (url, uid)
        if uid + '.json' in os.listdir('./author_list'):
            url = r.lpop("author_url_list_backup")
            continue
        # if uid in example_list: continue
        # if uid + '.json' in os.listdir('./author_list'): continue
        res, url_wrong = get_author_profile(url)
        if res:
            xpath = ".//div[@id='gsc_bdy']/div[@id='gsc_art']/form/div[@id='gsc_lwp']/div[@id='gsc_bpf']/button"
            unfold_tag = driver.find_elements_by_xpath(xpath)[0]
            flag = True
            try_time = 0
            last_tag = '文章 1–20'
            while (unfold_tag.is_enabled()):
                driver.find_elements_by_xpath(xpath)[0].click()
                time.sleep(5)
                tag = driver.find_elements_by_xpath(".//span[@id='gsc_a_nn']")[0].text
                if tag == last_tag:
                    last_tag = '文章 1–20'
                    res1 = get_author_profile(url)
                    if not res1:
                        flag = False
                        break
                last_tag = tag
                unfold_tag = driver.find_elements_by_xpath(xpath)[0]

            if not flag:
                print(url, 'Error!')
                r.rpush('author_url_list_backup', url)
                url = r.lpop("author_url_list_backup")
                continue

            paper_citation_search, citation_number = get_citations(driver)
            author_count = search_citations(paper_citation_search, citation_number, uid)
            if author_count:
                print (author_count)
                print (list(author_count.keys())[0])
                for new_author_url in list(author_count.keys()):
                    # if new_author_url not in authors_dirs:
                    #     authors_dirs.append(new_author_url)
                    new_uid = url.split('user=')[1].split('&')[0]
                    redis_res = r.sadd('uid_set_backup', new_uid)
                    if redis_res == 1:
                        r.rpush('author_url_list_backup', bytes.decode(new_author_url))
                print ("Push successfully!")
            else:
                if  uid + '.json' in os.listdir('./author_list'):
                    os.remove('./author_list/' + uid + '.json')
                print (url, 'Error!')
                r.rpush('author_url_list_backup', url)
            # with open('author_list.json', 'w') as fp:
            #     fp.write(json.dumps(authors_dirs))
            # fp.close()
            # with open('author_idx.txt', 'w') as fp:
            #     fp.write(str(idx))
            # fp.close()
        else:
            if  uid + '.json' in os.listdir('./author_list'):
                os.remove('./author_list/' + uid + '.json')
            print(url, 'Error!')
            r.rpush('author_url_list_backup', url)
        url = r.lpop("author_url_list_backup")


