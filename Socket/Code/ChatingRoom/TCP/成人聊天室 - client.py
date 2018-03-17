import os
import socket
import threading
# c  昵称
# t  1:用户信息, 0:系统信息
# u  1:普通用户, 0:显示器
# v  True:可见, False:不可见

class Chat:
    def __init__(self):
        self.IP_PORT = ('127.0.0.1', 2018)
        
    def run(self):
        self.client()


    def client(self):
        print('欢迎光临成人聊天室!\n\n')
        name = input('你的名字: ')
        while name == '':
            name = input('你的名字: ')
        print()
        client = socket.socket()
        try:
            client.connect(self.IP_PORT)
        except ConnectionRefusedError:
            print('警告: 未开启服务器')
            exit(1)
        # 通知服务器, 我已上线
        di = {'n':name, 'c':name, 't':'0', 'v':False, 'u':'1'}
        client.sendall(bytes(str(di), encoding='utf-8'))

        # 此后的聊天信息都是不可见的
        di['v'] = True
        try:
            loginInfo = client.recv(1024)
            print(loginInfo.decode('utf-8'))
        except:
            print('警告: 无法登录')
            exit(1)
        while True:
            try:
                meg = input('{}: '.format(name))
                di['t'] = '1'
                di['c'] = '{0:>10s}: {1}'.format(name[:10:], meg)
                client.sendall(bytes(str(di), encoding='utf-8'))
            except ConnectionResetError:
                print('警告: 服务器意外关闭')
                client.close()
                exit(1)
            except:
                di['t'] = '0'
                di['c'] = '---- 系统: "{}" 异常退出 ----\n'.format(name)
                client.sendall(bytes(str(di), encoding='utf-8'))
                client.close()
                exit(1)

chat = Chat()
chat.run()

