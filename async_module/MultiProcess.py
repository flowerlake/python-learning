"""
author： flowerlake
time： 2019-09-07
description： multiple process
"""

import socket, time

from concurrent import futures

import async_module.SyncBlock


class MultiProcess:
    def __init__(self):
        pass

    @staticmethod
    def blocking_way():
        http_sock = socket.socket()
        http_sock.connect(("www.baidu.com", 80))
        request = "GET / Host: www.baidu.com \r\n HTTP/1.1\r\n\r\n"
        http_sock.send(request.encode("ascii"))
        # b表示byte
        response = b''
        # TODO：如何确定send or recv的缓冲区大小，或者说buffer size大小对程序效率的影响
        # https://blog.csdn.net/wangst4321/article/details/8789779
        chunk = http_sock.recv(4096)
        while chunk:
            response += chunk
            # blocking
            chunk = http_sock.recv(4096)
        return response

    def process_way(self):
        workers = 10
        with futures.ProcessPoolExecutor(workers) as executor:
            futs = {executor.submit(MultiProcess.blocking_way) for i in range(10)}

        return len([fut.result() for fut in futs])


if __name__ == '__main__':
    start_time = time.time()
    multiProcess = MultiProcess()
    multiProcess.process_way()
    print("multiple process time: {:.2f}".format(time.time()-start_time))
