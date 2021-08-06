import os

__all__=['query']

#Auto install dependency
try:
    from elasticsearch import Elasticsearch
except ModuleNotFoundError:
    #print('error')
    print(os.popen("pip3 install elasticsearch").read())

from fuzzyQuery import query