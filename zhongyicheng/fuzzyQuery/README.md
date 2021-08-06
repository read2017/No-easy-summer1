# 使用方法
## 导入
`from fuzzyQuery import *`或`import fuzzyQuery`
## 调用
实例化查询对象`FuzzyQuery`，然后调用`query`方法。  
参数见函数注解，可由`help`得到
## 返回
```
<list>[
    <dict>{
        'name': <str> entity name
        'id': <int> ID in enterprise_t_unique
    }
]
```
## 样例
```
#import fuzzyQuery as fuzzy
from fuzzyQuery import *

#fuzz=fuzzy.query.FuzzyQuery('localhost','ename_test')
fuzz=query.FuzzyQuery('localhost','ename_test')
print(fuzz.query('中国华为科技',20))
help(fuzz.query)
```
目前导入的服务器是`202.114.74.170`，index是`ename_test`，port是`8200`