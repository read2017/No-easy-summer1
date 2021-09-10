# Input
- Penetration
    - `host:string`
    - `port:number`
    - `dbname:string` 目前是`entity2`
- getPenetrationNetwork
    - `centerId:string` 查询节点的eid
    - `level:number` *optional* 层数限制
    - `dateFrom` *optional, no-use*
    - `dateTo` *optional, no-use*
# Output
`<dict>{
'nodes':<list>[
    <dict>{'id','name','category','percent'}
],
'links':<list>[
    <dict>{'source','target','value'}
]
}
`
# Example
```python
#import Penetration.penetration as penetration
from Penetration import *
p = penetration.Penetration('202.114.74.170',9900)
p.getPenetrationNetwork(input())
```