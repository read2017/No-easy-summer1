from elasticsearch import Elasticsearch

es = Elasticsearch([
    {'host':'localhost','port':8200},
])
print(es.search(index='ename_test_multiprocess',body={"query":{"match":{"name":str(input())}}})['hits']['hits'])
