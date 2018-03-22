A simple python version of hystrix.

USAGE 
---------------
```python
from hystrix import addHystrix
@addHystrix(groupKey='group1',key='key1',failback=func)
def callHello():
    pass

```


FSM 
---------------
1. **CIRCUIT_OPEN** : All requests will be allowed
2. **CIRCUIT__HALF_OPEN** : request will be allowed once 
3. **CIRCUIT_CLOSE** : All requests is rejected.

State transitions:

`OPEN --> CLOSE --> HALF_OPEN --> CLOSE/OPEN`