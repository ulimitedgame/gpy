from readmdict import MDX, MDD  # pip install readmdict
from pyquery import PyQuery as pq    # pip install pyquery

'''
# 如果是windows环境，运行提示安装python-lzo，但
> pip install python-lzo
报错“please set LZO_DIR to where the lzo source lives” ，则直接从 https://www.lfd.uci.edu/~gohlke/pythonlibs/#_python-lzo 下载 "python_lzo‑1.12‑你的python版本.whl" 
> pip install xxx.whl 
装上就行了，免去编译的麻烦

简单说一下mdx的构成，里面的每个单词其实都是一个单独的html文件。
按照特定格式转换添加索引变成一个压缩包，就变成了mdx字典文件

这里不需要了解如何解包，直接安装readmict模块就可以实现对mdx的加载得到每个单词的html文件。
至于从html里提取词义，和爬虫从网页中提取内容一样，了解一下BeautifulSoup、pyquery之类就可以了，
我这里用的是pyquery。
'''

# 加载mdx文件
filename = "TLD.mdx"
headwords = [*MDX(filename)]       # 单词名列表
items = [*MDX(filename).items()]   # 释义html源码列表
if len(headwords)==len(items):
    print(f'加载成功：共{len(headwords)}条')
else:
    print(f'【ERROR】加载失败{len(headwords)}，{len(items)}')

# 查词，返回单词和html文件
queryWord = 'Walkman'
wordIndex = headwords.index(queryWord.encode())
word,html = items[wordIndex]
word,html = word.decode(), html.decode()
#print(word, html)

# 从html中提取需要的部分，这里以the litte dict字典为例。到这一步需要根据自己查询的字典html格式，自行调整了。
doc = pq(html)
coca2 = doc('div[class="coca2"]').text().replace('\n','')
meaning = doc("""div[class="dcb"]""").text()
print(coca2)
print(meaning)
