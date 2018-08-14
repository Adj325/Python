import os
import re
import base64
import requests

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'www.nokiacn.net',
    'Referer': 'http://www.nokiacn.net/gaoxiao/turanxihuanni/73592.html',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.56 Safari/537.36'
}


class QingTianManHua:

    @staticmethod
    def get(url):
        r = requests.get(url=url, headers=headers)
        r.encoding = 'utf-8'
        return r

    def crawl(self, main_url, start=0):
        main_rep = self.get(main_url)

        manhua_name = re.findall('<h1>(.*?)</h1>', main_rep.text)[0]
        # 以漫画名创建目录
        if not os.path.exists(manhua_name):
            os.mkdir(manhua_name)

        print('漫画名：{}'.format(manhua_name))

        # 提取章节名及其url
        result_list = re.findall('<li><a href="(.*?)" target="_blank"><p>(.*?)</p><i></i></a></li>', main_rep.text)
        result_list = result_list[start::]
        print(len(result_list))
        # 遍历解析所有章节
        for chapter_url, chapter_name in result_list:
            chapter_id = re.findall('(\d+)', chapter_name)[0]
            # 补全章节链接
            chapter_url = 'http://www.nokiacn.net' + chapter_url
            chapter_rep = self.get(chapter_url)

            # 提取 经过base64加密后的图片url
            qTcms_S_m_murl_e = re.findall('qTcms_S_m_murl_e="(.*?)"', chapter_rep.text)[0]
            qTcms_S_m_murl = base64.b64decode(qTcms_S_m_murl_e).decode()
            images_url = qTcms_S_m_murl.split('$qingtiandy$')

            # 以章节名创建目录
            chapter_path = manhua_name + '/' + '第{0:03d}话'.format(int(chapter_id))
            if not os.path.exists(chapter_path):
                os.mkdir(chapter_path)

            # 下载当前章节图片到本地
            for image_id, image_url in enumerate(images_url):
                image_url = 'http://n.aiwenwo.net:55888' + image_url
                image_rep = requests.get(image_url)

                if len(image_rep.content) < 4 * 1024:
                    print('下载{}时出现问题！'.format(image_url))

                with open('{0}/{1:03d}.jpg'.format(chapter_path, image_id), 'wb') as img:
                    img.write(image_rep.content)

            print('\n提示：{}, 共{}张图片!'.format(chapter_name, len(images_url)))
        else:
            print('漫画"{}"已爬取完毕！'.format(manhua_name))


manhua_url = 'http://www.nokiacn.net/gaoxiao/turanxihuanni/'
# 上次56话
QingTianManHua().crawl(manhua_url, 0)
