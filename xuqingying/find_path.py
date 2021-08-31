import requests
import sys
import typing

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
                if ((ord(c) == 42) or (ord(c) == 45) or (ord(c) == 46) or (ord(c) == 47) or (ord(c) == 58) or (
                        ord(c) == 95)):
                    ret += c
                elif ((ord(c) >= 48) and (ord(c) <= 57)):
                    ret += c
                elif ((ord(c) >= 65) and (ord(c) <= 90)):
                    ret += c
                elif ((ord(c) >= 97) and (ord(c) <= 122)):
                    ret += c
                elif (ord(c) == 32):
                    ret += '+'
                elif ((ord(c) != 9) and (ord(c) != 10) and (ord(c) != 13)):
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
            strUrl = "/?operation=user&type=" + type + "&username1=" + self.username + "&password1=" + self.password + "&username2=" + username2 + "&addition=" + addition
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


# 查询持股公司
def query_edges(u):
    # ''' 查询被持股公司\n 输入：持股人名\u 输出：被持股公司信息\res'''
    # before you run this example, make sure that you have started up ghttp service (using bin/ghttp port)
    IP = "202.114.74.170"
    Port = 9900
    username = "root"
    password = "123456"
    sparql = """
                select * where {{
                ?entity <file:///D:/d2rq-0.8.1/vocab/entity_name> "{id}".
                ?entity <file:///D:/d2rq-0.8.1/vocab/entity_id> ?entity_id.
                ?hold <file:///D:/d2rq-0.8.1/vocab/hold_head_id> ?entity_id.
                ?hold <file:///D:/d2rq-0.8.1/vocab/hold_tail_id> ?associate_entity_id.
                ?associate_entity <file:///D:/d2rq-0.8.1/vocab/entity_id> ?associate_entity_id.
                ?associate_entity <file:///D:/d2rq-0.8.1/vocab/entity_name> ?associate_entity_name.
                }}""".format(id=u)

    # 字符串拼接SELECT ?entity_a_id WHERE {"+ u + " (^vocab:hold_head_id|vocab:hold_tail_id) ?entity_a_id}.
    filename = "res.txt"

    # start a gc with given IP, Port, username and password
    gc = GstoreConnector(IP, Port, username, password)

    # queryjson.loads(gc.query("subgraph","json",sparql,"GET"))['results']['bindings']
    res = json.loads(gc.query("entity2", "json", sparql, "GET"))['results']['bindings']
    res1 = gc.query("entity2", "json", sparql, "GET")
    # print(res1)
    return res


# 查询持股人及股权信息
def query_Shareholder(u):
    # ''' 查询持股人\n 输入：被持股公司\u 输出：持股人信息\res'''
    # before you run this example, make sure that you have started up ghttp service (using bin/ghttp port)
    IP = "202.114.74.170"
    Port = 9900
    username = "root"
    password = "123456"
    sparql = """
                select * where {{
                ?entity <file:///D:/d2rq-0.8.1/vocab/entity_name> ?entity_name.
                ?entity <file:///D:/d2rq-0.8.1/vocab/entity_id> ?entity_id.
                ?hold <file:///D:/d2rq-0.8.1/vocab/hold_head_id> ?entity_id.
                ?hold <file:///D:/d2rq-0.8.1/vocab/hold_amount> ?hold_amount.
                ?hold <file:///D:/d2rq-0.8.1/vocab/hold_stake> ?hold_stake.
                ?hold <file:///D:/d2rq-0.8.1/vocab/hold_tail_id> ?associate_entity_id.
                ?associate_entity <file:///D:/d2rq-0.8.1/vocab/entity_id> ?associate_entity_id.
                ?associate_entity <file:///D:/d2rq-0.8.1/vocab/entity_name> "{id}".
                }}""".format(id=u)
    filename = "res.txt"

    # start a gc with given IP, Port, username and password
    gc = GstoreConnector(IP, Port, username, password)

    # queryjson.loads(gc.query("subgraph","json",sparql,"GET"))['results']['bindings']
    res = gc.query("entity2", "json", sparql, "GET")
    return res


# 查询持股路径
def queryholders(start, end):
    # ''' 查询持股路径\n 输入：持股人，被持股公司\u 输出：持股路径\path[]'''
    q1 = queue.Queue()  # 创建队列存放关联实体
    vis = {}  # 空字典，标记已经遍历过的实体
    edge = {}  ## 空字典，存放路径图上的边
    subgraph = []  # 存放未去杂点的路径子图
    path = []  # 创建列表存放路径
    q1.put(start)
    vis[start] = 0
    vis[end] = 0
    edge[start] = []
    edge[end] = []
    while (not q1.empty() and q1.qsize() <= 2000):  # 提取路径子图
        u = q1.get()
        # print(u)
        res = query_edges(u)
        # print(res)
        subgraph.extend(res)  # 提取查询节点的List
        # print(subgraph)
        res1 = map(lambda item: item['associate_entity_name']['value'], res)
        # print(res1)

        for v in res1:

            if (not v in vis):
                q1.put(v)
                edge[v] = []

            vis[v] = max(vis[v] if v in vis else 0, vis[u] + 1)
            # print (v)

            edge[v].append(u)
            # print(v)
            # print(edge[v])
        # print(edge["9a4b84fc-b51b-4829-a052-263997814567"])
    q2 = queue.Queue()
    dict = {}
    q2.put(end)
    dict[start] = True
    while (not q2.empty()):  # 去除路径子图杂点
        u = q2.get()
        res = edge[u]
        dict[u] = True
        for v in res:
            if (v == start):
                path.append((v, u))
            if (v not in dict):
                q2.put(v)
                path.append((v, u))

    print(len(path))
    print(path)
    # print(edge["62a0feb2-979c-4688-98a0-4509b958945c"])
    return path


# print(len(data1))