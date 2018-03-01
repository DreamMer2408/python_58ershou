from bs4 import BeautifulSoup
import requests
import pymongo
import time
from multiprocessing import Pool

#连接MongoDB数据库
client=pymongo.MongoClient('localhost',27017)
#建立learn数据库，如果没有会自动创建
learn=client['learn']
#创建数据表
url_list=learn['url_list1']
shop_list=learn['shop_list']

#获取分类链接列表
def channal_get(url):
    url_part='http://bj.58.com'
    channal_links=[]
    wb_data=requests.get(url)
    soup=BeautifulSoup(wb_data.text,'lxml')
    links=soup.select('ul.ym-submnu > li > b > a')

    for link in links:
        channal_link=url_part+link.get('href')
        channal_links.append(channal_link)
    return channal_links

#获取分类中的商品的url，who_sell=0代表个人，1是商家
def get_links_from(channel,page,who_sell=0):
    #'http://bj.58.com/shouji/0/pn1/'
    url=channel+str(who_sell)+'/pn'+str(page)
    wb_data=requests.get(url)
    time.sleep(1)
    soup=BeautifulSoup(wb_data.text,'lxml')
    #判断当前页码有没有有效信息
    if soup.find('td','t'):
        links=soup.select('td.t > a')
        for link in links:
            items_link=link.get('href').split('?')[0]
            #二手手机个人页面前几个是个人回收，而且链接是一个跳转首页链接，给排除掉
            if items_link.split('/')[-1] == 'jump':
                pass
            else:
                url_list.insert_one({'url': items_link})
    else:
        pass

#获取商品信息
def things_get(url):
    wb_data=requests.get(url)
    time.sleep(2)
    soup=BeautifulSoup(wb_data.text,'lxml')
    try:
        titles=soup.select('.box_left_top > h1')[0].text
        price=soup.select('.price_now > i')[0].text
        place=soup.select('.palce_li > span > i ')[0].text
        scan=soup.select('p.info_p > .look_time')[0].text
        want=soup.select('p.info_p > .want_person')[0].text
    except Exception:
        print(url)
    if price=='0':
        print('商品已经下架')
    else:
        shop_list.insert_one({'title':titles,'price':price,'area':place,scan:want})

def get_all_links_from(channel):
    for i in range(1,101):
        get_links_from(channel,i)

if __name__=='__main__':
    channal_links = channal_get('http://bj.58.com/sale.shtml')
    # get_links_from(channal_links[0],1)
    # things_get('http://zhuanzhuan.58.com/detail/957912684012519433z.shtml')
    pool=Pool()
    pool.map(get_all_links_from ,channal_links)
    pool.close()
    pool.join()