#!/usr/bin/env python
# coding: utf-8

# In[4]:


import numpy as np
import pandas as pd
import sys
import random


# In[128]:


class Banzhaf0:
    """
    A:邻接矩阵
    P：关系概率数组
    Prob：投票类型概率矩阵
    """
    def __init__(self,A,P,Prob,m=5,Rdom = False):
        self.A = A
        self.P = P
        self.Prob = Prob
        self.Rdom = Rdom
        self.m = m
        self.A_star = self.float_change()
        self.control_point = self.control_find()

        
        
    def s12(self,x,A0):
        """
        班扎夫指数计算的前两步
        Args:
            x: 起始投票情况值
            A0: 股权矩阵
        Returns: 
            返回收敛投票状况，或相互转移的多个投票状况  
    
        """
        A = A0
        P = self.P
        A = np.array(A)*np.array(P)
        x0 = x
        x1 = x
        count = 0
        re = []
        M = 100
        for m in range(M):
            count += 1
            x0 = x1
            x1 = A.dot(x1)
            for i,j in enumerate(x1):
                if j > 0:
                    x1[i] = 1
                else:
                    x1[i] = -1
            if list(x1) in np.array(re).tolist():
                flag = np.array(re).tolist().index(list(x1))
                break
            re = re + [x1]    
        return re[flag:]
    
    def control_find(self):
        """
        找到源节点
        return:源节点编号
        """
        A = self.A_star
        Arr = np.array(A)
        n = Arr.shape[0]
        start = []
        end = []
        for i in range(n):
            for j in range(n):
                if Arr[i,j] != 0 and i != j:
                    start.append(i)
                    end.append(j)
        re1 = []
        re2 = []
        re1 = self.source(start,end)
        re2 = self.main_cir(start,end)
        re = list(set(re1)|set(re2))
  #      self.control_point = re
        return re

    def s_all(self,source,target,prob):
        """
        给出source公司对target公司的班扎夫指数值
        Args:
            source: 控股公司
            target: 被控股公司
            prob: 投票类型概率矩阵，长度为2^n的列表
        Returns: 
            返回source公司对target公司的班扎夫指数值 
        """
        Rdom = self.Rdom
        A = self.A_star
        control_point = self.control_point
        P = self.P
        if len(P) < len(A):
            P1 = np.ones((len(A)-len(P),len(P)))
            P2 = np.ones((len(A),len(A)-len(P)))
            P = np.concatenate((np.concatenate((np.array(P),P1),axis=0),P2),axis=1).tolist()
        A = np.array(A) * np.array(P) 
        A = A.T
        n = len(A)
        k = 2**len(control_point)
        re = 0
        if Rdom:
            y = list(range(k))
            i = random.sample(y)
            x0 = self.num2binary(i,n)
            x0 = np.array(x0)
            #print(f'x0:{x0}')
            x1 = self.s12(x0,A)
            #print(f'x1:{x1}{i}')
            for j in range(len(x1)):
                print(x1)
                if x0[source - 1] == x1[j][target - 1]:
                    re += 1/len(x1) * prob[i]
                  #  print(f're:{re} x1:{len(x1)}')
           # print(f'rev:{re}')
            return 2*re - 1
        else:
            for i in range(k):
                x0 = self.num2binary(i,n)
                x0 = np.array(x0)
              #  print(f'x0:{x0}')
                x1 = self.s12(x0,A)
            #print(f'x1:{x1}{i}')
                for j in range(len(x1)):
               #     print(x1)
                    if x0[source - 1] == x1[j][target - 1]:
                #        print(prob[i])
                        re += 1/len(x1) * prob[i]
                 #   print(f're:{re} x1:{len(x1)}')
           # print(f'rev:{re}')
            return 2*re - 1
        
    def source(self,start,left):
        re = []
        for i in start:
            if i not in left:
                re.append(i)
        return list(set(re))
    
    def main_cir(self,start,end):
        graph = {}
        visited = {}
        stack = []
        num = len(end)
        node_l = start
        node_r = end
        for i in range(num):
            n1 = node_l[i]
            n2 = node_r[i]
            if n1 not in graph:
                graph[n1] = [n2]
            elif n2 not in graph[n1]:
                graph[n1].append(n2)
            if n1 not in visited:
                visited[n1] = False
            if n2 not in visited:
                visited[n2] = False
   # print(graph)
    
        re = []
        for node in visited.keys():
            if not visited[node]:
                self.dfs(node, graph, visited, stack,re)
        return list(set(re))
    
    
    def dfs(self,node, graph, visited, stack,Circle_set):
        visited[node] = True
        stack.append(node)
        circle_list = []
        if node in graph:
            for n in graph[node]:
                if n not in stack:
                    if not visited[n]:
                        self.dfs(n, graph, visited, stack,Circle_set)
                else:
                    index = stack.index(n)
                   # print('Circle: ')
                    for i in stack[index:]:
                        Circle_set.append(i)
                      #  print(f'i:{i}')
                    #print(f'n:{n}')
                    circle_set = set(circle_list)
        stack.pop(-1)    
            
        
    def num2binary(self,num,k): 
        """
        生成第num种投票类型，如[0，0，0]
        Args:
            num: 表示第num种投票类型，范围为0-2^k-1，类型为整数
            k: 表示公司数目
        Returns: 
            返回一个0-1列表，代表生成的投票类型
        """
        all_point = k
        control_point = self.control_point
        re = [-1] * len(control_point)
        result = [-1] * all_point
        i = 0
        while num != 0:
            re[-i-1] = num % 2
            if re[-i-1] == 0:
                re[-i-1] = -1
            num = num // 2
            i += 1
        result = np.array(result)
        #print(len(re))
        #print(len(control_point))
        result[control_point] = np.array(re)
        return list(result)
    
    def Banzhaf(self):
        """
        给出资本系中各个公司的班扎夫指数值
        Args:
        Returns: 
            以一个矩阵的形式给出资本系中各个公司的班扎夫指数值
        """
        
        A = self.A
        P = self.P
        prob = self.Prob
        Rdom = self.Rdom
        
        n = len(A)
    
        s = np.zeros_like(A)
        A_star = self.float_change() 
        control_point = self.control_find()
        prob1 = []
        for i in range(len(prob)):
            for j in range(2**(len(A)-n)):
                prob1.append(prob[i]/(2**(len(A)-n)))
        #print(A)
       # print(prob1)
        for i in range(n):
            for j in range(n):
                s[i,j] = self.s_all(i+1,j+1,prob1)
        return s
    
    
    
    def float_change(self):
        """
        处理缺失数据
        :return: 返回经过处理补全后的股权邻接矩阵
        """
        m = self.m
        A = self.A
        A1 = np.array(A)
        stock = np.sum(A1,0)
        float_stock = 1 - stock
        float_stock = np.around(float_stock,decimals=3)
        #print(float_stock)
        find = False
        for i in range(len(stock)):
            #print(float_stock)
            if float_stock[i] > min(A1[:,i])+10**(-3):
                find = True
                break
        if find:
            A2 = np.zeros((m,len(stock)))
            for i in range(len(stock)):
                for j in range(m):
                    A2[j,i] = float_stock[i] / m
            A3 = np.zeros((m+len(stock),m))
            for i in range(m):
                A3[len(stock)+j,j] = 1
            A4 = np.concatenate((np.concatenate((A1,A2),axis=0),A3),axis=1)
            return A4.tolist()
        return A1.tolist()




