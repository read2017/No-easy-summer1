
import requests
import sys
import typing
import time
sys.path.append('../src')
from typing import List
from typing import Dict
import queue
import json
version = sys.version[0]
if version == '3':
        from urllib import parse

class GstoreConnector:
    
        def __init__(self, ip, port, username, password):
            defaultServerIP = "202.114.74.170"
            defaultServerPort = "9000"
            if (ip == "localhost"):
                self.serverIP = defaultServerIP
            else:
                self.serverIP = ip
            self.serverPort = port
            self.Url = "http://" + self.serverIP + ":" + str(self.serverPort)
            self.username = username
            self.password = password
    
        def UrlEncode(self, s):
            
            ret = ""
            if version == '2':
                for i in range(len(s)):
                    c = s[i]
                    if ((ord(c)==42) or (ord(c)==45) or (ord(c)==46) or (ord(c)==47) or (ord(c)==58) or (ord(c)==95)):
                        ret += c
                    elif ((ord(c)>=48) and (ord(c)<=57)):
                        ret += c
                    elif ((ord(c)>=65) and (ord(c)<=90)):
                        ret += c
                    elif ((ord(c)>=97) and (ord(c)<=122)):
                        ret += c
                    elif (ord(c)==32):
                        ret += '+'
                    elif ((ord(c)!=9) and (ord(c)!=10) and (ord(c)!=13)):
                        ret += "{}{:X}".format("%", ord(c))
            elif version == '3':
                ret = parse.quote(s)
            return ret

        def Get(self, strUrl):
            r = requests.get(self.Url + self.UrlEncode(strUrl))
            return r.text

        def Post(self, strUrl, strPost):
            r = requests.post(self.Url + self.UrlEncode(strUrl), strPost)
            return r.text

        def fGet(self, strUrl, filename):
            r = requests.get(self.Url + self.UrlEncode(strUrl), stream=True)
            with open(filename, 'wb') as fd:
                for chunk in r.iter_content(4096):
                    fd.write(chunk)
            return

        def fPost(self, strUrl, strPost, filename):
            r = requests.post(self.Url + self.UrlEncode(strUrl), strPost, stream=True)
            with open(filename, 'wb') as fd:
                for chunk in r.iter_content(4096):
                    fd.write(chunk)
            return

        def build(self, db_name, rdf_file_path, request_type='GET'):
            if request_type == 'GET':        
                strUrl = "/?operation=build&db_name=" + db_name + "&ds_path=" + rdf_file_path + "&username=" + self.username + "&password=" + self.password
                res = self.Get(strUrl)
            elif request_type == 'POST':        
                strUrl = "/build"
                strPost = '{\"db_name\": \"' + db_name + '\", \"ds_path\": \"' + rdf_file_path + '\", \"username\": \"' + self.username + '\", \"password\": \"' + self.password + '\"}'
                res = self.Post(strUrl, strPost)
            return res

        def load(self, db_name, request_type='GET'):
            if request_type == 'GET':        
                strUrl = "/?operation=load&db_name=" + db_name + "&username=" + self.username + "&password=" + self.password
                res = self.Get(strUrl)
            elif request_type == 'POST':        
                strUrl = "/load"
                strPost = '{\"db_name\": \"' + db_name + '\", \"username\": \"' + self.username + '\", \"password\": \"' + self.password + '\"}'
                res = self.Post(strUrl, strPost)
            return res
        
        def unload(self, db_name, request_type='GET'):
            if request_type == 'GET':        
                strUrl = "/?operation=unload&db_name=" + db_name + "&username=" + self.username + "&password=" + self.password
                res = self.Get(strUrl)
            elif request_type == 'POST':        
                strUrl = "/unload"
                strPost = '{\"db_name\": \"' + db_name + '\", \"username\": \"' + self.username + '\", \"password\": \"' + self.password + '\"}'
                res = self.Post(strUrl, strPost)             
            return res

        def user(self, type, username2, addition, request_type='GET'):
            if request_type == 'GET':        
                strUrl = "/?operation=user&type=" + type + "&username1=" + self.username + "&password1=" + self.password + "&username2=" + username2 + "&addition=" +addition
                res = self.Get(strUrl)
            elif request_type == 'POST':        
                strUrl = "/user"
                strPost = '{\"type\": \"' + type + '\", \"username1\": \"' + self.username + '\", \"password1\": \"' + self.password + '\", \"username2\": \"' + username2 + '\", \"addition\": \"' + addition + '\"}'
                res = self.Post(strUrl, strPost)
            return res

        def showUser(self, request_type='GET'):
            if request_type == 'GET':        
                strUrl = "/?operation=showUser&username=" + self.username + "&password=" + self.password
                res = self.Get(strUrl)
            elif request_type == 'POST':        
                strUrl = "/showUser"
                strPost = '{\"username\": \"' + self.username + '\", \"password\": \"' + self.password + '\"}'
                res = self.Post(strUrl, strPost)
            return res

        def query(self, db_name, format, sparql, request_type='GET'):
            if request_type == 'GET':        
                strUrl = "/?operation=query&username=" + self.username + "&password=" + self.password + "&db_name=" + db_name + "&format=" + format + "&sparql=" + sparql
                res = self.Get(strUrl)
            elif request_type == 'POST':        
                strUrl = "/query"
                strPost = '{\"username\": \"' + self.username + '\", \"password\": \"' + self.password + '\", \"db_name\": \"' + db_name + '\", \"format\": \"' + format + '\", \"sparql\": \"' + sparql + '\"}'
                res = self.Post(strUrl, strPost)
            return res

        def fquery(self, db_name, format, sparql, filename, request_type='GET'):
            if request_type == 'GET':        
                strUrl = "/?operation=query&username=" + self.username + "&password=" + self.password + "&db_name=" + db_name + "&format=" + format + "&sparql=" + sparql
                self.fGet(strUrl, filename)
            elif request_type == 'POST':        
                strUrl = "/query"
                strPost = '{\"username\": \"' + self.username + '\", \"password\": \"' + self.password + '\", \"db_name\": \"' + db_name + '\", \"format\": \"' + format + '\", \"sparql\": \"' + sparql + '\"}'
                self.fPost(strUrl, strPost, filename)
            return

        def drop(self, db_name, is_backup, request_type='GET'):
            if request_type == 'GET':      
                if is_backup:  
                    strUrl = "/?operation=drop&db_name=" + db_name + "&username=" + self.username + "&password=" + self.password + "&is_backup=true"
                else:  
                    strUrl = "/?operation=drop&db_name=" + db_name + "&username=" + self.username + "&password=" + self.password + "&is_backup=false"
                res = self.Get(strUrl)
            elif request_type == 'POST':        
                strUrl = "/drop"
                if is_backup: 
                    strPost = '{\"db_name\": \"' + db_name + '\", \"username\": \"' + self.username + '\", \"password\": \"' + self.password + '\", \"is_backup\": \"true\"}'
                else: 
                    strPost = '{\"db_name\": \"' + db_name + '\", \"username\": \"' + self.username + '\", \"password\": \"' + self.password + '\", \"is_backup\": \"false\"}'
                res = self.Post(strUrl, strPost)
            return res

        def monitor(self, db_name, request_type='GET'):    
            if request_type == 'GET':        
                strUrl = "/?operation=monitor&db_name=" + db_name + "&username=" + self.username + "&password=" + self.password
                res = self.Get(strUrl)
            elif request_type == 'POST':        
                strUrl = "/monitor"
                strPost = '{\"db_name\": \"' + db_name + '\", \"username\": \"' + self.username + '\", \"password\": \"' + self.password + '\"}'
                res = self.Post(strUrl, strPost)
            return res

        def checkpoint(self, db_name, request_type='GET'):    
            if request_type == 'GET':        
                strUrl = "/?operation=checkpoint&db_name=" + db_name + "&username=" + self.username + "&password=" + self.password
                res = self.Get(strUrl)
            elif request_type == 'POST':        
                strUrl = "/checkpoint"
                strPost = '{\"db_name\": \"' + db_name + '\", \"username\": \"' + self.username + '\", \"password\": \"' + self.password + '\"}'
                res = self.Post(strUrl, strPost)
            return res

        def show(self, request_type='GET'):
            if request_type == 'GET':        
                strUrl = "/?operation=show&username=" + self.username + "&password=" + self.password
                res = self.Get(strUrl)
            elif request_type == 'POST':        
                strUrl = "/show"
                strPost = '{\"username\": \"' + self.username + '\", \"password\": \"' + self.password + '\"}'
                res = self.Post(strUrl, strPost)
            return res

        def getCoreVersion(self, request_type='GET'):
            if request_type == 'GET':        
                strUrl = "/?operation=getCoreVersion&username=" + self.username + "&password=" + self.password
                res = self.Get(strUrl)
            elif request_type == 'POST':        
                strUrl = "/getCoreVersion"
                strPost = '{\"username\": \"' + self.username + '\", \"password\": \"' + self.password + '\"}'
                res = self.Post(strUrl, strPost)
            return res

        def getAPIVersion(self, request_type='GET'):
            if request_type == 'GET':        
                strUrl = "/?operation=getAPIVersion&username=" + self.username + "&password=" + self.password
                res = self.Get(strUrl)
            elif request_type == 'POST':        
                strUrl = "/getAPIVersion"
                strPost = '{\"username\": \"' + self.username + '\", \"password\": \"' + self.password + '\"}'
                res = self.Post(strUrl, strPost)
            return res

        def exportDB(self, db_name, dir_path, request_type='GET'):
            if request_type == 'GET':        
                strUrl = "/?operation=export&db_name=" + db_name + "&ds_path=" + dir_path + "&username=" + self.username + "&password=" + self.password
                res = self.Get(strUrl)
            elif request_type == 'POST':        
                strUrl = "/export"
                strPost = '{\"db_name\": \"' + db_name + '\", \"ds_path\": \"' + dir_path + '\", \"username\": \"' + self.username + '\", \"password\": \"' + self.password + '\"}'
                res = self.Post(strUrl, strPost)
            return res

def Node_id(graph=[]):
        node1=[]
        nodes=[]
        flag=[]
        i=0
        #print(graph)
        while(i<len(graph)):
            for node in graph[i] :
                if(node not in flag):
                    flag.append(node)
                    link=Query_Hold_type(node)
                    #print('node',link)
                    node1.extend(map(lambda item: (node,item['n']['value'],item['t']['value'] if 't' in item else ''), link))
                    #print(node1)
                    nodes=list(map(lambda item: {'id':item[0],'entity_name':item[1],'category':item[2]},node1))
            i=i+1
        return nodes

def csk(graph=[]):
        edgeLinks={}
        for gra in graph:
            a,b=gra[0],gra[1]
            addEdge(a, b,edgeLinks)  # 进入addEdge函数 把边加进去 注意上面已经读过一行 还需要读取边数edgeCount行
        return edgeLinks

def addEdge(a, b,edgeLinks):  # 该函数进行加边操作   构造一个完整的字典形如
        # 上式为演示的该函数处理完的结果
        if a not in edgeLinks:
            edgeLinks[a] = set()
        if b not in edgeLinks:
            edgeLinks[b] = set()
        edgeLinks[a].add(b)


def Extraction_path(entity1, entity2, path=[],path1={}):
        """
        输出：两点之间的所有路径
        """
        # entity1=self.Graph[0].index(entity1)
        # entity2=self.Graph[0].index(entity2)
        # print('path',path)   取消注释查看当前path的元素
        path = path + [entity1]
        # print('path',path)   取消注释查看当前path的元素
        if entity1 == entity2:
            #print('回溯')
            return [path]
        paths = []
        # 存储所有路径
        #print(paths)
        for node in path1[entity1]:
            if node not in path:
                ns = Extraction_path(node, entity2, path,path1)
                #print(ns)
                for n in ns:
                    paths.append(n)
                    #print(paths,'回溯')
        return paths

    #查询持股公司
def Query_Held_Company(u):
                #''' 查询被持股公司\n 输入：持股人名\u 输出：被持股公司信息\res'''
                # before you run this example, make sure that you have started up ghttp service (using bin/ghttp port)
        IP = "202.114.74.170"
        Port = 9900
        username = "root"
        password = "123456"
        sparql= """
                select * where {{
                ?hold <file:///D:/d2rq-0.8.1/vocab/hold_head_id> "{id}".
                ?hold <file:///D:/d2rq-0.8.1/vocab/hold_stake> ?stake .
                ?hold <file:///D:/d2rq-0.8.1/vocab/hold_tail_id> ?associate_entity_id.
                ?associate_entity <file:///D:/d2rq-0.8.1/vocab/entity_id> ?associate_entity_id.
                ?associate_entity <file:///D:/d2rq-0.8.1/vocab/entity_name> ?associate_entity_name.
                }}""".format(id=u)

                #字符串拼接SELECT ?entity_a_id WHERE {"+ u + " (^vocab:hold_head_id|vocab:hold_tail_id) ?entity_a_id}.
        filename = "res.txt"

                # start a gc with given IP, Port, username and password
        gc = GstoreConnector(IP, Port, username, password)

                # queryjson.loads(gc.query("subgraph","json",sparql,"GET"))['results']['bindings']
        res1=gc.query("entity2","json",sparql,"GET")
        #print(res1)
        res = json.loads(gc.query("entity2","json",sparql,"GET"))['results']['bindings']
        return res
    
def Query_Held_Stake(u,v):
                # before you run this example, make sure that you have started up ghttp service (using bin/ghttp port)
        IP = "202.114.74.170"
        Port = 9900
        username = "root"
        password = "123456"
        sparql= """
    select ?stake ?amount where
    {{
     ?hold <file:///D:/d2rq-0.8.1/vocab/hold_head_id> "{id1}" .
     ?hold <file:///D:/d2rq-0.8.1/vocab/hold_tail_id> "{id2}" .
     ?hold <file:///D:/d2rq-0.8.1/vocab/hold_stake> ?stake .
    ?hold <file:///D:/d2rq-0.8.1/vocab/hold_amount> ?amount.
    }}""".format(id1=u,id2=v)

                #字符串拼接SELECT ?entity_a_id WHERE {"+ u + " (^vocab:hold_head_id|vocab:hold_tail_id) ?entity_a_id}.
        filename = "res.txt"

                # start a gc with given IP, Port, username and password
        gc = GstoreConnector(IP, Port, username, password)

                # queryjson.loads(gc.query("subgraph","json",sparql,"GET"))['results']['bindings']
        res = json.loads(gc.query("entity2","json",sparql,"GET"))['results']['bindings']
        res1=gc.query("entity2","json",sparql,"GET")
        print(u,v,res1)
        return res
    
    #查询持股人及股权信息
def Query_Entity_Id(u):
                        #''' 查询持股人\n 输入：被持股公司\u 输出：持股人信息\res'''
                # before you run this example, make sure that you have started up ghttp service (using bin/ghttp port)
        IP = "202.114.74.170"
        Port = 9900
        username = "root"
        password = "123456"
        sparql= """
                select * where {{
                ?entity <file:///D:/d2rq-0.8.1/vocab/entity_name> ?entity_name.
                ?entity <file:///D:/d2rq-0.8.1/vocab/entity_id> "{id}".
                }}""".format(id=u)
        filename = "res.txt"
        
                # start a gc with given IP, Port, username and password
        gc =  GstoreConnector(IP, Port, username, password)

                # queryjson.loads(gc.query("subgraph","json",sparql,"GET"))['results']['bindings']
        res = json.loads(gc.query("entity2","json",sparql,"GET"))['results']['bindings']
        return res
def Query_Shareholder(u):
                        #''' 查询持股人\n 输入：被持股公司\u 输出：持股人信息\res'''
                # before you run this example, make sure that you have started up ghttp service (using bin/ghttp port)
        IP = "202.114.74.170"
        Port = 9900
        username = "root"
        password = "123456"
        sparql= """
                select * where {{
                ?hold <file:///D:/d2rq-0.8.1/vocab/hold_tail_id> "{id}".
                ?hold <file:///D:/d2rq-0.8.1/vocab/hold_head_id> ?entity_id.
                ?entity <file:///D:/d2rq-0.8.1/vocab/entity_id> ?entity_id.
                ?entity <file:///D:/d2rq-0.8.1/vocab/entity_name> ?entity_name.
                 ?hold <file:///D:/d2rq-0.8.1/vocab/hold_stake> ?stake.
                }}""".format(id=u)
        filename = "res.txt"
        
                # start a gc with given IP, Port, username and password
        gc =  GstoreConnector(IP, Port, username, password)

                # queryjson.loads(gc.query("subgraph","json",sparql,"GET"))['results']['bindings']
        res = json.loads(gc.query("entity2","json",sparql,"GET"))['results']['bindings']
        return res
    #查询持股路径
def Query_associate_entity_id(u):
                        #''' 查询持股id\n 输入：被持股公司id\u 输出：持股人id\res'''
                # before you run this example, make sure that you have started up ghttp service (using bin/ghttp port)
        IP = "202.114.74.170"
        Port = 9900
        username = "root"
        password = "123456"
        sparql= """
                select * where {{
                ?hold <file:///D:/d2rq-0.8.1/vocab/hold_head_id> "{id}".
                ?hold <file:///D:/d2rq-0.8.1/vocab/hold_tail_id> ?associate_entity_id.
                }}""".format(id=u)
        filename = "res.txt"
        
                # start a gc with given IP, Port, username and password
        gc =  GstoreConnector(IP, Port, username, password)

                # queryjson.loads(gc.query("subgraph","json",sparql,"GET"))['results']['bindings']
        res = gc.query("entity2","json",sparql,"GET")
        return res
def Query_Hold_type(u):
                        #''' 查询持股id\n 输入：被持股公司id\u 输出：持股人id\res'''
                # before you run this example, make sure that you have started up ghttp service (using bin/ghttp port)
        IP = "202.114.74.170"
        Port = 9900
        username = "root"
        password = "123456"
        sparql= """
select * where
    {{
     ?e <file:///D:/d2rq-0.8.1/vocab/entity_id> "{id}" .
     ?e <file:///D:/d2rq-0.8.1/vocab/entity_name> ?n .
     optional {{?e <file:///D:/d2rq-0.8.1/vocab/entity_type> ?t .}}
    }}""".format(id=u)
        filename = "res.txt"
        
                # start a gc with given IP, Port, username and password
        gc =  GstoreConnector(IP, Port, username, password)

                # queryjson.loads(gc.query("subgraph","json",sparql,"GET"))['results']['bindings']
        res = json.loads(gc.query("entity2","json",sparql,"GET"))['results']['bindings']
        return res
def Query_Entity(u):
    entity=u
    link=[]
    node=[]
    res2=Query_Shareholder(u)
    res1=Query_Held_Company(u)
    #print("res1",res1)

    #print("res2",res2)
    if len(res1)>0:
        node.extend(list(map(lambda item: {'id':item['associate_entity_id']['value'],'name':item['associate_entity_name']['value'],'category':''},res1)))

    #print(node)
        link.extend(list(map(lambda item: {'target':item['associate_entity_id']['value'],'source':entity,'stake':item['stake']['value']},res1)))
    if len(res2)>0:
        node.extend(list(map(lambda item: {'id':item['entity_id']['value'],'name':item['entity_name']['value'],'category':''},res2)))    
        link.extend(list(map(lambda item: {'target':entity,'source':item['entity_id']['value'],'stake':item['stake']['value']},res2)))
    #print(link)
    return {'nodes':node,
        'links':
        link
        }
def Query_Shareholding_Path(start,end):
                        #''' 查询持股路径\n 输入：持股人，被持股公司\u 输出：持股路径\path[]'''
            q1=queue.Queue()      #创建队列存放关联实体
            vis = {}    #空字典，标记已经遍历过的实体
            edge = {}       ## 空字典，存放路径图上的边
            subgraph=[] #存放未去杂点的路径子图
            path=[]        #创建列表存放路径
            paths=[]
            q1.put(start)
            vis[start]=0
            vis[end]=0
            edge[start]=[]
            edge[end]=[]
            t0=time.time()
            while (not q1.empty() and q1.qsize()<=1500):#提取路径子图not q1.empty() and q1.qsize()<=2000复杂节点可加限制
                    u=q1.get()
                    #print(u)
                    res=Query_Held_Company(u)
                    #print(res)
                    #subgraph.extend(res)#提取查询节点的List
                    #print(subgraph)
                    res1 = map(lambda item: item['associate_entity_id']['value'], res)
                    #print(res1)
                    runningTime=time.time()-t0
                    #print (runningTime)
                    if(runningTime>=180):
                        print("查询超时")
                        break
                    for v in res1:
                            
                            if(not v in vis):
                                    q1.put(v)
                                    edge[v]=[]
                                    
                            vis[v] = max(vis[v] if v in vis else 0,vis[u]+1)
                            #print (v)
                            
                            edge[v].append(u)
                            #print(v)
                            #print(edge[v])
                    #print(edge["9a4b84fc-b51b-4829-a052-263997814567"])
                    
            q2=queue.Queue()
            dict={}
            q2.put(end)
            dict[start]=True
            i=0
            while(not q2.empty()):#去除路径子图杂点
                    u=q2.get()
                    #print (u)
                    res=edge[u]
                    #print(res)
                    dict[u]=True
                    for v in res:
                            if(v==start):
                                    path.append((v,u))
                            if(v not in dict):
                                    q2.put(v)
                                    path.append((v,u))
                        
            #print(len(path))
            #print (path)
            #print(edge["62a0feb2-979c-4688-98a0-4509b958945c"])
            path1=csk(path)
            path2=[]
            PATH=[]
            PATHs=[]
            link=[]
            stake=[]
            amount=[]
            LINK=[]
            paths=Extraction_path(start,end,path2,path1)
            #print(paths)
            while i<len(paths):
                j=0
                long=len(paths[i])
                k=0
                while k<long-1:
                        link.append(paths[i][k+1]) #生成一个新的列表，原列表的最后一位成为第一位
                        k+=1 #依次向前进一位
                        #print(link)
                link.append(path[i][0])
                
                stake.extend(map(lambda x,y: list(map(lambda item: item['stake']['value'], Query_Held_Stake(x,y))),paths[i],link))
                amount.extend(map(lambda x,y: list(map(lambda item: item['amount']['value'], Query_Held_Stake(x,y))),paths[i],link))
                PATH.extend(map(lambda x,y,z,w: {'source':x,'target':y,"stake":z,"amount":w},paths[i],link,stake,amount))
                def parseItem(item):
                    tmp = Query_Held_Stake(item[0],item[1])[0]
                    #print('tmp',tmp)
                    return {'source':item[0],'target':item[1],'stake':tmp['stake']['value'],'amount':tmp['amount']['value']}
                LINK.extend(map(parseItem, path))

                PATHs.extend(PATH)
                i=i+1
            nodes=Node_id(paths)
            #print(path3)
            return {'nodes':nodes,
        'pathlist':
        PATHs,
        'links':
        LINK
        }
#data = Query_Held_Company("74872bcb8aab954c6db239059794df05")
##print(data)
#print(list(map(lambda item: {'id':item['associate_entity_id']['value'],'name':item['associate_entity_name']['value']},data)))
#print(list(map(lambda item: {'target':item['associate_entity_id']['value'],'source':'','stake':item['stake']['value']},data)))
#data1= Query_Shareholder("84117557-ca25-4b5c-97ed-592fa17ba095")
#print(data1)#'"张宝世","呼伦贝尔市新村物流运输有限责任公司"
##print(Query_Hold_type("84117557-ca25-4b5c-97ed-592fa17ba095"

#''''/'' "9a4b84fc-b51b-4829-a052-263997814567","f915d73e-94ab-44bf-8649-0655c99511a1""#'''#另一组测试实体''/''"74872bcb8aab954c6db239059794df05","84117557-ca25-4b5c-97ed-592fa17ba095"
    #/删除此处#进行路径查询测试/'''data2为所查询路径图
#data2=Query_Shareholding_Path("74872bcb8aab954c6db239059794df05","84117557-ca25-4b5c-97ed-592fa17ba095")
#print(data2)
data3=Query_Entity("9a4b84fc-b51b-4829-a052-263997814567")
print(data3)
