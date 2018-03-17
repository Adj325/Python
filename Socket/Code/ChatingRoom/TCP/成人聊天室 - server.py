import os
import socket
import threading
# n  昵称
# c  内容
# t  1:用户信息, 0:系统信息
# u  1:普通用户, 0:显示器, 2:系统
# v  True:可见, False:不可见
class Chat:
    def __init__(self):
        self.MEG_LIST = []
        self.MAX_MEG_NUM = 20
        self.Max_LISTENE_NUM = 1024
        self.DISPLAYER = []
        self.IP_PORT = ('127.0.0.1', 2018)
        self.IP_PORT_UDP = ('127.0.0.1', 2019)
        
    def run(self):
        self.server()
    
    def sendToAll(self, con, addr):
        client_data = con.recv(1024)
            
        InfoDi = eval(client_data.decode('utf-8'))
        clientName = InfoDi['n']
        print('---- 系统: "{}" 进入聊天室 ----'.format(clientName))
        # 添加显示器
        if InfoDi['u'] == '0':
            print('添加 {} 到显示器'.format(clientName))
            self.DISPLAYER.append((con, addr))
            while True:
                try:
                    pass
                except:
                    self.DISPLAYER.remove((con, addr))
        else:
            while True:
                try:
                    client_data = con.recv(1024)
                    if len(client_data) != 0:
                        # 在服务器上打印信息
                        di = eval(client_data.decode('utf-8'))
                        if di['v']:
                            print(di['c'])
                            # 转发信息到所有客户机
                            for conDisplayer, addr in self.DISPLAYER:
                                conDisplayer.sendall(client_data)
                except ConnectionResetError:
                    print('系统: "{}" 退出聊天室'.format(clientName))
                
                    di = {'n':'系统', 't':'0', 'v':True, 'u':'2', 'c':': "{}" 退出聊天室'.format(clientName)}
                    data = bytes(str(di), encoding='utf-8')
                    # 转发信息到所有客户机
                    for con, addr in self.DISPLAYER:
                        con.sendall(data)
                    con.close()
                    break
                        

        con.close()
    
    def server(self):
        sk = socket.socket()
        sk.bind(self.IP_PORT)
        sk.listen(self.Max_LISTENE_NUM)
        print('欢迎光临成人聊天室!\n\n系统: 等待连接....\n')        # 死循环等待连接
        while True:
            con, addr = sk.accept()
            con.sendto(bytes('---- 系统: 你已成功登录 ----\n', encoding='utf-8'), addr)  #将信息发送给客户端
            t = threading.Thread(target=self.sendToAll, args=(con, addr))
            t.start()

chat = Chat()
chat.run()

