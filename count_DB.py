import time
from Tao_mm import shop_list
from multiprocessing import Pool

while True:
    print(shop_list.find().count())
    time.sleep(5)


