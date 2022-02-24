# cntbot-idi

[cntbot](https://github.com/YouXam/cntbot) 的猜成语后端，修改自 [汉兜](https://handle.antfu.me/)。

## 依赖

需要安装 webdriver 和 chrome。

```sh
pip install flask selenium lxml requests
```

## 修改词库

在 words.txt 中添加成语，然后运行 `python gene.py` 爬取成语释义（数据来源：百度汉语）。

## 运行

```sh
python app.py
```
