import sys
sys.path.append('../src')
import GstoreConnector
import json
import json
from queue import Queue
import time
from scipy.sparse import *
from scipy.sparse.linalg import inv
import numpy as np
np.set_printoptions(threshold=np.inf, linewidth=400)

class DataDoor:
    """
    Input：对应的服务器信息以及所查询的实体
    Output：所查询实体相关联的文件
    示例：
    a=DataDoor(IP, Port, username, password,'常玉英', '上海山阳电讯器材厂')
    a.data_process()
    输入：两实体名；输出：(float)两实体间的股权权

    b=DataDoor(IP, Port, username, password,entity2='上海山阳电讯器材厂')
    b.data_processA()
    输入：实体；输出：[[XXX,'上海山阳电讯器材厂',(float)股权],[],[]]所有持股被查询实体的股权

    c=DataDoor(IP, Port, username, password,entity1='常玉英')
    c.data_processB()
    输入：实体；输出：[['常玉英',XXX,(float)股权],[],[]]所有被被查询实体持股的股权

    d=DataDoor(IP, Port, username, password,entity1='交通银行股份有限公司')
    print(d.get_id())输出：被查询实体Id
    """
    def __init__(self, IP, Port, username, password, entity1='',entity2=''):
        self.IP = IP
        self.Port = Port
        self.username = username
        self.password = password
        self.entity1 = entity1
        self.entity2=entity2

    def get_data(self):
        """
        返回res：从gstore查询到的json数据
        """
        entity1=self.entity1
        entity2=self.entity2
        sparql = """
        select * where {{
                        ?entity <file:///D:/d2rq-0.8.1/vocab/entity_name> "{id1}".
                        ?entity <file:///D:/d2rq-0.8.1/vocab/entity_id> ?entity_id.
                        ?hold <file:///D:/d2rq-0.8.1/vocab/hold_head_id> ?entity_id.
                        ?hold <file:///D:/d2rq-0.8.1/vocab/hold_amount> ?hold_amount.
                        ?hold <file:///D:/d2rq-0.8.1/vocab/hold_stake> ?hold_stake.
                        ?hold <file:///D:/d2rq-0.8.1/vocab/hold_tail_id> ?associate_entity_id.
                        ?associate_entity <file:///D:/d2rq-0.8.1/vocab/entity_id> ?associate_entity_id.
                        ?associate_entity <file:///D:/d2rq-0.8.1/vocab/entity_name> "{id2}".
                        }}""".format(id1=entity1, id2=entity2)
        IP = self.IP
        Port = self.Port
        username = self.username
        password = self.password
        gc = GstoreConnector.GstoreConnector(IP, Port, username, password)
        res = gc.query("entity2", "json", sparql, "GET")
        #print(res)
        #print(type(res))
        return res

    def get_dataA(self):
        """
               返回res：从gstore查询到的json数据
               """
        entity1 = self.entity1
        entity2 = self.entity2
        sparql = """
                                   select * where {
                                    ?entity <file:///D:/d2rq-0.8.1/vocab/entity_name>?entity_name.
                                    ?entity <file:///D:/d2rq-0.8.1/vocab/entity_id> ?entity_id.
                                    ?hold <file:///D:/d2rq-0.8.1/vocab/hold_head_id> ?entity_id.
                                    ?hold <file:///D:/d2rq-0.8.1/vocab/hold_amount> ?hold_amount.
                                    ?hold <file:///D:/d2rq-0.8.1/vocab/hold_stake> ?hold_stake.
                                    ?hold <file:///D:/d2rq-0.8.1/vocab/hold_tail_id> ?associate_entity_id.
                                    ?associate_entity <file:///D:/d2rq-0.8.1/vocab/entity_id> ?associate_entity_id.
                                    ?associate_entity <file:///D:/d2rq-0.8.1/vocab/entity_name> "%s".
                                   }
                                   """ % (entity2)
        IP = self.IP
        Port = self.Port
        username = self.username
        password = self.password
        gc = GstoreConnector.GstoreConnector(IP, Port, username, password)
        res = gc.query("entity2", "json", sparql, "GET")
        #print(res)
        #print(type(res))
        return res

    def get_dataB(self):
        """
               返回res：从gstore查询到的json数据
               """
        entity1 = self.entity1
        entity2 = self.entity2
        sparql = """
                                   select * where {
                                    ?entity <file:///D:/d2rq-0.8.1/vocab/entity_name>"%s".
                                    ?entity <file:///D:/d2rq-0.8.1/vocab/entity_id> ?entity_id.
                                    ?hold <file:///D:/d2rq-0.8.1/vocab/hold_head_id> ?entity_id.
                                    ?hold <file:///D:/d2rq-0.8.1/vocab/hold_amount> ?hold_amount.
                                    ?hold <file:///D:/d2rq-0.8.1/vocab/hold_stake> ?hold_stake.
                                    ?hold <file:///D:/d2rq-0.8.1/vocab/hold_tail_id> ?associate_entity_id.
                                    ?associate_entity <file:///D:/d2rq-0.8.1/vocab/entity_id> ?associate_entity_id.
                                    ?associate_entity <file:///D:/d2rq-0.8.1/vocab/entity_name> ?associate_entity_name.
                                   }
                                   """ % (entity1)
        IP = self.IP
        Port = self.Port
        username = self.username
        password = self.password
        gc = GstoreConnector.GstoreConnector(IP, Port, username, password)
        res = gc.query("entity2", "json", sparql, "GET")
        #print(res)
        #print(type(res))
        return res

    def data_process(self):
        """
        Iuput:由gstore查询得到的数据文件
        Return：二者之间的股权
        """
        result=self.get_data()
        res = json.loads(result)
        #print(res)
        # data = res['head']['vars']['hold_amout']
        #datas = res['results']['bindings']
        #for data in datas:
        #    print(data['associate_entity_name']['value'])
        #    if data['associate_entity_name']['value'] == self.entity2:
        #        power = data['hold_stake']['value']
        try:
            #data = res['head']['vars']['hold_amout']
            data=res['results']['bindings']
            if data:
                power=float(data['hold_stake']['value'])
                return power
        except:
            pass
        #return power

    def data_processA(self):
        """
        Iuput:由gstore查询得到的数据文件
        Return：二者之间的股权
        """
        result=self.get_dataA()
        res = json.loads(result)
        data=[]
        #print(res)
        try:
            datas = res['results']['bindings']
            for da in datas:
                data.append([da['entity_name']['value'],self.entity2,float(da['hold_stake']['value'])])
            #print(data)
            return data
        except:
            pass
        return data

    def data_processB(self):
        """
        Iuput:由gstore查询得到的数据文件
        Return：二者之间的股权
        """
        result = self.get_dataB()
        res = json.loads(result)
        data = []
        #print(res)
        try:
            datas = res['results']['bindings']
            for da in datas:
                data.append([self.entity1, da['associate_entity_name']['value'],float(da['hold_stake']['value'])])
            #print(data)
            return data
        except:
            pass

    def get_id(self):
        """
                      返回res：从gstore查询到的json数据
                      """
        entity1 = self.entity1
        sparql = """
                                          select * where {
                                           ?entity <file:///D:/d2rq-0.8.1/vocab/entity_name>"%s".
                                           ?entity <file:///D:/d2rq-0.8.1/vocab/entity_id> ?entity_id.
                                          }
                                          """ % (entity1)
        IP = self.IP
        Port = self.Port
        username = self.username
        password = self.password
        gc = GstoreConnector.GstoreConnector(IP, Port, username, password)
        res = gc.query("entity2", "json", sparql, "GET")
        id=json.loads(res)['results']['bindings'][0]['entity_id']['value']
        # print(res)
        # print(type(res))
        return id

    def get_Son_id(self):
        """
        输出所有子节点id（list)
        """
        entity1 = self.entity1
        sparql = """
                                   select * where {
                                    ?entity <file:///D:/d2rq-0.8.1/vocab/entity_name>"%s".
                                    ?entity <file:///D:/d2rq-0.8.1/vocab/entity_id> ?entity_id.
                                    ?hold <file:///D:/d2rq-0.8.1/vocab/hold_head_id> ?entity_id.
                                    ?hold <file:///D:/d2rq-0.8.1/vocab/hold_amount> ?hold_amount.
                                    ?hold <file:///D:/d2rq-0.8.1/vocab/hold_stake> ?hold_stake.
                                    ?hold <file:///D:/d2rq-0.8.1/vocab/hold_tail_id> ?associate_entity_id.
                                    ?associate_entity <file:///D:/d2rq-0.8.1/vocab/entity_id> ?associate_entity_id.
                                    ?associate_entity <file:///D:/d2rq-0.8.1/vocab/entity_name> ?associate_entity_name.
                                   }
                                   """ % (entity1)
        IP = self.IP
        Port = self.Port
        username = self.username
        password = self.password
        gc = GstoreConnector.GstoreConnector(IP, Port, username, password)
        res = gc.query("entity2", "json", sparql, "GET")
        Son_ids=json.loads(res)['results']
        Son_id = []
        if Son_ids:
            son=Son_ids['bindings']
            for i in son:
                Son_id.append(i['associate_entity_id']['value'])
        return Son_id
        # print(res)
        # print(type(res))

class pentration:
    """
    股权穿透代码
    好像有点问题：股权层数不够的会出错。
    """
    def __init__(self,username,password):
        self.t_start = time.time()
        self.IP = "localhost"
        self.Port = 9900
        self.username = username
        self.password = password

    def getNeighbor(self,u):
        global commTot
        global getNeighborTot
        global maxresults
        t_t = time.time()
        t_c = time.time()
        gc = GstoreConnector.GstoreConnector(self.IP, self.Port, self.username, self.password)
        db = "entity2"
        gc.load(db, "POST")
        sql = """
    select ?id2 ?stake where
    {{
     ?hold <file:///D:/d2rq-0.8.1/vocab/hold_head_id> ?id2 .
     ?hold <file:///D:/d2rq-0.8.1/vocab/hold_tail_id> "{id}" .
     ?hold <file:///D:/d2rq-0.8.1/vocab/hold_stake> ?stake .
    }}""".format(id=u)
        #    print(sql)
        res = json.loads(gc.query(db, "json", sql, "GET"))['results']['bindings']
        #    maxresults = max(maxresults,len(res))
        #    commTot += time.time() - t_c
        #    getNeighborTot += time.time()-t_t
        return res

    def getHoldInfo(self,item):
        return float(item['stake']['value'])

    # vis = {}
    # subg = []
    # id2n = {}
    # n2id = {}
    def queryholders(self,hid, depth_limit=10):
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
        while (not q.empty()):
            u = q.get()
            if (vis[u] > max_d):
                max_d = vis[u]
            #            max_u = u
            if (max_d > depth_limit):
                break
            links = self.getNeighbor(u)
            neighbors = map(lambda item: item['id2']['value'], links)
            subg.extend(map(lambda item: (u, item['id2']['value'], self.getHoldInfo(item)), links))

            for v in neighbors:
                if (not v in vis):
                    q.put(v)
                    id2n[v] = len(id2n)
                    n2id[id2n[v]] = v
                vis[v] = max(vis[v] if v in vis else 0, vis[u] + 1)
            # ...
        # ...
        #    print('max_depth',max_d,max_u,'max results',maxresults)
        return subg, id2n, n2id

    # t_running = time.time() - t_start
    # print('running time',t_running)
    # t_calc_s = time.time()
    def calcTotalHolding(self,graph, id2n, n2id, target_n):
        result = []
        col = []
        row = []
        data = []
        for item in graph:
            if (item[0] == item[1]):
                #            print(id2n[item[0]],item)
                continue
            col.append(id2n[item[0]])
            row.append(id2n[item[1]])
            data.append(item[2])
        #        if(item[2][0]>1):
        #            raise Exception(item[2][0])
        direct_hold_matrix = coo_matrix((data, (row, col)), shape=(len(id2n), len(id2n))).tocsc()
        actual_hold = direct_hold_matrix.dot(inv(identity(len(id2n), format='csc') - direct_hold_matrix)).tocoo()
        print('calc over')
        for i, j, d in zip(actual_hold.row, actual_hold.col, actual_hold.data):
            if (j == target_n):
                result.append((n2id[i], d))
        return result

    # print('Total time',time.time() - t_start)
    # print('nodes',len(vis),'edges',len(subg),'query: {} {:.2%}'.format(getNeighborTot,getNeighborTot/t_running),'comm',commTot)
    def getPenetrationNetwork(self,centerId, dateFrom=None, dateTo=None, level=10):
        graph, id2n, n2id = self.queryholders(centerId, level)
        nodes = self.calcTotalHolding(graph, id2n, n2id, id2n[centerId])
        return {'nodes': nodes,
                'links':
                    graph
                #    map(lambda item: {'source':item[0],'target':item[1],'value':item[2][0]},graph)
                }

if __name__=='__main__':
    IP = "202.114.74.170"
    Port = 9900
    username = "root"
    password = "123456"
    #a=DataDoor(IP, Port, username, password,'常玉英', '上海山阳电讯器材厂')
    #b=DataDoor(IP, Port, username, password,entity2='上海山阳电讯器材厂')
    #c=DataDoor(IP, Port, username, password,entity1='常玉英')
    d=DataDoor(IP, Port, username, password,entity1='上海山阳电讯器材厂')
    #print(d.get_id())
    #c.get_dataB()
    #print(c.data_processB())
    #b.get_dataA()
    #print(b.data_processA())
    #print(a.get_dataA())
    #print(a.data_process())
    x=pentration(username,password)
    print(x.getPenetrationNetwork('9a4b84fc-b51b-4829-a052-263997814567', level=5)['links'])