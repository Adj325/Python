import re
import os
import execjs
import requests
from urllib import parse

js_sigu = '''
function getSigu(message){
	var key_base = 'contentWindowHig';
	var iv_base = 'contentDocuments';
	var key_base_md5 = CryptoJS.MD5(key_base);
	var key_base_md5_utf8 = CryptoJS.enc.Utf8.parse(key_base_md5);
	var iv_base_utf8 = CryptoJS.enc.Utf8.parse(iv_base);
	var message_encrypted = CryptoJS.AES.encrypt(message, key_base_md5_utf8, {
		'iv': iv_base_utf8,
		'mode': CryptoJS.mode.CBC,
		'padding': CryptoJS.pad.ZeroPadding
	});
	return message_encrypted.toString();
}

'''

with open("sign.js") as f:
    jsData = f.read()
    sign_ctx = execjs.compile(jsData)

with open("crypto-js.js") as f:
    jsData = f.read()
    sigu_ctx = execjs.compile(jsData+js_sigu)

def getSign(text):
    return sign_ctx.call("sign", text)

def getSigu(text):
    return sigu_ctx.call("getSigu", text)

def getHmd5Str(html):
    string = re.findall('eval\("(.*?)"\);', html)[0]
    string = string.split('\\')[1:]
    s = ''
    for i in string[17:49]:
        s += chr(int('0'+i, 16))
    return s

def getSiguStr(html):
    return re.findall('sigu\("(\d+)"\)', html)[0]

def download_m3u8(url, name):
    print('\nm3u8:', url)
    download_path = os.getcwd() + os.sep +"download"
    file_name = download_path + os.sep + name + '.ts'
    if not os.path.exists(download_path):
        os.mkdir(download_path)
    all_content = requests.get(url).text # 获取M3U8的文件内容
    file_line = all_content.split("\n") # 读取文件里的每一行
    for index, line in enumerate(file_line):
        if "http" in line:
            res = requests.get(line)
            with open(file_name, 'ab') as f:
                f.write(res.content)
                f.flush()
    else:
        print("提示: {} 下载完成".format(name))

def download_mp4(url_list, name):
    print('\nurl_list_size:', len(url_list))
    download_path = os.getcwd() + os.sep +"download"
    file_name = download_path + os.sep + name + '_{}.mp4'
    if not os.path.exists(download_path):
        os.mkdir(download_path)
    for index, url in enumerate(url_list):
        res = requests.get(url)
        with open(file_name.format(index+1), 'wb') as f:
            f.write(res.content)
            f.flush()
        print("提示: {}_{}.mp4 下载完成".format(name, index+1))
    else:
        print("提示: {} 下载完成".format(name))

host = 'http://api.bbbbbb.me'
api_url = 'http://api.bbbbbb.me/yunjx{}/api.php'
#video_url = 'https://www.iqiyi.com/v_19rqr832ok.html'
video_url = input('电影链接: ')
name = input('电影名称: ')
base_url = 'http://api.bbbbbb.me/yunjx/?url='
base_url += video_url
api_num = ''
while True:
    data = {
        'id': video_url,
        'type':'auto',
        'siteuser':'',
        'md5':'',
        'hd':'',
        'lg':''
    }
    print('video_url:', video_url)
    print('base_url:', base_url)
    if 'sigu' in html:
        sigu = getSiguStr(html)
        data['key'] = getSigu(sigu)
    hmd5 = getHmd5Str(html)
    data['md5'] = getSign(hmd5)

    r = requests.post(api_url.format(api_num), data=data)
    print('result:', r.json())
    if r.json()['ext'] == 'm3u8':
        url_encoded = r.json()['url']
        url = parse.unquote(url_encoded)
        download_m3u8(url, name)
        break
    else if r.json()['ext'] == 'xml':
        r = requests.get(r.json()['url'])
        url_list = re.findall('<file><!\[CDATA\[(.*?)\]\]></file>', r.text)
        download_mp4(url_list, name)
        break
    else:
        video_url = 'http' + r.json()['url'].split('=http')[-1]
        if 'http' != r.json()['url'][:4:]:
            base_url = host + r.json()['url']
        else:
            base_url = r.json()['url']
    api_num = ''
    for i in r.json()['url'].split('/'):
        if 'yunjx' in i:
            api_num = i[5::]
    print()
