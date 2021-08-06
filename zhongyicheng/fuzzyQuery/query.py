from elasticsearch import Elasticsearch
import time

class FuzzyQuery:
    def __init__(self,host_url,default_index,port=9200):
        self.es = Elasticsearch([
                {'host':host_url,'port':port},
            ]
        )
        self.default_index=default_index
    def query(self,s,limit=10,ts=time.time(),index=''):
        """
        :param s:str 查询字符串
        :param limit:int 结果数量，默认10，应小于50
        :param ts:str/float 时间戳，暂时没用上
        :param index:str 检索索引，默认为构造时指定的索引
        """
        if(limit>50):
            raise ValueError("Invalid result limit",limit)
        res_all=self.es.search(
            index=index if index else self.default_index,
            body={
                "query":{
                    "match":{"name":s}
                }
            },
            size=limit
        )
        res = list(map(lambda e: e['_source'],res_all['hits']['hits']))
        return res