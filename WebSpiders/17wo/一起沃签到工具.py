import os
import re
import base64
import requests
from http import cookiejar


class Wo:
    def __init__(self):
        # 默认主页
        self.index_url = 'http://112.96.28.245/citic/home'
        # 登录主页
        self.login_url = 'http://112.96.28.245/login/loginPageActionForBusiness'
        # 验证码
        self.pic_url = 'http://112.96.28.245/login/loginpage'

        # 签到主页
        self.signin_url = 'http://112.96.28.245/citic/sign/view'
        # 点击签到
        self.signin_click_url = 'http://112.96.28.245/citic/sign/signin'
        # 已签到信息
        self.signin_info_url = 'http://112.96.28.245/citic/sign/signCount'

        # 红包主页
        self.redpacket_url = 'http://112.96.28.245/redPacket/FlowRedPacket'
        # 拆红包
        self.redpacket_click_url = 'http://112.96.28.245/redPacket/openRedPacket'
        # 当前信息
        self.curinfo_url = 'http://112.96.28.245/citic/home/account'
        # 表单数据
        self.login_data = {
            'logintype': 'passlogin',
            'url': '/login/indexpage',
            'mobile': '',
            'pwd': '',
            'imgcheckcode': '',
            'checkcode': '',
            'source': '',
            'campaign': '',
            'callback': '',
            'csrf': ''
        }
        # 浏览器模拟
        self.headers = {
            "Host": "112.96.28.245",
            "Referer": "http://112.96.28.245/login/loginPageActionForBusiness",
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/56.0.2924.87',
            'Connection': 'keep-alive'
        }

        # 创建一个session, 方便保存cookies
        self.session = requests.session()
        self.run()

    # 获取验证码
    def getimgcheckcode(self):

        r = self.session.get(self.pic_url, headers=self.headers)
        pic_base64 = str(r.text).replace('data:image/jpg;base64,', '')

        with open('yzm.jpg', 'wb') as pic:
            pic.write(base64.b64decode(pic_base64))

        imgcheckcode = input('  验证码: ')
        self.login_data['imgcheckcode'] = imgcheckcode
        with open('yzm.jpg', 'wb') as pic:
            pic.write(base64.b64decode(pic_base64))
        return imgcheckcode

    # 拆红包主函数
    def redpacket_click(self):
        self.session.get(self.redpacket_url, headers=self.headers)
        self.headers["Referer"] = 'http://112.96.28.245'
        r = self.session.get(self.redpacket_click_url, headers=self.headers)
        print('红包提示: {}'.format(r.json()['data']['descri']))

    # 首次登录
    def first_login(self, account, pwd):

        self.login_data['mobile'] = account

        self.login_data['pwd'] = pwd

        # 获取csrf
        # session = requests.session()
        r = self.session.get('http://112.96.28.245/citic/citiclogin', headers=self.headers)

        self.login_data['csrf'] = re.findall('id="csrf" value="(.*?)" /', r.text)[0]

        # 获取验证码
        imgcheckcode = self.getimgcheckcode()
        # 提交账号密码及验证码以登录
        self.session.post(self.login_url, data=self.login_data, headers=self.headers)
        while not self.login_status(account):
            # 获取验证码
            imgcheckcode = self.getimgcheckcode()
            # 获取csrf
            r = self.session.get(self.login_url, headers=self.headers)
            try:
                self.login_data['csrf'] = re.findall('id="csrf" value="(.*?)"', r.text)[0]
            except IndexError:
                continue
            # 再次 提交账号密码及验证码以登录
            self.session.post(self.login_url, data=self.login_data, headers=self.headers)
        print('登录提示: 登录成功!')
        os.rename('yzm.jpg', 'yzm/{}.jpg'.format(imgcheckcode))

    # 判断是否已经登录
    def login_status(self, account):
        r = self.session.get(self.index_url, headers=self.headers)

        if account in r.text:
            return True
        else:
            return False

    # 签到主函数
    def signin_click(self):
        self.session.get(self.signin_click_url, headers=self.headers)
        r = self.session.get(self.signin_info_url, headers=self.headers)
        if r.json()['data']['continuousNum'] == 7:
            print('签到提示: 成功签到, 获得50M流量')
        else:
            print('签到提示: 成功签到, 获得5M流量')

    def curinfo(self):
        r = self.session.get(self.curinfo_url, headers=self.headers)
        print('当前流量: {}M'.format(r.json()['data']['flow']))

    def run(self):
        di_acpw = eval(open('acpw.txt', 'r', encoding='gbk').read())
        nft = 1
        for account in di_acpw:
            name = di_acpw[account][0]
            pwd = di_acpw[account][1]
            print('\n--------------------------------------------------------')
            print('                正在读取第 {} 个用户!'.format(nft))
            print('--------------------------------------------------------\n')
            print('当前用户: {}\n手机号码: {}'.format(name, account))

            # 判断一起沃目录是否存在
            if not os.path.exists(os.getcwd() + '\\一起沃\\'):
                os.makedirs(os.getcwd() + '\\一起沃\\')
            cookies_name = os.getcwd() + '\\一起沃\\' + account

            # 更新cookies
            self.session.cookies = cookiejar.LWPCookieJar(filename=cookies_name)
            try:  # 尝试加载cookies
                self.session.cookies.load(ignore_discard=True)
            except:  # 无法加载cookies时,采用账号密码登录
                open(cookies_name, 'w+')

            while not self.login_status(account):
                self.first_login(account, pwd)

            try:
                # 签到
                self.signin_click()
                # 拆红包
                # redpacket_click()
                # 目前信息
                self.curinfo()
            except:
                self.first_login(account, pwd)
                # 签到
                self.signin_click()
                # 拆红包
                # redpacket_click()
                # 目前信息
                self.curinfo()

            # 保存cookies文件
            self.session.cookies.save()
            nft += 1


if __name__ == '__main__':
    Wo()
