import time
import pymysql

class CoQuery:
    def __init__(self,fuzz,host_url):
        """
        :param fuzz:FuzzyQuery
        :param host_url:str MySQL服务器地址
        """
        self.__fuzz = fuzz
        self.__connection = pymysql.connect(user='root', password='zhirong123', database='F_CL_ENTERPRISE_DB', charset='utf8',host=host_url)
        self.__cursor = self.__connection.cursor()

    def queryMysql(self,id):
        QUERY_STR="""
select E_EID,E_ENAME,E_STATUS from enterprise_t_unique
where ID="{}"
""".format(id)
        count = self.__cursor.execute(QUERY_STR)
        data = self.__cursor.fetchall()[0]
        #print(data)
        return {'name':data[1],'id':data[0],'status':data[2]}
    def query(self,s,limit=10,ts=time.time(),index=''):
        """
        :param s:str 查询字符串
        :param limit:int 结果数量，默认10，应小于50
        :param ts:str/float 时间戳，暂时没用上
        :param index:str 检索索引，默认为构造时指定的索引
        """
        res = self.__fuzz.query(s,limit,ts,index)
        return [self.queryMysql(item['id']) for item in res]
        