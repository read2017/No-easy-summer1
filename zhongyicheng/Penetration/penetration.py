from Penetration.GstoreConnector import GstoreConnector
import json
from queue import Queue
import time
from scipy.sparse import *
from scipy.sparse.linalg import inv
import numpy as np
np.set_printoptions(threshold=np.inf,linewidth=400)

#t_start = time.time()

#getNeighborTot = 0
#commTot = 0
#maxresults = 0
class Penetration:
    def __init__(self,host,port,dbname='entity3',username = "root",password = "123456"):
        self.gc = GstoreConnector(host,port,username,password)
        self.gc.load(dbname,'POST')
        self.db = dbname
    def getEntity(self,id):
        sql = """
    select ?e where
    {{
     ?e <file:///D:/d2rq-0.8.1/vocab/entity_id> "{}" .
    }}""".format(id)
        #print(id,json.loads(self.gc.query(self.db,"json",sql,"GET")))
        res = json.loads(self.gc.query(self.db,"json",sql,"GET"))['results']['bindings'][0]['e']['value']
        return res
    def getNeighbor(self,u):
        global commTot
        global getNeighborTot
        global maxresults
#        t_t = time.time()
#        t_c = time.time()
        sql = """
    select ?e2 ?s where
    {{
     ?e2 <file:///D:/d2rq-0.8.1/vocab/entity_hold> ?hold .
     ?hold <file:///D:/d2rq-0.8.1/vocab/hold_entity> <{e1}> .
     ?hold <file:///D:/d2rq-0.8.1/vocab/hold_stake> ?s .
    }}""".format(e1=u)
    #    print(sql)
        res = json.loads(self.gc.query(self.db,"json",sql,"GET"))['results']['bindings']
    #    maxresults = max(maxresults,len(res))
    #    commTot += time.time() - t_c
    #    getNeighborTot += time.time()-t_t
        return res
    
    def getHoldInfo(self,item):
        return float(item['stake']['value'])
    
    def queryholders(self,hid,depth_limit=10):
        max_d = 0
    #    max_u = ""
        subg = []
        vis = {}
        id2n = {}
        n2id = {}
        q = Queue()
        entity = self.getEntity(hid)
        q.put(entity)
        vis[entity] = 0
        id2n[entity] = 0
        n2id[0] = entity
        while(not q.empty()):
            u = q.get()
            if(vis[u]>max_d):
                max_d = vis[u]
    #            max_u = u
            if(max_d>depth_limit):
                break
            links = self.getNeighbor(u)
            neighbors = map(lambda item: item['e2']['value'], links)
            subg.extend(map(lambda item: (u,item['e2']['value'],float(item['s']['value'])), links))

            for v in neighbors:
                if(not v in vis):
                    q.put(v)
                    id2n[v] = len(id2n)
                    n2id[id2n[v]] = v
                vis[v] = max(vis[v] if v in vis else 0,vis[u]+1)
            # ...
        # ...
    #    print('max_depth',max_d,max_u,'max results',maxresults)
        return subg,id2n,n2id

    #t_running = time.time() - t_start
    #print('running time',t_running)
    #t_calc_s = time.time()
    def getEntityInfo(self,u):
        sql = """
    select * where
    {{
     <{e}> <file:///D:/d2rq-0.8.1/vocab/entity_name> ?n .
     <{e}> <file:///D:/d2rq-0.8.1/vocab/entity_id> ?id .
     optional {{<{e}> <file:///D:/d2rq-0.8.1/vocab/entity_type> ?t .}}
    }}""".format(e=u)
        res = json.loads(self.gc.query(self.db,"json",sql,"GET"))['results']['bindings'][0]
    #    commTot += time.time() - t_c
        return res
    def calcTotalHolding(self,graph,id2n,n2id,target_n):
        result = []
        if(len(graph)):
            col = []
            row = []
            data = []
            for item in graph:
                if(item[0]==item[1]):
        #            print(id2n[item[0]],item)
                    continue
                col.append(id2n[item[0]])
                row.append(id2n[item[1]])
                data.append(item[2])
        #        if(item[2][0]>1):
        #            raise Exception(item[2][0])
            direct_hold_matrix = coo_matrix((data,(row,col)),shape=(len(id2n),len(id2n))).tocsc()
            actual_hold = direct_hold_matrix.dot(inv(identity(len(id2n),format='csc')-direct_hold_matrix)).tocoo()
        #    print('calc over')
            for i,j,d in zip(actual_hold.row,actual_hold.col,actual_hold.data):
                if(j == target_n):
                    eid = n2id[i]
                    tmp = self.getEntityInfo(eid)
                    n = tmp['n']['value']
                    t = tmp['t']['value'] if 't' in tmp else ''
    #                result.append((n2id[i],d))
                    result.append({'id':eid,'percent':d,'category':t,'name':n})
        tmp = self.getEntityInfo(n2id[target_n])
        n = tmp['n']['value']
        t = tmp['t']['value'] if 't' in tmp else ''
        result.append({'id':n2id[target_n],'percent':0,'category':t,'name':n})
        return result
    #print('Total time',time.time() - t_start)
    #print('nodes',len(vis),'edges',len(subg),'query: {} {:.2%}'.format(getNeighborTot,getNeighborTot/t_running),'comm',commTot)
    def getPenetrationNetwork(self,centerId,dateFrom=None,dateTo=None,level=10):
        graph,id2n,n2id = self.queryholders(centerId,level)
        nodes = self.calcTotalHolding(graph,id2n,n2id,id2n[self.getEntity(centerId)])
        return {
            'nodes':nodes,
            'links':list(map(lambda item: {'source':item[0],'target':item[1],'value':item[2]},graph))
        }

