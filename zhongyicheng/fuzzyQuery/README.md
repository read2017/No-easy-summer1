# 使用方法
## 导入
`from fuzzyQuery import *`或`import fuzzyQuery`
## 调用
- 实例化查询对象`FuzzyQuery`，然后调用`query`方法。  
- 使用`FuzzyQuery`对象实例化联合查询对象`CoQuery`，然后调用`query`方法。
参数见函数注解，可由`help`得到
## 返回
- `FuzzyQuery.query`
    ```
    <list>[
        <dict>{
            'name': <str> entity name
            'id': <int> ID in enterprise_t_unique
        }
    ]
    ```
- `CoQuery.query`
  ```
    <list>[
        <dict>{
            'name': <str> entity name
            'id': <str> E_EID in enterprise_t_unique
            'status': <str>
        }
    ]
  ```
## 样例
```python
#import fuzzyQuery as fuzzy
from fuzzyQuery import *
#fuzz=fuzzy.query.FuzzyQuery('localhost','ename_test')
fuzz=query.FuzzyQuery('localhost','ename_test')
print(fuzz.query('中国华为科技',20))
help(fuzz.query)
```

```python
from fuzzyQuery import *

fuzz=query.FuzzyQuery('202.114.74.170','ename_test',port=8200)
co = co_query.CoQuery(fuzz,'202.114.74.167')
co.query('中国华为科技',10)
```
目前elasticsearch导入的服务器是`202.114.74.170`，index是`ename_test`，port是`8200`
