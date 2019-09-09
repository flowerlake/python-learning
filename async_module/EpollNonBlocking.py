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
url_todo = ['/', '/1', '/2', '/3', '/4', '/5', '/6', '/7', '/8', '/9']
stopped = False


def loop():
    while not stopped:
        # utilize select method blocking
        # selector.select() 是一个阻塞调用，因为如果事件不发生，那应用程序就没事件可处理，所以就干脆阻塞在这里等待事件发生。
        events = selector.select()
        for event_key, event_mask in events:
            callback = event_key.data
            callback(event_key, event_mask)


class EpollNonBlocking:

    def __init__(self, url):
        self.select_sock = None
        self.url = url
        self.response = b''

    def fetch(self):
        self.select_sock = socket.socket()
        self.select_sock.setblocking(False)
        try:
            self.select_sock.connect(("www.baidu.com", 80))
        except BlockingIOError as e:
            print("Connection error: {}".format(e))
            pass

        # 注册socket可写事件(EVENT_WRITE)和可读事件(EVENT_READ)发生后应该采取的回调函数。
        selector.register(self.select_sock.fileno(), EVENT_WRITE, self.connected)

    def connected(self, key, mask):
        selector.unregister(key.fd)
        # TODO: here is a point that different request get will work, the same get will fail. why?
        get = "GET {} Host: www.baidu.com \r\n HTTP/1.1\r\n\r\n".format(self.url).encode("ascii")
        # attend that send method only receive encode byte string
        self.select_sock.sendall(get)
        selector.register(key.fd, EVENT_READ, self.read_response)

    def read_response(self, key, mask):
        global stopped

        # if chunk size > 4kB, next loop will continue ？ That is controlled by system event?
        chunk = self.select_sock.recv(4096)

        if chunk:
            self.response += chunk
        else:
            selector.unregister(key.fd)
            # self.loop_time = self.loop_time - 1
            url_todo.remove(self.url)
            if not url_todo:
                stopped = True


if __name__ == '__main__':
    start_time = time.time()
    for i in url_todo:
        nonBlocking = EpollNonBlocking(i)
        nonBlocking.fetch()
    loop()
    print("EpollNonBlocking time: {:.2f}".format(time.time() - start_time))
