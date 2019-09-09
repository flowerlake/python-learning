"""
-*- coding: utf-8 -*-
@author： flowerlake
@time： 2019-09-09 17：20
@description： tcp connection server
TODO：1、根据消息队列对该客户端进行改进；2、实现server是server，client是client，现在实现的是server和client的通信
"""

import socket, logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("127.0.0.1", 32069))
sock.listen(3)

while True:
    logger.info("Waiting for connect......")

    # For IP sockets, the address info is a pair (hostaddr, port).
    sc, address = sock.accept()
    while True:
        try:
            data = sc.recv(1024)
            print(address, " :", data.decode("utf-8"))
            send_data = input(">>:").strip()
            sc.send(send_data.encode("utf-8"))
        except ConnectionResetError as e:
            logger.info("{} has disconnected.\n".format(address))
    sc.close()
