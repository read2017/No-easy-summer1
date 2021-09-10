import sys
sys.path.append('../src')
import query
IP = "202.114.74.170"
Port = 9900
import sys
sys.path.append('../src')
import GstoreConnector
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
            #print(data)
            if data:
                power=float(data[0]['hold_stake']['value'])
                #print(power)
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
        ids=json.loads(res)['results']['bindings']
        id=[]
        for i in ids:
            id.append(i['entity_id']['value'])
        # print(res)
        # print(type(res))
        #print(id)
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
        self.Graph=self.data_process()
        self.edgeLinks=self.csk()

    def data_process(self):
        """
        将输入图预处理
        """
        Node=[]
        #Eme=[]
        i=0
        #for gra in self.graph:
        #    if gra[0] not in Node:
        #        Node.append(gra[0])
        #    if gra[1] not in Node:
        #        Node.append(gra[1])
        for gra in self.graph:
            Node.append(gra[0])
            Node.append(gra[1])
        Node=set(Node)
        #for gra in self.graph:
        #    k=[]
        #    k.append(Node.index(gra[0]))
        #   k.append(Node.index(gra[1]))
        #    k.append(gra[2])
        #    Eme.append(k)
        size=len(Node)
        edgeCount=len(self.graph)
        #edgeCount=len(Eme)
        print("节点数为:%d" % size, "边数为:%d" % edgeCount)
        Graph=[]
        Graph.append(Node)
        #Graph.append(Eme)
        Graph.append(self.graph)
        return Graph

    def csk(self):
        edgeLinks={}
        for gra in self.Graph[1]:
            a,b=gra[0],gra[1]
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
            for gra in self.graph:
                #print(gra)
                if entity1==gra[0] and gra[1]==entity2:
                    #print(111111)
                    control=gra[2]
            return 1
        else:
            paths=self.Check(entity1,entity2)
            if paths:
                control=0
                #print(paths)
                for path in paths:
                    weak = 0
                    link=[]
                    for i in range(len(path)-1):
                        x=0
                        for gra in self.graph:
                            if gra[0]==path[i] and gra[1]==path[i+1]:
                                link.append(gra[2])
                                x=1
                                #print(gra[2])
                        if x==0:
                            paths.remove(path)
                            link.clear()
                            break
                    if link:
                        weak=min(link)
                    control = control + weak
                #print(paths)
                return control,paths

    def calcuAll(self):
        """
        输出所有结点两两间的控股
        """
        Node=self.Graph[0]
        Allcontrol=[]
        Allpath=[]
        for node1 in Node:
            for node2 in Node:
                try:
                    [control,path]=self.calculation(node1,node2)
                    Allcontrol.append([node1,node2,control])
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
        if paths:
            self.exist=True
            graph=[]
            for path in paths:
                #print(path[0])
                #print(path[1])
                ControlA = DataDoor(IP, Port, self.username, self.password, path[0],path[1])
                power=ControlA.data_process()
                print(power)
                if power:
                    graph.append([path[0],path[1],power])
            #print(graph)
            WeakCacul=WeakPath(graph)
            conAB=WeakCacul.calculation(self.entity1,self.entity2)[0]
            allNodes=WeakCacul.Graph[0]
            control=[]
            for node in allNodes:
                if node!=self.entity2:
                    con=WeakCacul.calculation(node,self.entity2)[0]
                    control.append(con)
            if max(control)==conAB:
                self.cotntrol=True
                return conAB
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

    def getFather(self,layer):
        """
        向外提取父节点
        layer:层数
        输出：股权图
        """
        if layer<0:
            print('Error:层数应大于0')
        else:
            #entity=self.entity
            nodes=[]#所有点
            nodes.append(self.entity)
            l=[]
            graph=[]#所有边
            while layer>0:
                for node in nodes:
                    print(node)
                    print(len(nodes))
                    ControlA = DataDoor(IP, Port, self.username, self.password, entity2=node)
                    data = ControlA.data_processA()
                    print(data)
                    if data:
                        for da in data:
                            l.append(da[0])
                            #print(da[0])
                    print(node)
                layer = layer-1
                nodes=nodes+l
                print(layer)
            for node1 in nodes:
                for node2 in nodes:
                    con12= DataDoor(IP, Port, self.username, self.password,node1, node2)
                    power=con12.data_process()
                    if power:
                        #print(power)
                        graph.append([node1,node2,power])
            print(graph)
            return graph

    def data_process(self,layer):
        """
        通过最弱边算法得到控制权
        """
        #graph=self.getFather(layer)
        K=DataDoor(IP, Port, self.username, self.password, self.entity)
        ids=K.get_id()
        print('获取到id')
        control=[]
        for id in ids:
            PE=pentration(self.username,self.password)
            all_graph=PE.getPenetrationNetwork(id,level=layer)
            graph=all_graph['links']
            print('数据加载完毕,开始计算。')
            WeakCacul=WeakPath(graph)
            [con,path]=WeakCacul.calcuAll()
            control.append(con)
        return control

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
            ControlA = DataDoor(IP, Port, self.username, self.password, entity1=self.entity)
            son=ControlA.get_Son_id()
            id = DataDoor(IP, Port, self.username, self.password, entity1=self.entity)
            entity_ids = id.get_id()
            print('获取到id')
            nodes=[]
            nodes.append(entity_ids)#所有点
            nodes.append(son)
            #sonnodes=[]
            #graph=[]#所有边
            while layer>1:
                sonnodes = []
                k=1#计数单位
                for node in nodes[k]:
                    #ControlA = DataDoor(IP, Port, self.username, self.password, entity1=node)
                    #print('开始获取子节点')
                    datas=query.Query_associate_entity_id(node)
                    try:
                        datalist = json.loads(datas)['results']['bindings']
                        #print(111)
                        for data in datalist:
                            sonnodes.append(data['associate_entity_id']['value'])
                    except:
                        pass
                layer=layer-1
                nodes.append(sonnodes)
                k=k+1
            print('子节点提取完毕')
            return nodes

    def getFather(self,layer):
        """
        向外提取父节点
        layer:层数
        输出：股权图
        """
        if layer<0:
            print('Error:层数应大于0')
        else:
            id=DataDoor(IP, Port, self.username, self.password, entity1=self.entity)
            entity=id.get_id()
            nodes=[entity]#所有点
            l=[]
            graph=[]#所有边
            while layer>0:
                for node in nodes:
                    ControlA = DataDoor(IP, Port, self.username, self.password, entity2=node)
                    data = ControlA.data_processA()
                    if data:
                        for da in data:
                            #print(da[0])
                            l.append(da[0])
                layer=layer-1
                nodes=nodes+l
                #print(layer)
            for node1 in nodes:
                for node2 in nodes:
                    con12= DataDoor(IP, Port, self.username, self.password,node1, node2)
                    power=con12.data_process()
                    if power:
                        graph.append([node1,node2,power])
                        #print(power)
            print('父节点提取完毕。')
            return graph


    def data_process(self,layer_son,layer_father):
        """
        输出：属于被查询实体控制系的点，及他们之间的控制权指数
        """
        Sonnodes=self.getSon(layer_son)
        #print('子节点提取完毕')
        entity_ids=Sonnodes[0]
        #print(entity_ids)
        Department=[]
        k=1
        for layer in Sonnodes[1:]:
            print("第{}层，共有{}个节点".format(k, len(layer)))
            k=k+1
            for node in layer:
                PE=pentration(self.username,self.password)
                graph=PE.getPenetrationNetwork(node,level=layer_father)['links']
                #print(graph)
                WeakCacul=WeakPath(graph)
                control=[]
                for no in WeakCacul.Graph[0]:
                    if no!=node:
                        con=WeakCacul.calculation(node,no)[0]
                        #print(no)
                        control.append(con)
                print(control)
                for entity_id in entity_ids:
                    try:
                        conAB=WeakCacul.calculation(node,entity_id)[0]
                        #print(entity_id)
                        print(conAB)
                        if conAB == max(control):
                            Department.append([entity_id, node, conAB])
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
    #x=DataDoor(IP,Port,uesrname,password,'常玉英')
    #print(x.get_id())
    #for data in x.data_processB():
    #    if data[1]==entity2:
    #        print(data)

    #计算二者之间控股示例：第一页面
    #controlAB=ControlAB('常玉英','上海山阳电讯器材厂',uesrname,password)
    #AB=controlAB.data_process()
    #print(AB)
    #exist=controlAB.exist
    #print(exist)
    #control=controlAB.cotntrol
    #print(control)

    #计算实体控制权图代码示例：第二页面
    controlA=ControlA('上海山阳电讯器材厂',uesrname,password)
    data=controlA.data_process(5)#向外提取5层子图
    print(data)

    #计算控制系代码示例；第三页面
    #controlB=ControlFull('常玉英',uesrname,password)
    #print(len(controlB.getSon(2)))
    #B=controlB.data_process(1,3)#向内提取一层
    #print(B)

