import base64
import json
import os
import random
from flask import Flask, request
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
app = Flask(__name__, static_folder='static')


def get_new_word():
    f = open('words.json', 'r', encoding='utf-8')
    data = json.load(f)
    f.close()
    rr = random.choice(data)
    return rr['word'], rr['explanation']


driver = None
max_cnt = 100
cnt = max_cnt
word, exp = get_new_word()


@app.route('/', methods=['GET'])
def index():
    with open('index.html', 'r', encoding='utf-8') as f:
        data = f.read()
    return data


@app.route('/get', methods=['GET'])
def get():
    global cnt, driver, word, exp
    if cnt >= max_cnt:
        if driver is None:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument('--no-sandbox')
            driver = webdriver.Chrome(options=chrome_options)
        cnt = 0
        driver.get('http://127.0.0.1:6699/?word=' + word)
    arg = request.args.get("word")
    driver.find_element(by=By.ID, value="input").send_keys(arg)
    driver.find_element(by=By.ID, value="btn").click()
    cnt += 1
    issucceed = False
    try:
        countdown = driver.find_elements(
            by=By.XPATH, value='/html/body/div[1]/main/div[7]/div/div/div/div[1]/div[1]')
        for i in countdown:
            if i.text == '距离下一题更新还有':
                issucceed = True
    except selenium.common.exceptions.NoSuchElementException:
        pass
    words = driver.find_elements(
        by=By.XPATH, value='/html/body/div[1]/main/div[7]/div/div/div')
    lens = len(words)
    last = driver.find_element(
        by=By.XPATH, value='/html/body/div[1]/main/div[7]/div/div/div[' + str(lens - (3 if issucceed else 1)) + ']')
    last.screenshot(arg + '.png')
    with open(arg + '.png', 'rb') as f:
        data = f.read()
    os.remove(arg + '.png')
    bdata = base64.b64encode(data).decode()
    rdata = json.dumps({'code': 0, 'success': int(issucceed), 'pic': bdata, 'word': word, 'explanation': exp})
    if issucceed:
        cnt = 0
        word, exp = get_new_word()
        driver.get('http://127.0.0.1:6699/?word=' + word)
    return rdata


app.run(host='0.0.0.0', port=6699)
