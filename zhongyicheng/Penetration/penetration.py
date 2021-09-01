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
    def __init__(self,host,port,dbname='entity2',username = "root",password = "123456"):
        self.gc = GstoreConnector(host,port,username,password)
        self.gc.load(dbname,'POST')
        self.db = dbname
    def getNeighbor(self,u):
        global commTot
        global getNeighborTot
        global maxresults
#        t_t = time.time()
#        t_c = time.time()
        sql = """
    select ?id2 ?stake where
    {{
     ?hold <file:///D:/d2rq-0.8.1/vocab/hold_head_id> ?id2 .
     ?hold <file:///D:/d2rq-0.8.1/vocab/hold_tail_id> "{id}" .
     ?hold <file:///D:/d2rq-0.8.1/vocab/hold_stake> ?stake .
    }}""".format(id=u)
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
        q.put(hid)
        vis[hid] = 0
        id2n[hid] = 0
        n2id[0] = hid
        while(not q.empty()):
            u = q.get()
            if(vis[u]>max_d):
                max_d = vis[u]
    #            max_u = u
            if(max_d>depth_limit):
                break
            links = self.getNeighbor(u)
            neighbors = map(lambda item: item['id2']['value'], links)
            subg.extend(map(lambda item: (u,item['id2']['value'],self.getHoldInfo(item)), links))

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
    def calcTotalHolding(self,graph,id2n,n2id,target_n):
        result = []
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
                result.append((n2id[i],d))
        return result
    #print('Total time',time.time() - t_start)
    #print('nodes',len(vis),'edges',len(subg),'query: {} {:.2%}'.format(getNeighborTot,getNeighborTot/t_running),'comm',commTot)
    def getPenetrationNetwork(self,centerId,dateFrom=None,dateTo=None,level=10):
        graph,id2n,n2id = self.queryholders(centerId,level)
        nodes = self.calcTotalHolding(graph,id2n,n2id,id2n[centerId])
        return {'nodes':nodes,
        'links':
        graph
    #    map(lambda item: {'source':item[0],'target':item[1],'value':item[2][0]},graph)
        }