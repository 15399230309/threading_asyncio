# 定义一个协程
# 定义一个协程很简单，使用async关键字，就像定义普通函数一样：

import time
import asyncio

now = lambda: time.time()


# 通过async关键字定义一个协程（coroutine），协程也是一种对象
async def do_some_work(x):
    print('Watting： ', x)


start = now()

coroutine = do_some_work('A')

loop = asyncio.get_event_loop()

# 协程不能直接运行，需要把协程加入到事件循环（loop），由后者在适当的时候调用协程.
# asyncio.get_event_loop方法可以创建一个事件循环，然后使用run_until_complete将协程注册到事件循环，并启动事件循环。
loop.run_until_complete(coroutine)
print('Time:', now() - start)

'''
Waiting:  2
TIME:  0.0004658699035644531
'''
# ===================================================================================================================

# 创建一个task
'''
协程对象不能直接运行，在注册事件循环的时候，其实是run_until_complete方法将协程包装成为了一个任务（task）对象。
所谓task对象是Future类的子类。保存了协程运行后的状态，用于未来获取协程的结果。
'''

import asyncio
import time

now = lambda: time.time()


async def do_some_work(x):
    print('Waiting: ', x)


start = now()
coroutine = do_some_work(2)
loop = asyncio.get_event_loop()
# task = asyncio.ensure_future(coroutine)
task = loop.create_task(coroutine)
print(task)
loop.run_until_complete(task)
print(task)
print('TIME: ', now() - start)

'''
<Task pending coro=<do_some_work() running at C:\Users\Administrator\Desktop\test1.py:5>>
Waiting:  2
<Task finished coro=<do_some_work() done, defined at C:\Users\Administrator\Desktop\test1.py:5> result=None>

创建task后，task在加入事件循环之前是pending状态，
因为do_some_work中没有耗时的阻塞操作，task很快就执行完毕了。后面打印的finished状态。

asyncio.ensure_future(coroutine) 和 loop.create_task(coroutine)
都可以创建一个task，run_until_complete的参数是一个futrue对象。当传入一个协程，其内部会自动封装成task，task是Future的子类。
isinstance(task, asyncio.Future)将会输出True。
'''

# ===================================================================================================================

# 绑定回调
'''
绑定回调，在task执行完毕的时候可以获取执行的结果，回调的最后一个参数是future对象，
通过该对象可以获取协程返回值。如果回调需要多个参数，可以通过偏函数导入。
'''

import time
import asyncio

now = lambda: time.time()


async def do_some_work(x):
    print('Waiting: ', x)
    return 'Done after {}s'.format(x)


def callback(future):
    print('Callback: ', future.result())


start = now()

coroutine = do_some_work(2)
loop = asyncio.get_event_loop()
task = asyncio.ensure_future(coroutine)
task.add_done_callback(callback)
loop.run_until_complete(task)

# 程序结束也可以直接调用协程对象的result()方法
print('TIME: ', now() - start)

'''
Waiting:  2
Callback:  Done after 2s
TIME:  0.07500433921813965
do_some_work（coroutine） 结束后调用了回调函数，回调函数中打印了 do_some_work（coroutine）的结果

'''
# ===================================================================================================================

# 阻塞和await
'''
使用async可以定义协程对象，使用await可以针对耗时的操作进行挂起，就像生成器里的yield一样，函数让出控制权。
协程遇到await，事件循环将会挂起该协程，执行别的协程，直到其他的协程也挂起或者执行完毕，再进行下一个协程的执行。
耗时的操作一般是一些IO操作，例如网络请求，文件读取等。我们使用asyncio.sleep函数来模拟IO操作。协程的目的也是让这些IO操作异步化。
'''

import asyncio
import time

now = lambda: time.time()

async def do_some_work(x):
    print('Waiting: ', x)
    await asyncio.sleep(x)
    return 'Done after {}s'.format(x)

start = now()

coroutine = do_some_work(2)
loop = asyncio.get_event_loop()
task = asyncio.ensure_future(coroutine)
loop.run_until_complete(task)

print('Task ret: ', task.result())
print('TIME: ', now() - start)


'''
Waiting:  2
Task ret:  Done after 2s
TIME:  2.0821189880371094

在 sleep的时候，使用await让出控制权。即当遇到阻塞调用的函数的时候，使用await方法将协程的控制权让出，
以便loop调用其他的协程。现在我们的例子就用耗时的阻塞操作了。
'''

# ===================================================================================================================
# 并发和并行
'''
asyncio实现并发，就需要多个协程来完成任务，每当有任务阻塞的时候就await，然后其他协程继续工作。
创建多个协程的列表，然后将这些协程注册到事件循环中。
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
Waiting:  1
Waiting:  2
Waiting:  4
Task ret:  Done after 1s
Task ret:  Done after 2s
Task ret:  Done after 4s
TIME:  4.065232276916504

总时间为4s左右。4s的阻塞时间，足够前面两个协程执行完毕。如果是同步顺序的任务，那么至少需要7s。此时我们使用了aysncio实现了并发。
asyncio.wait(tasks) 也可以使用 asyncio.gather(*tasks) ,前者接受一个task列表，后者接收一堆task。'''

# ===================================================================================================================
# 协程嵌套
