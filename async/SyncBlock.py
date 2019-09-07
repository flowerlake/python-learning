import socket


# python的class类只有在需要继承的时候才需要写括号，除此之外，写或不写都无所谓。在不显式继承类的情况下，任何类默认继承object类
class SyncBlock:

    def blocking_way(self):
        sock = socket.socket()
        sock.connect(("www.baidu.com", 80))
