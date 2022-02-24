import json
import requests
from lxml import etree
import urllib
with open('words.txt', 'r', encoding='utf-8') as f:
    words = json.loads(f.read())
d = []
for i in words:
    req = requests.get(
        'https://hanyu.baidu.com/zici/s?wd=' + urllib.parse.quote(i))
    if req.status_code != 200:
        continue
    html = etree.HTML(req.text)
    t = html.xpath('/html/body/div[3]/div/div[3]/div[2]/div[2]/div[1]/dl/dd/p/text()')
    if not len(t):
        continue
    d.append({
        "word": i,
        "explanation": t[0].strip()
    })
with open('words.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(d, ensure_ascii=False))
