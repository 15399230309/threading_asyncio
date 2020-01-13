# python socket 实现同步web服务器 web_server.py
# go 实现并发客户端请求器  go_test_client.go

******************
### SOCKET 常用方法和参数意义
1. socket.socket(socket_family,socket_type,protocol=0)
> socket_family :
```
socket.AF_INET IPv4（默认）
socket.AF_INET6 IPv6
socket.AF_UNIX 只能够用于单一的Unix系统进程间通信
```

> socket_type:
```socket.SOCK_STREAM　　流式socket , for TCP （默认）
　　socket.SOCK_DGRAM　　 数据报式socket , for UDP
　　socket.SOCK_RAW 原始套接字，普通的套接字无法处理ICMP、IGMP等网络报文，而SOCK_RAW可以；其次，SOCK_RAW也可以处理特殊的IPv4报文；此外，利用原始套接字，可以通过IP_HDRINCL套接字选项由用户构造IP头。
　　socket.SOCK_RDM 是一种可靠的UDP形式，即保证交付数据报但不保证顺序。SOCK_RAM用来提供对原始协议的低级访问，在需要执行某些特殊操作时使用，如发送ICMP报文。SOCK_RAM通常仅限于高级用户或管理员运行的程序使用。
　　socket.SOCK_SEQPACKET 可靠的连续数据包服务
```
> protocol参数：
```angular2html
0　　（默认）与特定的地址家族相关的协议,如果是 0 ，则系统就会根据地址格式和套接类别,自动选择一个合适的协议
```

### 2.套接字对象内建方法
#### 服务器端套接字函数
* s.bind()　　　绑定地址(ip地址,端口)到套接字,参数必须是元组的格式例如：s.bind(('127.0.0.1',8009))
* s.listen(5)　　开始监听，5为最大挂起的连接数
* s.accept()　　被动接受客户端连接，阻塞，等待连接

#### 客户端端套接字函数

* s.connect()　　连接服务器端，参数必须是元组格式例如：s.connect(('127,0.0.1',8009))

#### 公共用途的套接字函数

* s.recv(1024)　　接收TCP数据，1024为一次数据接收的大小
* s.send(bytes)　　发送TCP数据，python3发送数据的格式必须为bytes格式
* s.sendall()　　完整发送数据，内部循环调用send
* s.close()　　关闭套接字


### socket中的一些常用方法

* a = socket.gethostname()     #获得本机的主机名，返回str型数据
* b=socket.gethostbyname(a)  #根据主机名获取ip地址，返回str型数据，也可以是网络上的域名
* c=socket.gethostbyaddr(b)  #通过ip获得该主机的一些信息，返回tuple元组型数据

### Socket 对象(内建)方法
* s.recvfrom() 接收UDP数据，与recv()类似，但返回值是（data,address）。其中data是包含接收数据的字符串，address是发送数据的套接字地址。
* s.sendto()   发送UDP数据，将数据发送到套接字，address是形式为（ipaddr，port）的元组，指定远程地址。返回值是发送的字节数。
* s.getpeername() 返回连接套接字的远程地址。返回值通常是元组（ipaddr,port）。
* s.setsockopt(level,optname[.buflen]) 设置给定套接字选项的值。
* s.getsockopt(level,optname[.buflen])	 返回套接字选项的值。
* s.settimeout(timeout) 设置套接字操作的超时期，timeout是一个浮点数，单位是秒。值为None表示没有超时期。一般，超时期应该在刚创建套接字时设置，因为它们可能用于连接的操作（如connect()）
* s.fileno() 返回套接字的文件描述符。
* s.setblocking(flag)	 如果flag为0，则将套接字设为非阻塞模式，否则将套接字设为阻塞模式（默认值）。非阻塞模式下，如果调用recv()没有发现任何数据，或send()调用无法立即发送数据，那么将引起socket.error异常。
* s.makefile() 创建一个与该套接字相关连的文件





