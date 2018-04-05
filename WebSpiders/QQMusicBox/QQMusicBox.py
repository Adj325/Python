import os
import time
import requests
from flask import Flask, request, make_response

class QQMusicBox:
    def __init__(self):
        self.headers = {
            "Host": "soso.music.qq.com",
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87'}
        self.result = []
        c = input('本地: 直接回车   flask: f\n选择: ')
        if c == 'f':
            self.flask()
        else:
            self.local()

    # flask模式
    def flask(self):
        app = Flask(__name__)

        @app.route("/getsong", methods=["POST", "GET"])
        def ajax():
            #args = request.args
            #values = request.values
            word = request.values.get("word")
            if word == '':
                word = "青花瓷"

            p = request.values.get("p")
            if p == '':
                p = "1"

            check = request.values.get("check")
            if check == '':
                check = "no"

            print(word, p, check)
            res_song = self.getSonogs(word, p, check)
            rst = make_response(str(res_song))
            rst.headers['Access-Control-Allow-Origin'] = '*'
            return rst
        os.system('start flask.html')
        app.run(port=325)

    # 对下载链接url, 进行状态码的获取
    def getStatusCode(self, url):
        '''
        try:
            url = url.replace('/', '%2F').replace('&', '%3F').replace('=', '%3D')
            headers = {
            "Host": "pl.soshoulu.com",
            'Referer':'http://pl.soshoulu.com/webspeed.aspx',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87'
            }
            statusCodeUrl = 'http://pl.soshoulu.com/ajax/shoulu.ashx?_type=webspeed&url={}&px=1'.format(url)
            r = requests.get(statusCodeUrl, headers=headers, timeout=1)
            statuscode =  r.text.split('$')[0]
            return statuscode
        except:
            return ''
        '''
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87'
            }
            r = requests.get(url, headers=headers, stream=True, timeout=0.4)
            return str(r.status_code)
        except:
            return ''


    # 本地模式
    def local(self):
        print('\n关闭程序: CTRL+C')
        os.system('start local.html')
        while True:
            word = input('关键词: ')
            li = []
            # 最多获取10页
            for p in range(1, 11):
                res_song = self.getSonogs(word, p, 'yes')
                li += res_song
                # i += 1
                with open('data.js', 'w', encoding='utf-8') as f:
                    f.write('var title = "{}";\r\n'.format(word))
                    f.write('var songData=' + str(li) + ';')

    # 获取歌曲
    # check: 'yes'-检测, '其它'-不检测
    def getSonogs(self, word, p, check='yes'):
        data = {
            'aggr': '0',
            'catZhida': '0',
            'lossless': '1',
            'sem': '1',
            'w': '',  # 关键词
            'n': '30',  # 每页的数量. 最大是30
            't': '0',
            'p': '1',  # 页码
            'remoteplace': 'wo.shi.nidaye',
            'g_tk': '5381',
            'loginUin': '0',
            'hostUin': '0',
            'format': 'json',
            'inCharset': 'GB2312',
            'outCharset': 'utf-8',
            'notice': '0',
            'platform': 'yqq',
            'needNewCode': '0'
        }
        res_song = []
        session = requests.session()
        data['p'] = str(p)
        data['w'] = word
        dataStr = '&'.join('='.join(i) for i in data.items())

        # 设置host, 用于获取搜索结果
        self.headers['Host'] = 'soso.music.qq.com'
        r = session.get('http://soso.music.qq.com/fcgi-bin/search_cp?'+dataStr, headers=self.headers, timeout=2)
        try:
            li = r.json()['data']['song']['list']
        except:
            return
        # 变换host, 用于获取vkey
        self.headers['Host'] = 'base.music.qq.com'
        print()
        for i, v in enumerate(li):
            time.sleep(0.2)
            #print('{0:03d}: {1} - {2}, 专辑: {3}'.format(i+1, v['singer'][0]['name'], v['songname'], v['albumname']))
            guid = v['docid']
            songmid = v['songmid']
            try:
                r = session.get('http://base.music.qq.com/fcgi-bin/fcg_musicexpress.fcg?json=3&guid={}'.format(guid), headers=self.headers, timeout=1)
            except:
                continue
            vkey = eval(r.text[13:-2:])['key']

            flac_url = 'http://ws.stream.qqmusic.qq.com/F000{}.flac?vkey={}&guid={}&fromtag=53'.format(songmid, vkey, guid)
            ape_url = 'http://ws.stream.qqmusic.qq.com/A000{}.ape?vkey={}&guid={}&fromtag=53'.format(songmid, vkey, guid)
            mp3128_url = 'http://ws.stream.qqmusic.qq.com/M500{}.mp3?vkey={}&guid={}&fromtag=53'.format(songmid, vkey, guid)
            mp3320_url = 'http://ws.stream.qqmusic.qq.com/M800{}.mp3?vkey={}&guid={}&fromtag=53'.format(songmid, vkey, guid)

            song = {'singer':v['singer'][0]['name'], 'songname':v['songname'], 'albumname':v['albumname']}

            if check == 'yes' and self.getStatusCode(flac_url) != '200':
                pass
            else:
                song['flac'] = flac_url

            if check == 'yes' and  self.getStatusCode(ape_url) != '200':
                pass
            else:
                song['ape'] = ape_url

            if check == 'yes' and  self.getStatusCode(mp3320_url) != '200':
                pass
            else:
                song['mp3320'] = mp3320_url

            if check == 'yes' and  self.getStatusCode(mp3128_url) != '200':
                pass
            else:
                song['mp3128'] = mp3128_url
            res_song.append(song)
        #print(res_song)
        return res_song

QQMusicBox()
