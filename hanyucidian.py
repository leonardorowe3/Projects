# -*- coding: utf-8 -*-
import requests #导入requests包
import os
from bs4 import BeautifulSoup #导入BeautifulSoup4
def mkdir(path): #创建文件夹的函数
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print
        "---  new folder...  ---"
        print
        "---  OK  ---"

    else:
        print
        "---  There is this folder!  ---"


url = "http://www.guoxuedashi.com/hydcd/" #目标网站的URL
mainpage = requests.get(url)
soup = BeautifulSoup(mainpage.content, "html.parser") #利用BeautifulSoup提取网站
titles = soup.find_all("dt") #获取第一个标题标签
contents = soup.select(".table2") #选择网站有文字的板块
letters = contents[0].find_all("td",{"width":"20"}) #拼音索引
bushous = contents[1].find_all("td",{"width":"20"}) #部首索引
print("按照拼音索引提取词语信息：\n")
for letter in letters:
    pinyins = letter.next_sibling #选择首字母的兄弟节点，即以该首字母开头的拼音
    #print(letter.text)
    for pinyin in pinyins:
        pylink = "http://www.guoxuedashi.com"+pinyin.get('href') #获取每个拼音的下一级链接
        pypage = requests.get(pylink)
        pysoup=BeautifulSoup(pypage.content, "html.parser") #利用BeautifulSoup提取二级页面（笔画）
        bihuas = pysoup.select(".info_txt2 strong") #获取下级页面的所有笔画
        for bihua in bihuas:
            words = bihua.find_next_siblings("a",{"target":"_blank"}) #找到笔画对应的文字
            for word in words:
                #print(letter.text+":"+pinyin.text+":"+bihua.text)
                filename = "/Users/LeonardoRowe/Desktop/" + titles[0].text + "/" + letter.text + "/" + pinyin.text + "/" + bihua.text + "/" + word.text
                mkdir(filename)#对于每一个文字，一层层建立对应文件夹
                wordlink = "http://www.guoxuedashi.com"+word.get('href')
                wordpage = requests.get(wordlink)
                wordsoup=BeautifulSoup(wordpage.content, "html.parser") #利用BeautifulSoup提取三级页面（文字）
                phrases = wordsoup.select(".info_txt2 a")

                for phrase in phrases:
                    phraselink = "http://www.guoxuedashi.com"+phrase.get('href')
                    phrasepage = requests.get(phraselink)
                    phrasesoup = BeautifulSoup(phrasepage.content, "html.parser") #利用BeautifulSoup提取四级页面（词语）
                    images = phrasesoup.select("h2 a") #选择词语文件夹中的超链接，连接到每个词的词典部分
                    f = open(filename + "/" + phrase.text + ".txt", "w") #在每个文字的文件夹下建立txt文件，对应以该文字开头的词语
                    lists = phrasesoup.select(".info_txt2") #选取词语界面的文字板块
                    [s.extract() for s in phrasesoup('div')] #去除文字板块中的无关信息部分
                    print("正在提取"+phrase.text+"的信息...")
                    for liste in lists:
                        f.write("定义："+liste.text+"\n") #将词语的定义分别写入到文件中
                    f.write("词典图片URL：\n")
                    for image in images:
                        imagelink="http://www.guoxuedashi.com"+image.get('href')
                        imagepage = requests.get(imagelink)
                        imagesoup = BeautifulSoup(imagepage.content, "html.parser")#利用BeautifulSoup提取五级页面（图片）
                        imgs = imagesoup.select("center img")
                        for img in imgs:
                            f.write(img.get('src')) #将每个词语的图片信息写入文件中

print("按照部首索引提取词语信息：\n")
for bushou in bushous: #按部首索引提取信息，原理和拼音索引部分一模一样
    pinyins = bushou.next_sibling
    #print(letter.text)
    for pinyin in pinyins:
        pylink = "http://www.guoxuedashi.com"+pinyin.get('href')
        pypage = requests.get(pylink)
        pysoup=BeautifulSoup(pypage.content, "html.parser")
        bihuas = pysoup.select(".info_txt2 strong")
        for bihua in bihuas:
            words = bihua.find_next_siblings("a",{"target":"_blank"})
            for word in words:
                #print(letter.text+":"+pinyin.text+":"+bihua.text)
                filename = "/Users/LeonardoRowe/Desktop/" + titles[1].text + "/" + bushou.text + "/" + pinyin.text + "/" + bihua.text + "/" + word.text
                mkdir(filename)
                wordlink = "http://www.guoxuedashi.com"+word.get('href')
                wordpage = requests.get(wordlink)
                wordsoup=BeautifulSoup(wordpage.content, "html.parser")
                phrases = wordsoup.select(".info_txt2 a")

                for phrase in phrases:
                    phraselink = "http://www.guoxuedashi.com"+phrase.get('href')
                    phrasepage = requests.get(phraselink)
                    phrasesoup = BeautifulSoup(phrasepage.content, "html.parser")
                    images = phrasesoup.select("h2 a")
                    f = open(filename + "/" + phrase.text + ".txt", "w")
                    lists = phrasesoup.select(".info_txt2")
                    [s.extract() for s in phrasesoup('div')]
                    print("正在提取"+phrase.text+"的信息...")
                    for liste in lists:

                        f.write("定义："+liste.text+"\n")

                    f.write("\n词典图片URL：\n")
                    for image in images:
                        imagelink="http://www.guoxuedashi.com"+image.get('href')
                        imagepage = requests.get(imagelink)
                        imagesoup = BeautifulSoup(imagepage.content, "html.parser")
                        imgs = imagesoup.select("center img")

                        for img in imgs:
                            f.write(img.get('src'))







