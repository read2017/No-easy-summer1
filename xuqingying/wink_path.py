import numpy as np
import pandas as pd
class WeakPath:
    """
    输入：Graph【(a,b,hold)】a持股b hold
    输出：Control【a,b,control】a控制b control
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
        edgeLinks[b].add(a)

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
        control=0
        paths=[]
        if entity1==entity2:#自身对自身的控制权,默认为1
            control=1
            for gra in self.graph:
                #print(gra)
                if entity1==gra[0] and gra[1]==entity2:
                    #print(111111)
                    control=gra[2]
        else:
            paths=self.Check(entity1,entity2)
            if paths:
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
                [control,path]=self.calculation(node1,node2)
                Allcontrol.append([node1,node2,control])
                Allpath.append(path)
        return Allcontrol,Allpath

if __name__ == '__main__':
    #a = [['a', 'b', 2], ['c', 'd', 3],['b','e',2],['a','a',4],['a','e',6]]
    a=[['王红军', '上海山阳电讯器材厂', 0.01], ['杨建军', '上海山阳电讯器材厂', 0.02], ['杨杰', '上海山阳电讯器材厂', 0.01], ['刘月华', '上海山阳电讯器材厂', 0.01],
     ['沈伟', '上海山阳电讯器材厂', 0.032], ['朱永权', '上海山阳电讯器材厂', 0.008], ['王奎弟', '上海山阳电讯器材厂', 0.01], ['唐明星', '上海山阳电讯器材厂', 0.008],
     ['吴国华', '上海山阳电讯器材厂', 0.01], ['金亚芳', '上海山阳电讯器材厂', 0.008], ['杨秀琴', '上海山阳电讯器材厂', 0.01], ['褚小妹', '上海山阳电讯器材厂', 0.01],
     ['沈引花', '上海山阳电讯器材厂', 0.01], ['徐顺忠', '上海山阳电讯器材厂', 0.008], ['陈亚华', '上海山阳电讯器材厂', 0.008], ['黎彩芳', '上海山阳电讯器材厂', 0.008],
     ['沈小宝', '上海山阳电讯器材厂', 0.01], ['葛连华', '上海山阳电讯器材厂', 0.01], ['王亚芳', '上海山阳电讯器材厂', 0.01], ['杨婉华', '上海山阳电讯器材厂', 0.01],
     ['徐永芳', '上海山阳电讯器材厂', 0.008], ['姜益云', '上海山阳电讯器材厂', 0.01], ['沈小妹', '上海山阳电讯器材厂', 0.01], ['钟连华', '上海山阳电讯器材厂', 0.01],
     ['濮小妹', '上海山阳电讯器材厂', 0.008], ['孙芬华', '上海山阳电讯器材厂', 0.01], ['杨金连', '上海山阳电讯器材厂', 0.008], ['沈芬华', '上海山阳电讯器材厂', 0.008],
     ['陈粉华', '上海山阳电讯器材厂', 0.01], ['朱洪书', '上海山阳电讯器材厂', 0.008], ['沈水忠', '上海山阳电讯器材厂', 0.008], ['杨吉华', '上海山阳电讯器材厂', 0.01],
     ['杨保方', '上海山阳电讯器材厂', 0.01], ['张亚妹', '上海山阳电讯器材厂', 0.008], ['盛金芳', '上海山阳电讯器材厂', 0.01], ['朱芬华', '上海山阳电讯器材厂', 0.01],
     ['王莲华', '上海山阳电讯器材厂', 0.01], ['翁仁仙', '上海山阳电讯器材厂', 0.008], ['施元立', '上海山阳电讯器材厂', 0.01], ['褚宝方', '上海山阳电讯器材厂', 0.01],
     ['王仁方', '上海山阳电讯器材厂', 0.01], ['付仁仙', '上海山阳电讯器材厂', 0.008], ['周仁宝', '上海山阳电讯器材厂', 0.008], ['沈引芳', '上海山阳电讯器材厂', 0.01],
     ['杨仁林', '上海山阳电讯器材厂', 0.01], ['朱亚连', '上海山阳电讯器材厂', 0.01], ['朱忠华', '上海山阳电讯器材厂', 0.008], ['沈婉华', '上海山阳电讯器材厂', 0.008],
     ['奚建兵', '上海山阳电讯器材厂', 0.01], ['常玉英', '上海山阳电讯器材厂', 0.01], ['沈元华', '上海山阳电讯器材厂', 0.008], ['杨士云', '上海山阳电讯器材厂', 0.02],
     ['魏秀军', '上海山阳电讯器材厂', 0.01], ['沈彩萍', '上海山阳电讯器材厂', 0.01], ['杨仁忠', '上海山阳电讯器材厂', 0.08], ['骆婉英', '上海山阳电讯器材厂', 0.01],
     ['翁引仙', '上海山阳电讯器材厂', 0.008], ['蒋月芳', '上海山阳电讯器材厂', 0.008], ['曹友余', '上海山阳电讯器材厂', 0.02], ['朱龙妹', '上海山阳电讯器材厂', 0.01],
     ['黄 翠仙', '上海山阳电讯器材厂', 0.01], ['朱火龙', '上海山阳电讯器材厂', 0.048], ['谢永琴', '上海山阳电讯器材厂', 0.01], ['胡德兴', '上海山阳电讯器材厂', 0.02],
     ['奚引勤', '上海山阳电讯器材厂', 0.01], ['朱效忠', '上海山阳电讯器材厂', 0.02], ['褚康龙', '上海山阳电讯器材厂', 0.032], ['钟仁贤', '上海山阳电讯器材厂', 0.01],
     ['王水余', '上海山阳电讯器材厂', 0.02], ['张仁连', '上海山阳电讯器材厂', 0.01], ['褚福明', '上海山阳电讯器材厂', 0.008],
     ['平顶山市安特商贸有限公司', '上海山阳电讯器材厂', 0.008], ['朱志云', '上海山阳电讯器材厂', 0.01], ['邬金芳', '上海山阳电讯器材厂', 0.01],
     ['沈引娣', '上海山阳电讯器材厂', 0.01], ['于美保', '上海山阳电讯器材厂', 0.01], ['钟友良', '上海山阳电讯器材厂', 0.008], ['沈培华', '上海山阳电讯器材厂', 0.008],
     ['徐友华', '上海山阳电讯器材厂', 0.01], ['钟友龙', '上海山阳电讯器材厂', 0.048]]

    b = WeakPath(a)
    [k,path] = b.calculation('徐友华', '上海山阳电讯器材厂')
    #k = b.calculation('a', 'b')
    print(k)
    print(path)
    [w,alpath]=b.calcuAll()
    print(w)