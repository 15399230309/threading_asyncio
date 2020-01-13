import socket


if __name__ == '__main__':

    HOST = 'localhost'    # The remote host
    PORT = 8888 # Arbitrary non-privileged port
    # socket.socket(socket_family, socket_type, protocol=0)
    # AF_INET 协议版本IPV4，
    # SOCK_STREAM（流式socket，for TCP）,
    # socket.SOCK_DGRAM　　 数据报式socket , for UDP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # 此函数比较复杂，没看懂，大致意思为可以设置连接的一些规则。
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 绑定主机名和端口号
        s.bind((HOST, PORT))
        # 设置最大连接数，超过后排队
        s.listen(50)
        while True:
            # 监听连接
            conn, addr = s.accept()
            print('Connected by', addr)
            # 读取连接信息
            with conn:
                while 1:
                    # 接收来自服务器的数据，bytes类型，大小为1024 byte
                    # 一个byte（字节）是8 bit（位），一（KB）为1024个bytes（字节），一兆为1024KB
                    data = conn.recv(1024)
                    if not data:
                        break
                    # 发送数据给客户端连接
                    conn.sendall(data)


