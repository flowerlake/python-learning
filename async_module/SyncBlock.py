"""
author： flowerlake
time： 2019-09-07
description： synchronize blocking
"""

import socket, time


# python的class类只有在需要继承的时候才需要写括号，除此之外，写或不写都无所谓。在不显式继承类的情况下，任何类默认继承object类
class SyncBlock:

    def __init__(self):
        pass

    def blocking_way(self):
        http_sock = socket.socket()
        http_sock.connect(("www.baidu.com", 80))
        request = "GET / Host: www.baidu.com \r\n HTTP/1.1\r\n\r\n"
        http_sock.send(request.encode("ascii"))
        # b表示byte
        response = b''
        chunk = http_sock.recv(4096)
        while chunk:
            response += chunk
            # blocking
            chunk = http_sock.recv(4096)
        return response


if __name__ == "__main__":
    res = []
    syncBlock = SyncBlock()
    start_time = time.time()
    for i in range(10):
        res.append(syncBlock.blocking_way())
    print("synchronize blocking time: {:.2f}".format(time.time() - start_time))
