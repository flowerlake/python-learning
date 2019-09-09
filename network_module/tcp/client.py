"""
-*- coding: utf-8 -*-
@author： flowerlake
@time： 2019-09-09 17：20
@description： tcp connection client
TODO：不要滥用日志表达
"""

import socket, logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname) - %(message)s")
logger = logging.getLogger(__name__)

# ip_addr = input('请输入对方IP地址：\n').strip()
ip_addr = "127.0.0.1"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client.connect((ip_addr, 32069))


while True:
    msg = input('>>:').strip()
    if len(msg) == 0: continue
    client.send(msg.encode('utf-8'))
    try:
        data_sure = client.recv(1024)
        print("'127.0.0.1:32069' : {}".format(data_sure.decode("utf-8")))
    except ConnectionError:
        pass
client.close()
