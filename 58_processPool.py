from Tao_mm import url_list
from Tao_mm import things_get
from Tao_mm import shop_list
from multiprocessing import Pool

if __name__ == '__main__':
    urls=[]
    for i in (url_list.find({},{'url':1})):
        urls.append(i['url'])
    pool=Pool()
    pool.map(things_get,urls)
