### 安装库
安装PIL、pytesseract、tesseract-ocr
PIL的安装中, 也许装64bit Python的电脑, 得安装32bit的wheel

pytesseract, 我直接pip就安装就成功了

tesseract-ocr, pip 安装失败, [Python 使用mingw构建第三方库 Unable to find vcvarsall.bat错误解决方法](https://blog.csdn.net/huobanjishijian/article/details/51915206)

百度后, 叫我下mingw64, 找了一会找不到就换别的解决方法了

最后, 直接下载tesseract-ocr: [Windows环境安装tesseract-ocr 4.00并配置环境变量](https://www.cnblogs.com/jianqingwang/p/6978724.html)

然后, 运行时碰到错误: [windows下pytesseract识别验证码遇到的WindowsError: [Error 2] 的解决方法](https://blog.csdn.net/bigzhao_25/article/details/52350781)

### 代码

``` python
import pytesseract
from PIL import Image
image = Image.open('yzm.jpg')
code = pytesseract.image_to_string(image)
print(code)
```

### 其它
往17沃签到工具加了识别代码, 但是用户体验极差, 识别效果非常低, 字符都交叉了.

也试过二值化, 但效果还是不好, 得用别的算法去训练数据.

所以只能先停下了, 这次算体验体验了.
