import sys
sys.path.append('../src')
import query
import GstoreConnector
IP = "202.114.74.170"
Port = 9900
import sys
sys.path.append('../src')
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
    def __init__(self, IP, Port, username, password):
        self.gc = GstoreConnector.GstoreConnector(IP, Port, username, password)

    def get_data(self,entity1,entity2):
        """
        返回res：从gstore查询到的json数据
        """
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
        res = self.gc.query("entity2", "json", sparql, "GET")
        #print(res)
        #print(type(res))
        return res

    def get_dataA(self,entity2):
        """
               返回res：从gstore查询到的json数据
               """
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
        res = self.gc.query("entity2", "json", sparql, "GET")
        #print(res)
        #print(type(res))
        return res

    def get_dataB(self,entity1):
        """
               返回res：从gstore查询到的json数据
               """
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
        res = self.gc.query("entity2", "json", sparql, "GET")
        #print(res)
        #print(type(res))
        return res

    def data_process(self,entity1,entity2):
        """
        Iuput:由gstore查询得到的数据文件
        Return：二者之间的股权
        """
        result=self.get_data(entity1,entity2)
        res = json.loads(result)
        #print(result)
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
            #print(data)
            if data:
                po=float(data[0]['hold_stake']['value'])
                nodes=[]
                nodes.append({'id':data[0]['entity_id']['value'],'name':entity1,'category':'不详'})
                nodes.append({'id':data[0]['associate_entity_id']['value'],'name':entity2,'category':'不详'})
                #print(power)
                power={'source':data[0]['associate_entity_id']['value'],'target':data[0]['entity_id']['value'],'value':po}
                return power,nodes
        except:
            pass
        #return power

    def data_processA(self,entity2):
        """
        Iuput:由gstore查询得到的数据文件
        Return：二者之间的股权
        """
        result=self.get_dataA(entity2)
        res = json.loads(result)
        data=[]
        #print(res)
        try:
            datas = res['results']['bindings']
            for da in datas:
                data.append([da['entity_name']['value'],entity2,float(da['hold_stake']['value'])])
            #print(data)
            return data
        except:
            pass
        return data

    def data_processB(self,entity1):
        """
        Iuput:由gstore查询得到的数据文件
        Return：二者之间的股权
        """
        result = self.get_dataB(entity1)
        res = json.loads(result)
        data = []
        #print(res)
        try:
            datas = res['results']['bindings']
            for da in datas:
                data.append([entity1, da['associate_entity_name']['value'],float(da['hold_stake']['value'])])
            #print(data)
            return data
        except:
            pass

    def get_id(self,entity1):
        """
                      返回res：从gstore查询到的json数据
                      """
        sparql = """
                                          select * where {
                                           ?entity <file:///D:/d2rq-0.8.1/vocab/entity_name>"%s".
                                           ?entity <file:///D:/d2rq-0.8.1/vocab/entity_id> ?entity_id.
                                          }
                                          """ % (entity1)
        res = self.gc.query("entity2", "json", sparql, "GET")
        ids=json.loads(res)['results']['bindings']
        id=[]
        for i in ids:
            id.append({'id':i['entity_id']['value'],'name':entity1,'category':'不详'})
        # print(res)
        # print(type(res))
        #print(id)
        return id

    def get_Son_id(self,entity1):
        """
        输出所有子节点id（list)
        """
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
        res = self.gc.query("entity2", "json", sparql, "GET")
        #print(res)
        Son_ids=json.loads(res)['results']
        Son_id = []
        if Son_ids:
            son=Son_ids['bindings']
            for i in son:
                Son_id.append({'id':i['associate_entity_id']['value'],'name':i['associate_entity_name']['value'],'category':'E'})
            return Son_id
        # print(res)
        # print(type(res))

class Penetration:
    def __init__(self, host=IP, port=Port, dbname='entity2', username="root", password="123456"):
        self.gc = GstoreConnector.GstoreConnector(host, port, username, password)
        self.gc.load(dbname, 'POST')
        self.db = dbname

    def getNeighbor(self, u):
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
        res = json.loads(self.gc.query(self.db, "json", sql, "GET"))['results']['bindings']
        #    maxresults = max(maxresults,len(res))
        #    commTot += time.time() - t_c
        #    getNeighborTot += time.time()-t_t
        return res

    def getHoldInfo(self, item):
        return float(item['stake']['value'])

    def queryholders(self, hid, depth_limit=10):
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
    def getEntity(self, u):
        sql = """
    select * where
    {{
     ?e <file:///D:/d2rq-0.8.1/vocab/entity_id> "{id}" .
     ?e <file:///D:/d2rq-0.8.1/vocab/entity_name> ?n .
     optional {{?e <file:///D:/d2rq-0.8.1/vocab/entity_type> ?t .}}
    }}""".format(id=u)
        res = json.loads(self.gc.query(self.db, "json", sql, "GET"))['results']['bindings'][0]
        #    commTot += time.time() - t_c
        return res

    def calcTotalHolding(self, graph, id2n, n2id, target_n):
        result = []
        if (len(graph)):
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
            #    print('calc over')
            for i, j, d in zip(actual_hold.row, actual_hold.col, actual_hold.data):
                if (j == target_n):
                    eid = n2id[i]
                    tmp = self.getEntity(eid)
                    n = tmp['n']['value']
                    t = tmp['t']['value'] if 't' in tmp else ''
                    #                result.append((n2id[i],d))
                    result.append({'id': eid, 'percent': d, 'category': t, 'name': n})

        tmp = self.getEntity(n2id[target_n])
        n = tmp['n']['value']
        t = tmp['t']['value'] if 't' in tmp else ''
        result.append({'id': n2id[target_n], 'percent': d, 'category': t, 'name': n})
        return result

    # print('Total time',time.time() - t_start)
    # print('nodes',len(vis),'edges',len(subg),'query: {} {:.2%}'.format(getNeighborTot,getNeighborTot/t_running),'comm',commTot)
    def getPenetrationNetwork(self, centerId, dateFrom=None, dateTo=None, level=10):
        graph, id2n, n2id = self.queryholders(centerId, level)
        nodes = self.calcTotalHolding(graph, id2n, n2id, id2n[centerId])
        return {'nodes': nodes,
                'links':
                #    graph
                    list(map(lambda item: {'source': item[0], 'target': item[1], 'value': item[2]}, graph))
                }

class WeakPath:
    """
    控制权计算文件
    输入：Graph【(a,b,hold)】a持股b hold
    输出：Control【a,b,control】a控制b control
    示例：
    a = [['a', 'b', 2], ['c', 'd', 3],['b','e',2],['a','a',4],['a','e',6]]/输入：[[]],股权网络图；
    b = WeakPath(a)
    [k,path] = b.calculation('a', 'b')/输出为：k:'a'对'b'的控制权(float)，path：’a'控制'b'的所有路径（[[‘a','b']]）
    [w,alpath]=b.calcuAll()/输出为：w:所有节点对之间的控制权（[['a','b',2],[],[]]）；alpath：所有节点对间的控制路径([[['a','b']],[[]],])
    """
    def __init__(self,graph):
        self.graph=graph
        self.edgeLinks=self.csk()

    def csk(self):
        edgeLinks={}
        for gra in self.graph['links']:
            a,b=gra['source'],gra['target']
            self.addEdge(a, b,edgeLinks)  # 进入addEdge函数 把边加进去 注意上面已经读过一行 还需要读取边数edgeCount行
        return edgeLinks

    def addEdge(self,a, b,edgeLinks):  # 该函数进行加边操作   构造一个完整的字典形如
        '''edgeLinks{
      "1":["2" "5"]
      "2":["1" "3" "4"]
      "3":["2" "4" "5"]
      "4":["2" "3" "5"]
      "5":["1" "3" "4"]
      }'''
        # 上式为演示的该函数处理完的结果
        if a not in edgeLinks:
            edgeLinks[a] = set()
        if b not in edgeLinks:
            edgeLinks[b] = set()
        edgeLinks[a].add(b)
        #edgeLinks[b].add(a)#无向图十字链表

    def Check(self, entity1, entity2, path=[]):
        """
        输出：两点之间的所有路径
        """
        # entity1=self.Graph[0].index(entity1)
        # entity2=self.Graph[0].index(entity2)
        # print('path',path)   取消注释查看当前path的元素
        path = path + [entity1]
        # print('path',path)   取消注释查看当前path的元素
        if entity1 == entity2:
            # print('回溯')
            return [path]

        paths = []
        # 存储所有路径
        for node in self.edgeLinks[entity1]:
            if node not in path:
                ns = self.Check(node, entity2, path)
                for n in ns:
                    paths.append(n)
        # print(paths,'回溯')
        return paths

    def calculation(self,entity1,entity2):
        """
        输出entity1对entity2的控制权
        """
        paths=[]
        if entity1==entity2:#自身对自身的控制权,默认为1
            for gra in self.graph['links']:
                #print(gra)
                if entity1==gra['source'] and gra['target']==entity2:
                    #print(111111)
                    control=gra['value']
            return 1
        else:
            paths=self.Check(entity1,entity2)
            if paths:
                pathList=[]
                control=0
                #print(paths)
                for path in paths:
                    p=[]
                    weak = 0
                    link=[]
                    for i in range(len(path)-1):
                        x=0
                        for gra in self.graph['links']:
                            if gra['source']==path[i] and gra['target']==path[i+1]:
                                link.append(gra['value'])
                                p.append(gra)
                                x=1
                                #print(gra[2])
                        if x==0:
                            paths.remove(path)
                            link.clear()
                            p.clear()
                            break
                    if link:
                        weak=min(link)
                        pathList=pathList+p
                    control = control + weak
                #print(paths)
                return control,pathList

    def calculationAB(self,entity1,entity2):
        """
        输出entity1对entity2的控制权
        """
        paths=[]
        if entity1==entity2:#自身对自身的控制权,默认为1
            for gra in self.graph['links']:
                #print(gra)
                if entity1==gra['source'] and gra['target']==entity2:
                    #print(111111)
                    control=gra['value']
            return 1
        else:
            paths=self.Check(entity1,entity2)
            if paths:
                pathList=[]
                control=0
                #print(paths)
                for path in paths:
                    p=[]
                    weak = 0
                    link=[]
                    for i in range(len(path)-1):
                        x=0
                        for gra in self.graph['links']:
                            if gra['source']==path[i] and gra['target']==path[i+1]:
                                link.append(gra['value'])
                                p.append(gra)
                                x=1
                                #print(gra[2])
                        if x==0:
                            paths.remove(path)
                            link.clear()
                            p.clear()
                            break
                    if link:
                        weak=min(link)
                        pathList.append({'controlPower':weak,'links':p})
                    control = control + weak
                #print(paths)
                return control,pathList

    def calcuAll(self):
        """
        输出所有结点两两间的控股
        """
        Node=self.graph['nodes']
        Allcontrol=[]
        Allpath=[]
        for node1 in Node:
            for node2 in Node:
                try:
                    [control,path]=self.calculation(node1['id'],node2['id'])
                    Allcontrol.append({'source':node1['id'],'target':node2['id'],'control':control})
                    Allpath.append(path)
                except:
                    pass
        return Allcontrol,Allpath

class ControlAB:
    """
    查控制关联
    entity1:持股实体
    entity2:被控股公司
    示例：
    controlAB=ControlAB('常玉英','交通银行股份有限公司',uesrname,password)/输入：被查询的俩实体及用户名密码。
    AB=controlAB.data_process()/若二者有控制关系，输出二者的控制权大小（float）,一定要运行该函数
    exist=controlAB.exist/路径是否存在(bool)
    control=controlAB.cotntrol/俩实体间是否有控制关系(bool)
    """
    def __init__(self,entity1,entity2,username,password,exist=False,control=False):
        self.entity1=entity1
        self.entity2=entity2
        self.exist=exist#有无控制关联
        self.cotntrol=control#是否A受B控制
        self.username=username
        self.password=password

    def check(self):
        """
        检验连接是否存在
        """
        path=query.Query_Holder(self.entity1,self.entity2)
        if path:
            self.exist=True
            return path
        else:
            return None

    def data_process(self):
        """
        判断是否存在最大控制关系
        若存在，返回控制权指数
        """
        #if self.exist==True:
        paths = query.Query_Holder(self.entity1, self.entity2)
        #print(1111)
        if paths:
            self.exist=True
            graph=[]
            allNode=[]
            ControlA = DataDoor(IP, Port, self.username, self.password)
            for path in paths:
                #print(path[0])
                #print(path[1])
                power,nodes=ControlA.data_process(path[0],path[1])
                if path[0]==self.entity1:
                    id_1=nodes[0]['id']
                if path[1]==self.entity1:
                    id_1=nodes[1]['id']
                if path[0]==self.entity2:
                    id_2=nodes[0]['id']
                if path[1]==self.entity2:
                    id_2=nodes[1]['id']
                #print(power)
                if power:
                    graph.append(power)
                    allNode=allNode+nodes
            #print(graph)
            WeakCacul=WeakPath({'nodes':allNode,'links':graph})
            conAB=WeakCacul.calculationAB(id_2,id_1)
            control=[]
            #allNode=set(allNode)
            #for node in allNode:
            #    con=WeakCacul.calculation(node['id'],self.entity2)[0]
            #    if con:
            #        control.append(con)
            #if max(control)==conAB[0]:
            #    self.cotntrol=True
            #    return conAB
            result={'totalControlPower':conAB[0],"pathList":conAB[1],'nodes':allNode}
            return result
        else:
            pass

class ControlA:
    """
    输出：二维数组
    示例：
    controlA=ControlA('上海山阳电讯器材厂',uesrname,password)/输入：实体及用户名密码
    data=controlA.data_process(1)#向外提取一层/输出：子图上两两节点的控制权[['','',(float)],[],[],]
    """
    def __init__(self,entity,username,password):
        self.entity=entity
        self.username=username
        self.password=password

    def data_process(self,layer):
        """
        通过最弱边算法得到控制权
        """
        #graph=self.getFather(layer)
        K=DataDoor(IP, Port, self.username, self.password)
        ids=K.get_id(self.entity)
        print('获取到id')
        control=[]
        nodes=[]
        for id in ids:
            PE=Penetration()
            all_graph=PE.getPenetrationNetwork(id['id'],level=layer)
            nodes=nodes+all_graph['nodes']
            print('数据加载完毕,开始计算。')
            WeakCacul=WeakPath(all_graph)
            [con,path]=WeakCacul.calcuAll()
            control=control+con
        data={'nodes':nodes,'links':control}
        return data

class ControlFull:
    """
    查控制网络页面
    耗时较大（子节点需要一个一个提取父节点，而后计算控制权，计算量较大）
    示例：
    controlB=ControlFull('常玉英',uesrname,password)/输入：实体用户名密码
    B=controlB.data_process(1,5)#向内提取一层,对于每一个子节点向外提取5层子图/输出：属于控制系的节点及控制权大小([['常玉英'(id),XXX,(float)],[],[]])
    """
    def __init__(self,entity,username,password):
        self.entity=entity
        self.username=username
        self.password=password

    def getSon(self,layer):
        """
        向内提取子节点
        layer:层数
        输出：所有子节点
        """
        if layer<0:
            print('Error:层数应大于0')
        else:
            ControlA = DataDoor(IP, Port, self.username, self.password)
            son=ControlA.get_Son_id(self.entity)
            entity_ids = ControlA.get_id(self.entity)
            print('获取到id')
            nodes=[]
            nodes.append(entity_ids)#所有点
            nodes.append(son)
            #sonnodes=[]
            #graph=[]#所有边
            while layer>1:
                sonnodes = []
                k=1#计数单位
                for node in son:
                    #ControlA = DataDoor(IP, Port, self.username, self.password, entity1=node)
                    #print('开始获取子节点')
                    datas=ControlA.get_Son_id(node['name'])
                    if datas:
                        sonnodes.append(datas)
                layer=layer-1
                if sonnodes:
                    nodes.append(sonnodes)
                k=k+1
            print('子节点提取完毕')
            return nodes

    def data_process(self,layer_son,layer_father):
        """
        输出：属于被查询实体控制系的点，及他们之间的控制权指数
        """
        Sonnodes=self.getSon(layer_son)
        #print(Sonnodes)
        #print('子节点提取完毕')
        entity_ids=Sonnodes[0]
        #print(entity_ids)
        #print(entity_ids)
        links=[]
        nodes=[]
        k=1
        for layer in Sonnodes[1:]:
            print("第{}层，共有{}个节点".format(k, len(layer)))
            k=k+1
            for node in layer:
                PE=Penetration()
                graph=PE.getPenetrationNetwork(node['id'],level=layer_father)
                #print(graph)
                WeakCacul=WeakPath(graph)
                control=[]
                for no in graph['nodes']:
                    try:
                        con=WeakCacul.calculation(node['id'],no['id'])
                        #print(no)
                        control.append(con[0])
                    except:
                        pass
                print(control)
                for entity_id in entity_ids:
                    try:
                        conAB=WeakCacul.calculation(node['id'],entity_id['id'])
                        #print(entity_id)
                        #print(conAB)
                        if conAB[0] == max(control):
                            node['controlPower']=conAB[0]
                            links=links+conAB[1]
                            nodes.append(node)
                            Department={'nodes':nodes,'links':links}
                            #print(1)
                    except:
                        pass
            #班扎夫指数计算
            #id1.append(self.entity)
            #leng = len(id1)
            #A = np.empty(leng, leng)
            #for i in range(leng - 1):
            #    for j in range(leng - 1):
            #        if id1[i]==self.entity:
            #            index=i
            #        ControlA = DataDoor(IP, Port, username, password, id1[i], id1[j])
            #        ControlA.get_data()
            #        data[i][j] = ControlA.data_process()
            #con = bz.Banzhaf0(A, [[1] * leng] * leng, [1 / (2 ** leng)] * (2 ** leng))
            #con.float_change()
            #control_A = con.Banzhaf()
            #if control_A[index][leng-1]==max(control_A[:,leng-1]):
            #    cons.append({'name':isi,'control':control_A[index][leng-1]})
        return Department

if __name__=='__main__':
    uesrname = 'root'
    password = '123456'
    #entity2='上海山阳电讯器材厂'
    #x=DataDoor(IP,Port,uesrname,password)
    #print(x.data_process('常玉英', '上海山阳电讯器材厂'))
    #print(x.get_Son_id('常玉英'))
    #print(x.get_Son_id('常玉英'))
    #for data in x.data_processB():
    #    if data[1]==entity2:
    #        print(data)
    #x=Penetration(IP,Port)
    #print(x.getPenetrationNetwork('9e7a3a48-00ae-4763-b15c-29adc9603245',3))

    #计算二者之间控股示例：第一页面
    controlAB=ControlAB('常玉英','上海山阳电讯器材厂',uesrname,password)
    AB=controlAB.data_process()
    print(AB)
    #exist=controlAB.exist
    #print(exist)
    #control=controlAB.cotntrol
    #print(control)

    #计算实体控制权图代码示例：第二页面
    #controlA=ControlA('上海山阳电讯器材厂',uesrname,password)
    #data=controlA.data_process(5)#向外提取5层子图
    #print(data)

    #计算控制系代码示例；第三页面
    #controlB=ControlFull('常玉英',uesrname,password)
    #print(len(controlB.getSon(2)))
    #B=controlB.data_process(1,3)#向内提取一层
    #print(B)
    #graph={'nodes': [{'id': '028e78ef59d803be28cd3b451153c662', 'percent': 1.0, 'category': '自然人', 'name': '常玉英'}, {'id': '31a55c18-e90d-4f41-9e6d-92d153933c48', 'percent': 1.0, 'category': '', 'name': '宁夏玉龙福康假肢矫形器装配服务中心(有限公司)'}], 'links': [{'source': '31a55c18-e90d-4f41-9e6d-92d153933c48', 'target': '028e78ef59d803be28cd3b451153c662', 'value': 1.0}]}
    #Weak=WeakPath(graph)
    #print(Weak.edgeLinks)
    #print(Weak.calculationAB('31a55c18-e90d-4f41-9e6d-92d153933c48','028e78ef59d803be28cd3b451153c662'))
