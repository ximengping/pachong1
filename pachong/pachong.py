#!/usr/bin/python
# coding=utf-8
import urllib2
import re
from bs4 import BeautifulSoup
#爬取小说http://www.shengxu6.com
#GB2312汉字编码 GBK 扩展板
#根据url发送request请求，获取服务器相应内容
def OpenPage(url):
#1.构造请求头
    Myheaders={}
#2.构造request请求
    req=urllib2.Request(url,headers=Myheaders)
#3.激活request请求，向服务器端发送请求
#服务器端的请求应被获取，一种类文本的对象
    f=urllib2.urlopen(req)
#4.decode解码函数 encode编码函数（编码名）
    data=f.read()
#ignore replace
    return data.decode("GBK",errors="ignore").encode("utf-8")

#发送网址解析内容
def Test1():
    print OpenPage("http://www.shengxu6.com/book/2967.html")

#解析主页内容，获取url各章节 的网址
def ParseMainPage(page):
    soup=BeautifulSoup(page,"html.parser")
#re.compile  Pattern对象  正则表达式 a标签中含有read的 章节连接地址 
    GetUrl=soup.find_all(href=re.compile("read"))
#每一个元素都是一个类的实例化对象
    UrlList=[]
    for item in GetUrl:  
        UrlList.append("http://www.shengxu6.com"+item["href"]) #类似字典                    
    return UrlList
#解析章节内容，获取标题和正文
def ParseDetailPage(page):
  #解析章节内容
    soup=BeautifulSoup(page,"html.parser")
  #获取章节标题
    title=soup.find_all(class_="panel-heading")[0].get_text()
  #获取章节正文
    content=soup.find_all(class_="content-body")[0].get_text()
    return title,content[:-12]
def Test3():
    page=OpenPage("")
    print ParseDetailPage(page)  

def Test2():
    page=OpenPage("http://www.shengxu6.com/book/2967.html")
    List=ParseMainPage(page)
    print List

#把获取到的内容保存到txt文件里
def WriteDataToFile(data):
    with open("output.txt","a+") as f:
        f.write(data)
def Test4():
    WriteDataToFile("acscsddd")

#main函数
if __name__ =='__main__': 

#url="http://www.shengxu6.com/book/2967.html"
    url=raw_input("请输入要爬取的网址")
  #获取主页相应内容
    MainPage=OpenPage(url)
  #解析主页内容，获取各章节的url
    UrlList=ParseMainPage(MainPage)
    for item in UrlList:
  #遍历获得各个章节的相应内容
        detailPage=OpenPage(item)

#解析各个章节的相应内容 ，获取标题和正文
        title,content=ParseDetailPage(detailPage)
  #把标题和正文组合起来
        data="\n\n\n"+title+"\n\n\n"+content
        WriteDataToFile(data.encode("utf-8"))
    print "Clone Finish"
