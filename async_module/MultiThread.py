"""
author： flowerlake
time： 2019-09-08
description： multiple thread。concurrent.futures 函数库有一个 ThreadPoolExecutor 类可以被用来完成这个任务。

在讨论普通的GIL之前，有一点要强调的是GIL只会影响到那些严重依赖CPU的程序（比如计算型的）。 如果你的程序大部分只会涉及到I/O，比如网络交互，
那么使用多线程就很合适， 因为它们大部分时间都在等待。实际上，你完全可以放心的创建几千个Python线程， 现代操作系统运行这么多线程没有任何压力，没啥可担心的。
"""

import socket, time

from concurrent import futures


class MultiThread:
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
        chunk = http_sock.recv(4096)
        while chunk:
            response += chunk
            # blocking
            chunk = http_sock.recv(4096)
        return response

    def process_way(self):
        workers = 10
        with futures.ThreadPoolExecutor(workers) as executor:
            futs = {executor.submit(MultiThread.blocking_way) for i in range(10)}

        return len([fut.result() for fut in futs])


if __name__ == '__main__':
    start_time = time.time()
    multiProcess = MultiThread()
    multiProcess.process_way()
    print("multiple thread time: {:.2f}".format(time.time() - start_time))
