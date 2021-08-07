import pymysql
from elasticsearch import Elasticsearch
#from multiprocessing.dummy import Pool as ThreadPool
import multiprocessing as mp
import re
import time

print('CPUs',mp.cpu_count())
es = Elasticsearch([
        #{'host':'localhost','port':9200},
        {'host':'202.114.74.170','port':8200},
    ]
)
connection = pymysql.connect(user='root', password='zhirong123', database='F_CL_ENTERPRISE_DB', charset='utf8',host='202.114.74.167')
cursor = connection.cursor()
QUERY_STR="""
select ID,E_ENAME from enterprise_t_unique
"""
count = cursor.execute(QUERY_STR)
data = cursor.fetchall()

#pattern = re.compile(r'[^\u4E00-\u9FA5]')
#pattern = re.compile(r'[^\u2E80-\u9FFF^0-9^a-z^A-Z^\(^\)^（^）]')
#def process(s):
#    return pattern.sub('',s)
pattern1 = re.compile(r'[^\u2E80-\u9FFF^0-9^a-z^A-Z^\(^\)^（^）]')
pattern = re.compile('\(待清理\)')
def name_process(s):
    return pattern1.sub('',pattern.sub('',s))
def check_validity(s):
    #print(s.lstrip(),s.lstrip().isalpha())
    return s.isalpha()
cnt = 0
def process(item):
    global cnt
    name = name_process(item[1])
    if(check_validity(name)):
        doc = {
            'name':name,
            'id':item[0],
        }
        es.index(index='ename_test_multiprocess',body=doc)
        cnt = cnt+1
        if(cnt%10000==0):
            print(cnt,'items')
print('CPUs',mp.cpu_count())
t_s = time.time()
pool = mp.Pool(mp.cpu_count())
pool.map(process,data)
pool.close()
print('多进程用时',str(time.time()-t_s))
print(cnt,'over')
