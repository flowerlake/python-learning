"""
-*- coding: utf-8 -*-
@author： flowerlake
@time： 2019-09-08 19:39
@description： python-learning, EpollNonBlocking.py
selectors模块是对底层select/poll/epoll/kqueue的封装。DefaultSelector类会根据 OS 环境自动选择最佳的模块
"""

import socket, time
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE

selector = DefaultSelector()

stopped = False


def loop():
    while not stopped:
        # utilize select method blocking
        events = selector.select()
        for event_key, event_mask in events:
            callback = event_key.data
            callback(event_key, event_mask)


class EpollNonBlocking:

    def __init__(self):
        self.sock = None
        self.loop_time = 10
        self.response = b''

    def fetch(self):
        self.sock = socket.socket()
        self.sock.setblocking(False)
        try:
            self.sock.connect(("www.baidu.com", 80))
        except BlockingIOError as e:
            print("Connection error: {}".format(e))

        # 注册socket可写事件(EVENT_WRITE)和可读事件(EVENT_READ)发生后应该采取的回调函数。
        selector.register(self.sock.fileno(), EVENT_WRITE, self.connected)

    def connected(self, key, mask):

        selector.unregister(key.fd)
        get = "GET / Host: www.baidu.com \r\n HTTP/1.1\r\n\r\n".encode("ascii")
        # attend that send method only receive encode byte string
        self.sock.sendall(get)

        selector.register(self.sock.fileno(), EVENT_READ, self.read_response)

    def read_response(self, key, mask):
        global stopped

        # if chunk size > 4kB, next loop will continue ？ That is controlled by system event?
        chunk = self.sock.recv(4096)

        if chunk:
            self.response += chunk
        else:
            selector.unregister(key.fd)
            self.loop_time = self.loop_time - 1
            if not self.loop_time:
                stopped = True


if __name__ == '__main__':
    start_time = time.time()
    for i in range(10):
        nonBlocking = EpollNonBlocking()
        nonBlocking.fetch()
    loop()
    print("EpollNonBlocking time: {:.2f}".format(time.time() - start_time))