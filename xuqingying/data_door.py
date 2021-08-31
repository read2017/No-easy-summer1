import sys

sys.path.append('../src')
import GstoreConnector
import json


class DataDoor:
    """
    Input：对应的服务器信息以及所查询的实体
    Output：所查询实体相关联的字典文件
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

if __name__=='__main__':
    IP = "202.114.74.170"
    Port = 9900
    username = "root"
    password = "123456"
    a=DataDoor(IP, Port, username, password,'常玉英', '上海山阳电讯器材厂')
    b=DataDoor(IP, Port, username, password,entity2='上海山阳电讯器材厂')
    c=DataDoor(IP, Port, username, password,entity1='常玉英')
    #c.get_dataB()
    #print(c.data_processB())
    #b.get_dataA()
    #print(b.data_processA())
    print(a.get_dataA())
    #print(a.data_process())