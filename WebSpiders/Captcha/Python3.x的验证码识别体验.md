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

### 搭配机器学习进行识别 2018-4-4
参考帖子: [机器学习之验证码识别](https://blog.csdn.net/alis_xt/article/details/65627303)

跟着这帖子弄好一段时间, 折腾的是别的网站

最后, 成功倒是成功了.

可是过程中, 遇到了很多问题!

numpy, pillow对我来说, 还是不够熟悉, 机器学习相关的库更是第一次使用!

预分类那块...就很尴尬了.

切割出来的单字符, pytesseract识别不了!

目前, 我也不知道为什么.

由于那网站的验证码字符种类不多, 我最终选择手动分类了下!

最后能成功识别了, 体验还是很良好的!

就是不知道为啥识别出来而已...还得好好学习.

由于某种原因, 不附上自己根据上面那帖子ctrl+c, ctrl+v出来的代码
