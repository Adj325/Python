import os
import socket
import threading

class Chat:
    def __init__(self):
        self.MEG_LIST = []
        self.MAX_MEG_NUM = 20
        self.Max_LISTENE_NUM = 1024
        self.USER_LIST = []
        self.IP_PORT = ('127.0.0.1', 2018)
        
    def run(self):
        self.display()

    def display(self):
        client = socket.socket()
        try:
            client.connect(self.IP_PORT)
        except ConnectionRefusedError:
            print('警告: 未开启服务器')
            exit(1)
        # 通知服务器, 我已上线
        di = {'n':'显示器_{}'.format(client.getsockname()[1]), 't':'0', 'v':False, 'u':'0'}
        client.sendall(bytes(str(di), encoding='utf-8'))
        
        print('欢迎光临成人聊天室!\n')
        client.recv(1024)
        while True:
            try:
                data = client.recv(1024)
                di = eval(data.decode('utf-8'))
                if di['v'] and di['u'] != '0':
                    self.MEG_LIST.append(di['c'])
                    self.MEG_LIST = self.MEG_LIST[-20::]
                    os.system('cls')
                    print('\n<-----大型成人聊天室----->\n')
                        
                    for meg in self.MEG_LIST:
                        print(meg)

                    print('\n<--------------------->')
            except ConnectionResetError:
                client.close()
                print('系统: 服务器关闭!')
                break
                exit(1)
            except:
                di['c'] = '---- 系统: "{}" 异常退出 ----\n'.format(di['n'])
                client.sendall(bytes(str(di), encoding='utf-8'))
                client.close()
                break
                exit(1)
            
                
                
        client.close()

chat = Chat()
chat.run()

