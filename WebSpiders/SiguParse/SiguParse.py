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
    sigu_ctx = execjs.compile(jsData + js_sigu)


def getSign(text):
    return sign_ctx.call("sign", text)


def getSigu(text):
    return sigu_ctx.call("getSigu", text)


def getHmd5Str(html):
    string = re.findall('eval\("(.*?)"\);', html)[0]
    string = string.split('\\')[1:]
    s = ''
    for i in string[17:49]:
        s += chr(int('0' + i, 16))
    return s


def getSiguStr(html):
    return re.findall('"key":sigu\("(\d+)"\)', html)[0]


def download_m3u8(url, name):
    print('\nm3u8: {}'.format(url))
    domain = re.findall("https?://.*?/", url)[0]
    print('domain: {}\n'.format(domain))
    download_path = os.getcwd() + os.sep + "download"
    file_name = download_path + os.sep + name + '.ts'
    if not os.path.exists(download_path):
        os.mkdir(download_path)
    all_content = requests.get(url).text  # 获取M3U8的文件内容

    file_line = all_content.split("\n")  # 读取文件里的每一行
    count = 1
    for line in file_line:
        if '.m3u8' in line:
            print('forward:', domain + line[1::])
            download_m3u8(domain + line[1::], name)
            return
        elif ".ts" in line:
            if 'http' not in line:
                line = domain + line[1::]
            print('{0:05d}: {1}\n'.format(count, line))
            count += 1
            res = requests.get(line)
            with open(file_name, 'ab') as f:
                f.write(res.content)
                f.flush()
    else:
        print("提示: {} 下载完成".format(name))
        return True


def download_mp4(url_list, name):
    download_path = os.getcwd() + os.sep + "download"
    if not os.path.exists(download_path):
        os.mkdir(download_path)

    if len(url_list) == 1:
        file_name = download_path + os.sep + name + '.mp4'
        res = requests.get(url_list[0])
        if len(res.content) < 1050429:
            return False
        with open(file_name, 'wb') as f:
            f.write(res.content)
            f.flush()
        print("提示: {} 下载完成".format(name))
        return True

    print('\nurl_list_size:', len(url_list))
    file_name = download_path + os.sep + name + '_{}.mp4'
    for index, url in enumerate(url_list):
        res = requests.get(url)
        with open(file_name.format(index + 1), 'wb') as f:
            f.write(res.content)
            f.flush()
        print("提示: {}_{}.mp4 下载完成".format(name, index + 1))
    else:
        print("提示: {} 下载完成".format(name))
    return True


def process(video_url, base_url_list):
    for base_url in base_url_list:
        print('base_url:', base_url)
        base_url += video_url
        print('video_url:', video_url)
        # 解决 frame 识别
        headers = {
            'referer': base_url,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
        r = requests.get(base_url, headers=headers)
        if len(r.text) < 10000:
            print('\nstatus: {} invalid'.format(base_url))
            continue
        else:
            print('\nstatus: {} valid'.format(base_url))

        data = {
            'id': video_url,
            'type': 'auto',
            'siteuser': '',
            'md5': '',
            'hd': '',
            'lg': ''
        }
        # 获取sigu
        if '"key":sigu' in r.text:
            sigu = getSiguStr(r.text)
            data['key'] = getSigu(sigu)
        # 获取sign
        hmd5 = getHmd5Str(r.text)
        data['md5'] = getSign(hmd5)

        headers = {
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'referer': base_url,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
        print('\ndata: {}'.format(data))
        api_url = re.findall('https://.*?/.*?/', base_url)[0] + 'api.php'
        r = requests.post(api_url, data=data, headers=headers)
        if r.status_code == 200:
            if 'meg' in r.json():
                # print('result: {}'.format(r.json()['meg']))
                continue
            elif 'ext' in r.json():
                print('\napi_url: {}'.format(api_url))
                print('result: {}\n'.format(r.text))

                if r.json()['ext'] == 'm3u8' or 'm3u8' in r.json()['url']:
                    print('type: m3u8')
                    url_encoded = r.json()['url']
                    url = parse.unquote(url_encoded)

                    if download_m3u8(url, name):
                        return True
                    else:
                        continue
                elif r.json()['ext'] == 'xml':
                    print('type: xml')
                    r = requests.get(r.json()['url'])
                    url_list = re.findall('<file><!\[CDATA\[(.*?)\]\]></file>', r.text)
                    if download_mp4(url_list, name):
                        return True
                    else:
                        continue
                elif r.json()['ext'] == 'mp4':
                    print('type: mp4')
                    if download_mp4([r.json()['url']], name):
                        return True
                    else:
                        continue
                elif r.json()['ext'] == 'link':
                    print('type: link')
                    video_url = 'http' + r.json()['url'].split('=http')[-1]
                    if host in r.json()['url']:
                        _base_url = r.json()['url'].split('=http')[0]
                        get_video(video_url, _base_url)
                    else:
                        print('redirect: {}\n'.format(video_url))
                        if get_video(video_url):
                            return True
                        else:
                            continue


def get_video(video_url, base_url=None):
    if base_url is None:
        base_url_list = base_urls[::]
    else:
        base_url_list = [base_url]
    return process(video_url, base_url_list)


print('提示: execjs 与 Node js 不兼容\n')

host = 'api.sigujx.com'
api_url = 'https://{}/yunjx{}/api.php'
video_url = 'https://www.iqiyi.com/v_19rr3knsh8.html'
name = '一吻定情'

# video_url = input('电影链接: ').strip(' ')
# name = input('电影名称: ').strip(' ')

video_url = 'https://www.iqiyi.com/v_19rr8cycvc.html'
name = '寻梦环游记'
base_urls = [
    'https://{}/yunjxss/index.php?id='.format(host),
    'https://{}/yunjx/?url='.format(host),
    'https://{}/yunjx1/?url='.format(host),
    'https://{}/yunjx2/?url='.format(host),
    'https://{}/yunjx3/?url='.format(host),
    'https://{}/yunjx4/?url='.format(host),
    'https://{}/yunjx5/?url='.format(host),
    'https://{}/?url='.format(host),
    'https://{}/v.php?url='.format(host)]
get_video(video_url)
