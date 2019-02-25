

```python
import time
import asyncio

now = lambda : time.time()

async def do_some_work(x):
    print('Waiting: ', x)

start = now()

coroutine = do_some_work(2)

loop = asyncio.get_event_loop()
loop.run_until_complete(coroutine)

print('TIME: ', now() - start)
```

    Waiting:  2
    TIME:  0.004000425338745117
    


```python
# 并发和并行
'''
并发和并行一直是容易混淆的概念。并发通常指有多个任务需要同时进行，
并行则是同一时刻有多个任务执行。
用上课来举例就是，并发情况下是一个老师在同一时间段辅助不同的人功课。
并行则是好几个老师分别同时辅助多个学生功课。
简而言之就是一个人同时吃三个馒头还是三个人同时分别吃一个的情况，
吃一个馒头算一个任务。

asyncio实现并发，
就需要多个协程来完成任务，
每当有任务阻塞的时候就await，
然后其他协程继续工作。
创建多个协程的列表，
然后将这些协程注册到事件循环中。
'''

import asyncio

import time

now = lambda: time.time()

async def do_some_work(x):
    print('Waiting: ', x)

    await asyncio.sleep(x)
    return 'Done after {}s'.format(x)

start = now()

coroutine1 = do_some_work(1)
coroutine2 = do_some_work(2)
coroutine3 = do_some_work(4)

tasks = [
    asyncio.ensure_future(coroutine1),
    asyncio.ensure_future(coroutine2),
    asyncio.ensure_future(coroutine3)
]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

for task in tasks:
    print('Task ret: ', task.result())

print('TIME: ', now() - start)

'''
总时间为4s左右。4s的阻塞时间，足够前面两个协程执行完毕。
如果是同步顺序的任务，那么至少需要7s。
此时我们使用了aysncio实现了并发。
asyncio.wait(tasks) 也可以使用 asyncio.gather(*tasks) ,
前者接受一个task列表，后者接收一堆task。

'''
```

    Waiting:  1
    Waiting:  2
    Waiting:  4
    Task ret:  Done after 1s
    Task ret:  Done after 2s
    Task ret:  Done after 4s
    TIME:  4.0072290897369385
    


```python
# 协程嵌套
'''
使用async可以定义协程，协程用于耗时的io操作，
我们也可以封装更多的io操作过程，这样就实现了嵌套的协程，
即一个协程中await了另外一个协程，如此连接起来。
'''
import asyncio

import time

now = lambda: time.time()

async def do_some_work(x):
    print('Waiting: ', x)

    await asyncio.sleep(x)
    return 'Done after {}s'.format(x)

async def main():
    coroutine1 = do_some_work(1)
    coroutine2 = do_some_work(2)
    coroutine3 = do_some_work(4)

    tasks = [
        asyncio.ensure_future(coroutine1),
        asyncio.ensure_future(coroutine2),
        asyncio.ensure_future(coroutine3)
    ]

    dones, pendings = await asyncio.wait(tasks)

    for task in dones:
        print('Task ret: ', task.result())

start = now()
print('11111111111')
loop = asyncio.get_event_loop()
loop.run_until_complete(main())

print('TIME: ', now() - start)
```

    11111111111
    Waiting:  1
    Waiting:  2
    Waiting:  4
    Task ret:  Done after 2s
    Task ret:  Done after 1s
    Task ret:  Done after 4s
    TIME:  4.006229400634766
    


```python
# 如果使用的是 asyncio.gather创建协程对象，那么await的返回值就是协程运行的结果。


import asyncio

import time

now = lambda: time.time()

async def do_some_work(x):
    print('Waiting: ', x)

    await asyncio.sleep(x)
    return 'Done after {}s'.format(x)

async def main():
    coroutine1 = do_some_work(1)
    coroutine2 = do_some_work(2)
    coroutine3 = do_some_work(4)

    tasks = [
        asyncio.ensure_future(coroutine1),
        asyncio.ensure_future(coroutine2),
        asyncio.ensure_future(coroutine3)
    ]

    results = await asyncio.gather(*tasks)

    for result in results:
        print('Task ret: ', result)
    
start = now()
print('11111111111')
loop = asyncio.get_event_loop()
loop.run_until_complete(main())

print('TIME: ', now() - start)
```

    11111111111
    Waiting:  1
    Waiting:  2
    Waiting:  4
    Task ret:  Done after 1s
    Task ret:  Done after 2s
    Task ret:  Done after 4s
    TIME:  4.0082292556762695
    


```python
# 直接用main返回结果
import asyncio

import time

now = lambda: time.time()

async def do_some_work(x):
    print('Waiting: ', x)

    await asyncio.sleep(x)
    return 'Done after {}s'.format(x)

async def main():
    coroutine1 = do_some_work(1)
    coroutine2 = do_some_work(2)
    coroutine3 = do_some_work(2)

    tasks = [
        asyncio.ensure_future(coroutine1),
        asyncio.ensure_future(coroutine2),
        asyncio.ensure_future(coroutine3)
    ]

    return await asyncio.gather(*tasks)

start = now()

loop = asyncio.get_event_loop()
results = loop.run_until_complete(main())

for result in results:
    print('Task ret: ', result)
```

    Waiting:  1
    Waiting:  2
    Waiting:  2
    Task ret:  Done after 1s
    Task ret:  Done after 2s
    Task ret:  Done after 2s
    


```python
# 请求一个flask应用，测试协程并发
import asyncio
import requests
import time

start = time.time()
async def request():
    url = 'http://127.0.0.1:5000'
    print('watting for ',url)
    response = requests.get(url)
    print ('get response from',url,'result is :' , response.text)

tasks = [asyncio.ensure_future(request()) for i in range(5)]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

end = time.time()

print('cost time:',end-start)
'''
可以发现和正常的请求并没有什么两样，依然还是顺次执行的，耗时 15 秒，
平均一个请求耗时 5秒，说好的异步处理呢？
其实，要实现异步处理，我们得先要有挂起的操作，当一个任务需要等待 IO 结果的时候，可以挂起当前任务，
转而去执行其他任务，这样我们才能充分利用好资源，
上面方法都是一本正经的串行走下来，连个挂起都没有，怎么可能实现异步？想太多了。
'''
```

    watting for  http://127.0.0.1:5000
    get response from http://127.0.0.1:5000 result is : hello!
    watting for  http://127.0.0.1:5000
    get response from http://127.0.0.1:5000 result is : hello!
    watting for  http://127.0.0.1:5000
    get response from http://127.0.0.1:5000 result is : hello!
    watting for  http://127.0.0.1:5000
    get response from http://127.0.0.1:5000 result is : hello!
    watting for  http://127.0.0.1:5000
    get response from http://127.0.0.1:5000 result is : hello!
    cost time: 25.04843258857727
    


```python
'''
要实现异步，接下来我们在了解一下await的用法，使用await可以将耗时的程序挂起，让出控制权。
当协程执行到await，事件循环就将本协程挂起，转而去执行别的协程，知道其他的协程挂起或执行完毕。

所以我们可以将resquest()函数用await挂起

'''
import asyncio
import requests
import time

start = time.time()
async def request():
    url = 'http://127.0.0.1:5000'
    print('watting for ',url)
    response =  await requests.get(url)
    print ('get response from',url,'result is :' , response.text)

tasks = [asyncio.ensure_future(request()) for i in range(5)]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

end = time.time()

print('cost time:',end-start)

'''

'''
```

    Task exception was never retrieved
    future: <Task finished coro=<request() done, defined at <ipython-input-16-6dd24bd7d0ed>:13> exception=TypeError("object Response can't be used in 'await' expression",)>
    Traceback (most recent call last):
      File "<ipython-input-16-6dd24bd7d0ed>", line 16, in request
        response =  await requests.get(url)
    TypeError: object Response can't be used in 'await' expression
    Task exception was never retrieved
    future: <Task finished coro=<request() done, defined at <ipython-input-16-6dd24bd7d0ed>:13> exception=TypeError("object Response can't be used in 'await' expression",)>
    Traceback (most recent call last):
      File "<ipython-input-16-6dd24bd7d0ed>", line 16, in request
        response =  await requests.get(url)
    TypeError: object Response can't be used in 'await' expression
    Task exception was never retrieved
    future: <Task finished coro=<request() done, defined at <ipython-input-16-6dd24bd7d0ed>:13> exception=TypeError("object Response can't be used in 'await' expression",)>
    Traceback (most recent call last):
      File "<ipython-input-16-6dd24bd7d0ed>", line 16, in request
        response =  await requests.get(url)
    TypeError: object Response can't be used in 'await' expression
    Task exception was never retrieved
    future: <Task finished coro=<request() done, defined at <ipython-input-16-6dd24bd7d0ed>:13> exception=TypeError("object Response can't be used in 'await' expression",)>
    Traceback (most recent call last):
      File "<ipython-input-16-6dd24bd7d0ed>", line 16, in request
        response =  await requests.get(url)
    TypeError: object Response can't be used in 'await' expression
    Task exception was never retrieved
    future: <Task finished coro=<request() done, defined at <ipython-input-16-6dd24bd7d0ed>:13> exception=TypeError("object Response can't be used in 'await' expression",)>
    Traceback (most recent call last):
      File "<ipython-input-16-6dd24bd7d0ed>", line 16, in request
        response =  await requests.get(url)
    TypeError: object Response can't be used in 'await' expression
    

    watting for  http://127.0.0.1:5000
    watting for  http://127.0.0.1:5000
    watting for  http://127.0.0.1:5000
    watting for  http://127.0.0.1:5000
    watting for  http://127.0.0.1:5000
    cost time: 25.049432516098022
    


```python

```


```python

```


```python

```


```python

```


```python

```


```python

```


```python

```


```python

```


```python

```


```python

```
