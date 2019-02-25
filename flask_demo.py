
'''
跑一个flask小demo 模仿请求的网络IO
'''
from flask import Flask

import time

app = Flask(__name__)

@app.route('/')
def index():
    time.sleep(5)
    return 'hello!'

if __name__ == '__main__':
    app.run(threaded = True)

