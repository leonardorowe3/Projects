# coding: utf-8

# In[11]:

from selenium import webdriver
import time
import os
from os import listdir
import jieba
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
import sys

stdi, stdo, stde = sys.stdin, sys.stdout, sys.stderr
reload(sys)  # 通过import引用进来时,setdefaultencoding函数在被系统调用后被删除了，所以必须reload一次
sys.stdin, sys.stdout, sys.stderr = stdi, stdo, stde
sys.setdefaultencoding('utf-8')



def is_element_exist(css):
    try:
        browser.find_element_by_tag_name(css)
        return True
    except:
        return False


def is_class_para(classname):
    elems_div = browser.find_elements_by_tag_name('div')
    for elem_div in elems_div:
        if elem_div.get_attribute('class') == classname: return True
    return False



if __name__ == "__main__":
    if not os.path.exists("/Users/luoliming/Desktop/Hanlintao "):
        os.mkdir("/Users/luoliming/Desktop/Hanlintao ")
    browser = webdriver.Chrome()
    browser.get(
        'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=2&tn=baiduhome_pg&wd=%E9%9F%A9%E6%9E%97%E6%B6%9B&rsv_spt=1&oq=%252FUsers%252Fluoliming%252FDesktop%252FHanlintao&rsv_pq=e7c1d332000e9617&rsv_t=299dAezj8qqSDpkah2ezu65LglSYswEFh33M10nFLvbqgpaeAUvhHIh8v8Ecg2jAOMYB&rqlang=cn&rsv_enter=1&rsv_sug3=9&rsv_sug1=4&rsv_sug7=100&rsv_sug2=0&inputT=2040&rsv_sug4=2041')
    i = 0
    while (i < 20):  # 抓取搜索结果前20页文本
        i = i + 1
        '''开始依次抓取'''
        elems = browser.find_elements_by_class_name('t')
        for elem in elems:
            print("正在抓取文章：" + elem.text + "...")  # 抓取进程可视化
            title = elem.text
            title = title.replace('?', '').replace('/', '').replace('<', '').replace('>', '').replace('|', '').replace(
                '*', '').replace('"', '')
            # 避免文件名禁用符
            elem.find_element_by_tag_name('a').click()
            time.sleep(3)
            browser.switch_to.window(browser.window_handles[-1])
            if is_class_para('para'):

                elems_div = browser.find_elements_by_class_name('para')
                for elem_div in elems_div:
                    # print(elem_div.text)
                    with open('/Users/luoliming/Desktop/Hanlintao' + title + '.txt', "a") as f:  # 将正文内容写入文件，文件名为链接列表名
                        f.write(elem_div.text)
                        f.write('\n')
            elif is_element_exist('p'):
                elems_p = browser.find_elements_by_tag_name('p')
                for elem_p in elems_p:
                    # print(elem_p.text)
                    with open('/Users/luoliming/Desktop/Hanlintao' + title + '.txt', "a") as f:  # 将正文内容写入文件，文件名为链接列表名
                        f.write(elem_p.text)
                        f.write('\n')
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
        browser.find_elements_by_class_name('n')[-1].click()
        time.sleep(3)
        browser.switch_to.window(browser.window_handles[0])
    '''分析抓取结果'''
    all_file = listdir('/Users/luoliming/Desktop/Hanlintao')
    for file in all_file:
        if os.path.getsize(os.path.join("/Users/luoliming/Desktop/Hanlintao", file)) == 0:  # 删除空文件
            os.remove(os.path.join("/Users/jiweilu/Desktop/zhanglixin", file))

# In[26]:


labels = []  # 搜索结果列表
corpus = []  # 空语料库
'''过滤停用词'''
typetxt = open('/Users/luoliming/Desktop/Hanlintao/stop.txt')
texts = ['\u3000', '\n', ' ']  # 爬取的文本中未处理的特殊字符
'''建立停用词库'''
for word in typetxt:
    word = word.strip()
    texts.append(word)
'''建立语料库：分词+过滤停用词'''
for i in range(0, len(all_file)):
    filename = all_file[i]
    filelabel = filename.split('.')[0]
    labels.append(filelabel)
    file_add = '/Users/luoliming/Desktop/Hanlintao' + filename
    print(file_add)
    doc = open(file_add).read()
    data = jieba.cut(doc, cut_all=True)  # 文本分词
    data_adj = ''
    delete_word = []
    for item in data:
        if item not in texts:  # 过滤停用词
            data_adj += item + ' '
        else:
            delete_word.append(item)
    corpus.append(data_adj)  # 语料库建立完成
print corpus[0].encode('utf8')

# In[29]:


'''文本聚类'''
vectorizer = CountVectorizer()  # 将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
transformer = TfidfTransformer()  # 统计每个词语的tf-idf权值
tfidf = transformer.fit_transform(
    vectorizer.fit_transform(corpus))  # 第一个fit_transform计算tf-idf，第二个fit_transform将文本转为词频矩阵
weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词
mykms = KMeans(n_clusters=10)
y = mykms.fit_predict(weight)
for i in range(0, 10):
    label_i = []
    for j in range(0, len(y)):
        if y[j] == i:
            label_i.append(labels[j])
    print('韩林涛第' + str(i) + ':' + str(label_i).decode('string_escape'))# coding: utf-8

# In[11]:


import sys #这里只是一个对sys的引用，只能reload才能进行重新加载
stdi,stdo,stde=sys.stdin,sys.stdout,sys.stderr
reload(sys) #通过import引用进来时,setdefaultencoding函数在被系统调用后被删除了，所以必须reload一次
sys.stdin,sys.stdout,sys.stderr=stdi,stdo,stde
sys.setdefaultencoding('utf-8')
from selenium import webdriver
import time
import os
from os import listdir
import jieba
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans


def is_element_exist(css):
    try:
        browser.find_element_by_tag_name(css)
        return True
    except:
        return False
def is_class_para(classname):
    elems_div=browser.find_elements_by_tag_name('div')
    for elem_div in elems_div:
        if elem_div.get_attribute('class')==classname: return True
    return False

'''程序入口'''
if __name__ == "__main__":
    if not os.path.exists("/Users/luoliming/Desktop/Hanlintao"):
            os.mkdir("/Users/luoliming/Desktop/Hanlintao")      
    browser=webdriver.Chrome()
    browser.get('https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E5%BC%A0%E7%AB%8B%E6%96%B0&oq=%25E5%25BC%25A0%25E4%25BA%25AE&rsv_pq=c125fee500011156&rsv_t=4e0fgmzrRHiiMYKjFsqy5U8NzgZI0FMM03DjCCEJeIEPmCsiE4nzaSmric0&rqlang=cn&rsv_enter=1&rsv_sug3=5&rsv_sug1=4&rsv_sug7=100&bs=%E5%BC%A0%E4%BA%AE')
    i=0
    while(i<20):    #抓取搜索结果前20页文本
        i=i+1
        '''开始依次抓取'''
        elems=browser.find_elements_by_class_name('t')
        for elem in elems:
            print("正在抓取："+elem.text+"...")
            title=elem.text
            title=title.replace('?','').replace('/','').replace('<','').replace('>','').replace('|','').replace('*','').replace('"','')
            #避免文件名禁用符
            elem.find_element_by_tag_name('a').click()
            time.sleep(3)
            browser.switch_to.window(browser.window_handles[-1])
            if is_class_para('para'):

                elems_div=browser.find_elements_by_class_name('para')
                for elem_div in elems_div:
                    #print(elem_div.text)
                    with open('/Users/luoliming/Desktop/Hanlintao'+title+'.txt',"a") as f:  #将正文内容写入文件，文件名为链接列表名
                        f.write(elem_div.text)
                        f.write('\n')
            elif is_element_exist('p'):
                elems_p=browser.find_elements_by_tag_name('p')
                for elem_p in elems_p:
                    #print(elem_p.text)
                    with open('/Users/luoliming/Desktop/Hanlintao'+title+'.txt',"a") as f:  #将正文内容写入文件，文件名为链接列表名
                        f.write(elem_p.text)
                        f.write('\n')
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
        browser.find_elements_by_class_name('n')[-1].click()
        time.sleep(3)
        browser.switch_to.window(browser.window_handles[0])
    '''分析抓取结果'''
    all_file=listdir('/Users/luoliming/Desktop/Hanlintao')
    for file in all_file:
            if os.path.getsize(os.path.join("/Users/luoliming/Desktop/Hanlintao", file)) == 0:  #删除空文件
                os.remove(os.path.join("/Users/luoliming/Desktop/Hanlintao", file))



# In[26]:


labels=[] #搜索结果列表
corpus=[] #空语料库
'''过滤停用词'''
typetxt=open('/Users/luoliming/Desktop/Hanlintao/stop.txt')
texts=['\u3000','\n',' '] #爬取的文本中未处理的特殊字符
'''建立停用词库'''
for word in typetxt:
    word=word.strip()
    texts.append(word)
'''建立语料库：分词+过滤停用词'''
for i in range(0,len(all_file)):
    filename=all_file[i]
    filelabel=filename.split('.')[0]
    labels.append(filelabel)
    file_add='/Users/luoliming/Desktop/Hanlintao'+ filename
    print(file_add)
    doc=open(file_add).read()
    data=jieba.cut(doc,cut_all=True) #文本分词
    data_adj=''
    delete_word=[]
    for item in data:
        if item not in texts: #过滤停用词
            data_adj+=item+' '
        else:
            delete_word.append(item)
    corpus.append(data_adj) #语料库建立完成
print corpus[0].encode('utf8')


# In[29]:


'''聚类算法'''
vectorizer=CountVectorizer()    #将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
transformer=TfidfTransformer()  #统计每个词语的tf-idf权值
tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))   #第一个fit_transform计算tf-idf，第二个fit_transform将文本转为词频矩阵
weight=tfidf.toarray()      #将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
word=vectorizer.get_feature_names()     #获取词袋模型中的所有词
mykms=KMeans(n_clusters=10)
y=mykms.fit_predict(weight)
for i in range(0,10):
    label_i=[]
    for j in range(0,len(y)):
        if y[j]==i:
            label_i.append(labels[j])
    print('韩林涛第'+str(i)+':'+str(label_i).decode('string_escape'))
