

前言
---
title: Socket小总结(粗糙)
---
### 前言
Python 提供了两个基本的 socket 模块。
第一个是 Socket，它提供了标准的 BSD Sockets API。
第二个是 SocketServer， 它提供了服务器中心类，可以简化网络服务器的开发。
### Socket 类型
套接字格式：
socket(family,type[,protocal])
使用family: 地址族、type: 套接字类型、protocal: 协议编号（默认为0）来创建套接字
 | socket类型 | 描述 | 
| --- | --- | 
 | socket.AF_UNIX | 只能够用于单一的Unix系统进程间通信 | 
 | socket.AF_INET | 服务器之间网络通信 | 
 | socket.AF_INET6 | IPv6 | 
 | socket.SOCK_STREAM | 流式socket , for TCP | 
 | socket.SOCK_DGRAM | 数据报式socket , for UDP | 
 | socket.SOCK_RAW | 原始套接字，普通的套接字无法处理ICMP、IGMP等网络报文，而SOCK_RAW可以；其次，SOCK_RAW也可以处理特殊的IPv4报文；此外，利用原始套接字，可以通过IP_HDRINCL套接字选项由用户构造IP头。 | 
 | socket.SOCK_SEQPACKET | 可靠的连续数据包服务 | 
 | 创建TCP Socket | s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) | 
 | 创建UDP Socket | s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) | 
​
### Socket 函数
| 服务端socket函数 | 描述 |
| --- | --- | --- |
| s.bind(address) |将Socket绑定到地址, 在AF_INET下,以元组（host,port）的形式表示地址. | 
| s.listen(backlog) | 开始监听TCP传入连接。backlog指定在拒绝连接之前，操作系统可以挂起的**最大连接数量**。该值至少为1，大部分应用程序设为5就可以了。 |
| s.accept() | 接受TCP连接并返回（conn,address）,其中conn是新的Socket对象，可以用来接收和发送数据。address是连接客户端的地址。**阻塞模式, 一直等待连接的到来**。 | 
​
| 客户端socket函数 | 描述 |
| --- | --- | --- |
| s.connect(address) | 连接到address处的Socket。一般address的格式为元组（hostname,port），如果连接出错，返回socket.error错误。 | 
| s.connect_ex(adddress) | 功能与connect(address)相同，但是成功返回0，失败返回errno的值。 |
​
| 公共socket函数 | 描述 |
| --- | --- | --- |
| s.recv(bufsize[,flag]) | 接受TCP Socket的数据。数据以字符串形式返回，bufsize指定要接收的最大数据量。flag提供有关消息的其他信息，通常可以忽略。**阻塞模式, 一直等待消息的到来** 。| 
 
[3:6]行数：102 长度：3884
Socket小总结(粗糙)
Selenium与requests相互更换cookies
笔记 - Python核心编程三
Python Selenium 自动化
编码问题
计算机网络
leetcode
笔记 - MySql
Jsp笔记
L - 09-正则表达式.md
笔记 - 正则
笔记 - linux
 小书匠
 新建
 保存
 另存为
Socket小总结(粗糙)
HTML
<h1 class="story_title">Socket小总结(粗糙)</h1>
<div class="line_item line_item_display xiaoshujiang_element"
data-line="3"></div>
<div class="xiaoshujiang_element xsj_anchor">
  <a name="e5898de8a880_1" class="blank_anchor_name"></a>
  <a id="e5898de8a880_1" class="blank_anchor_id"></a>
  <a name="前言" class="blank_anchor_name"></a>
  <a id="前言" class="blank_anchor_id"></a>
</div>
<h3>前言</h3>
<div class="line_item line_item_display xiaoshujiang_element" data-line="4"></div>
<p>Python 提供了两个基本的 socket 模块。
  <br> 第一个是 Socket，它提供了标准的 BSD Sockets API。
  <br> 第二个是 SocketServer， 它提供了服务器中心类，可以简化网络服务器的开发。</p>
<div class="line_item line_item_display xiaoshujiang_element" data-line="7"></div>
<div class="xiaoshujiang_element xsj_anchor">
  <a name="socket20e7b1bbe59e8b_2" class="blank_anchor_name"></a>
  <a id="socket20e7b1bbe59e8b_2" class="blank_anchor_id"></a>
  <a name="socket-类型" class="blank_anchor_name"></a>
  <a id="socket-类型" class="blank_anchor_id"></a>
</div>
<h3>Socket 类型</h3>
<div class="line_item line_item_display xiaoshujiang_element" data-line="8"></div>
<p>套接字格式：
  <br> socket(family,type[,protocal])
  <br> 使用family: 地址族、type: 套接字类型、protocal: 协议编号（默认为0）来创建套接字</p>
<div class="line_item line_item_display xiaoshujiang_element" data-line="11"></div>
<table class="table table-striped table-celled">
  <thead>
    <tr>
      <th>socket类型</th>
      <th>描述</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>socket.AF_UNIX</td>
      <td>只能够用于单一的Unix系统进程间通信</td>
    </tr>
    <tr>
      <td>socket.AF_INET</td>
      <td>服务器之间网络通信</td>
    </tr>
    <tr>
      <td>socket.AF_INET6</td>
      <td>IPv6</td>
    </tr>
    <tr>
      <td>socket.SOCK_STREAM</td>
      <td>流式socket , for TCP</td>
    </tr>
    <tr>
      <td>socket.SOCK_DGRAM</td>
      <td>数据报式socket , for UDP</td>
    </tr>
    <tr>
      <td>socket.SOCK_RAW</td>
      <td>原始套接字，普通的套接字无法处理ICMP、IGMP等网络报文，而SOCK_RAW可以；其次，SOCK_RAW也可以处理特殊的IPv4报文；此外，利用原始套接字，可以通过IP_HDRINCL套接字选项由用户构造IP头。</td>
    </tr>
    <tr>
      <td>socket.SOCK_SEQPACKET</td>
      <td>可靠的连续数据包服务</td>
    </tr>
    <tr>
      <td>创建TCP Socket</td>
      <td>s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)</td>
    </tr>
    <tr>
      <td>创建UDP Socket</td>
      <td>s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)</td>
    </tr>
  </tbody>
</table>
<div class="line_item line_item_display xiaoshujiang_element" data-line="23"></div>
<div class="xiaoshujiang_element xsj_anchor">
  <a name="socket20e587bde695b0_3" class="blank_anchor_name"></a>
  <a id="socket20e587bde695b0_3" class="blank_anchor_id"></a>
  <a name="socket-函数" class="blank_anchor_name"></a>
  <a id="socket-函数" class="blank_anchor_id"></a>
</div>
<h3>Socket 函数</h3>
<div class="line_item line_item_display xiaoshujiang_element" data-line="24"></div>
<table class="table table-striped table-celled">
  <thead>
    <tr>
      <th>服务端socket函数</th>
      <th>描述</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>s.bind(address)</td>
      <td>将Socket绑定到地址, 在AF_INET下,以元组（host,port）的形式表示地址.</td>
    </tr>
    <tr>
      <td>s.listen(backlog)</td>
      <td>开始监听TCP传入连接。backlog指定在拒绝连接之前，操作系统可以挂起的
        <strong>最大连接数量</strong>。该值至少为1，大部分应用程序设为5就可以了。</td>
    </tr>
    <tr>
      <td>s.accept()</td>
      <td>接受TCP连接并返回（conn,address）,其中conn是新的Socket对象，可以用来接收和发送数据。address是连接客户端的地址。
        <strong>阻塞模式, 一直等待连接的到来</strong>。</td>
    </tr>
  </tbody>
</table>
<div class="line_item line_item_display xiaoshujiang_element" data-line="30"></div>
<table class="table table-striped table-celled">
  <thead>
    <tr>
      <th>客户端socket函数</th>
      <th>描述</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>s.connect(address)</td>
      <td>连接到address处的Socket。一般address的格式为元组（hostname,port），如果连接出错，返回socket.error错误。</td>
    </tr>
    <tr>
      <td>s.connect_ex(adddress)</td>
      <td>功能与connect(address)相同，但是成功返回0，失败返回errno的值。</td>
    </tr>
  </tbody>
</table>
<div class="line_item line_item_display xiaoshujiang_element" data-line="35"></div>
<table class="table table-striped table-celled">
  <thead>
    <tr>
      <th>公共socket函数</th>
      <th>描述</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>s.recv(bufsize[,flag])</td>
      <td>接受TCP Socket的数据。数据以字符串形式返回，bufsize指定要接收的最大数据量。flag提供有关消息的其他信息，通常可以忽略。
        <strong>阻塞模式, 一直等待消息的到来</strong> 。</td>
    </tr>
    <tr>
      <td>s.send(string[,flag])</td>
      <td>
        <strong>发送TCP数据</strong>。将string中的数据发送到连接的Socket。返回值是要发送的字节数量，该数量可能小于string的字节大小。</td>
    </tr>
    <tr>
      <td>s.sendall(string[,flag])</td>
      <td>
        <strong>完整发送TCP数据</strong>。将string中的数据发送到连接的socket，但在返回之前会尝试发送所有数据。成功返回None，失败则抛出异常。
        <strong>此函数, 不是用于将信息发至所有已连接的主机</strong> 。</td>
    </tr>
    <tr>
      <td>s.recvfrom(bufsize[.flag])</td>
      <td>接受UDP Socket的数据。与recv()类似，但返回值是（data,address）。其中data是包含接收数据的字符串，address是发送数据的Socket地址。</td>
    </tr>
    <tr>
      <td>s.sendto(string[,flag],address)</td>
      <td>发送
        <strong>UDP</strong>数据。将数据发送到套接字，address是形式为（ipaddr，port）的元组，指定远程地址。返回值是发送的字节数。
        <strong>用于向特定用户发送信息, 使用此函数, 需要创建UDP socket</strong>。</td>
    </tr>
    <tr>
      <td>s.close()</td>
      <td>关闭Socket。</td>
    </tr>
    <tr>
      <td>s.getpeername()</td>
      <td>返回连接Socket的远程地址。返回值通常是元组（ipaddr,port）。</td>
    </tr>
    <tr>
      <td>s.getsockname()</td>
      <td>返回Socket自己的地址。通常是一个元组(ipaddr,port)</td>
    </tr>
    <tr>
      <td>s.setsockopt(level,optname,value)</td>
      <td>设置给定Socket选项的值。</td>
    </tr>
    <tr>
      <td>s.getsockopt(level,optname[.buflen])</td>
      <td>返回Socket选项的值。</td>
    </tr>
    <tr>
      <td>s.settimeout(timeout)</td>
      <td>设置Socket操作的超时期，timeout是一个浮点数，单位是秒。值为None表示没有超时期。一般，超时期应该在刚创建Socket时设置，因为它们可能用于连接的操作（如connect()）</td>
    </tr>
    <tr>
      <td>s.gettimeout()</td>
      <td>返回当前超时期的值，单位是秒，如果没有设置超时期，则返回None。</td>
    </tr>
    <tr>
      <td>s.fileno()</td>
      <td>返回套接字的文件描述符。</td>
    </tr>
    <tr>
      <td>s.setblocking(flag)</td>
      <td>如果flag为0，则将套接字设为非阻塞模式，否则将套接字设为阻塞模式（默认值）。非阻塞模式下，如果调用recv()没有发现任何数据，或send()调用无法立即发送数据，那么将引起socket.error异常。</td>
    </tr>
    <tr>
      <td>s.makefile()</td>
      <td>创建一个与该Socket相关联的文件</td>
    </tr>
  </tbody>
</table>
<div class="line_item line_item_display xiaoshujiang_element" data-line="53"></div>
<p>注意点:
  <br> 1）TCP发送数据时，已建立好TCP连接，所以不需要指定地址。UDP是面向无连接的，每次发送要指定是发给谁。
  <br> 2）服务端与客户端不能直接发送列表，元组，字典。需要字符串化repr(data)。
</p>
<div class="line_item line_item_display xiaoshujiang_element" data-line="58"></div>
<div class="xiaoshujiang_element xsj_anchor">
  <a name="sockete7bc96e7a88be6809de8b7af_4" class="blank_anchor_name"></a>
  <a id="sockete7bc96e7a88be6809de8b7af_4" class="blank_anchor_id"></a>
  <a name="socket编程思路" class="blank_anchor_name"></a>
  <a id="socket编程思路" class="blank_anchor_id"></a>
</div>
<h3>socket编程思路</h3>
<div class="line_item line_item_display xiaoshujiang_element" data-line="59"></div>
<p>TCP服务端：
  <br> 1 创建Socket，绑定Socket到本地IP与端口
  <br> socket.socket(socket.AF_INET,socket.SOCK_STREAM) , s.bind()
  <br> 2 开始监听连接
  <br> s.listen()
  <br> 3 进入循环，不断接受客户端的连接请求
  <br> s.accept()
  <br> 4 然后接收传来的数据，并发送给对方数据
  <br> s.recv() , s.sendall()
  <br> 5 传输完毕后，关闭Socket
  <br> s.close()
</p>
<div class="line_item line_item_display xiaoshujiang_element" data-line="71"></div>
<p>TCP客户端:
  <br> 1 创建Socket，连接远端地址
  <br> socket.socket(socket.AF_INET,socket.SOCK_STREAM) , s.connect()
  <br> 2 连接后发送数据和接收数据
  <br> s.sendall(), s.recv()
  <br> 3 传输完毕后，关闭Socket
  <br> s.close()
</p>
<div class="line_item line_item_display xiaoshujiang_element" data-line="79"></div>
<div class="xiaoshujiang_element xsj_anchor">
  <a name="e585b6e5ae83_5" class="blank_anchor_name"></a>
  <a id="e585b6e5ae83_5" class="blank_anchor_id"></a>
  <a name="其它" class="blank_anchor_name"></a>
  <a id="其它" class="blank_anchor_id"></a>
</div>
<h3>其它</h3>
<div class="line_item line_item_display xiaoshujiang_element" data-line="80"></div>
<div class="xiaoshujiang_element xsj_anchor">
  <a name="accepte587bde695b0_6" class="blank_anchor_name"></a>
  <a id="accepte587bde695b0_6" class="blank_anchor_id"></a>
  <a name="accept函数" class="blank_anchor_name"></a>
  <a id="accept函数" class="blank_anchor_id"></a>
</div>
<h4>accept函数</h4>
<div class="line_item line_item_display xiaoshujiang_element" data-line="81"></div>
<p>主服务器accept接受到客户机的connect连接后, 会返回一个单独的客户端与请求的客户机进行通信, 主服务器则回到原状态等待连接.
  <br> 如同接线员, 帮客户借入电话, 但不与客户通话.</p>
<div class="line_item line_item_display xiaoshujiang_element" data-line="84"></div>
<div class="xiaoshujiang_element xsj_anchor">
  <a name="connecte587bde695b0_7" class="blank_anchor_name"></a>
  <a id="connecte587bde695b0_7" class="blank_anchor_id"></a>
  <a name="connect函数" class="blank_anchor_name"></a>
  <a id="connect函数" class="blank_anchor_id"></a>
</div>
<h4>connect函数</h4>
<div class="line_item line_item_display xiaoshujiang_element" data-line="85"></div>
<p>connect函数, 仅用于TCP面向连接通讯</p>
<div class="line_item line_item_display xiaoshujiang_element" data-line="87"></div>
<div class="xiaoshujiang_element xsj_anchor">
  <a name="e6849fe58f97_8" class="blank_anchor_name"></a>
  <a id="e6849fe58f97_8" class="blank_anchor_id"></a>
  <a name="感受" class="blank_anchor_name"></a>
  <a id="感受" class="blank_anchor_id"></a>
</div>
<h4>感受</h4>
<div class="line_item line_item_display xiaoshujiang_element" data-line="88"></div>
<p>TCP面向连接
  <br> 客户端得先connect到服务端, 取得服务端返回的一个socket连接对象, 通过这个对象使用send或sendall向服务端发送信息, 通过recv接受信息;
  没有这个连接对象, 就无法与服务端进行通信, 而且, 这个连接对象只能进行一对一通信, 即只能允许服务端与当前客户端进行通信;
  <br> 服务端得先绑定一个(host,port), 通过accept获取能与客户端进行通信的连接对象; 其它同上;
  <br> 需要注意的是, connect与accept都是阻塞模式, 就是说, 它会一直等, 直到服务端有了客户端的connect请求或客户端有了服务端的accept请求,
  才会执行其后面的语句; connect与accept都是成对出现;</p>
<div class="line_item line_item_display xiaoshujiang_element" data-line="93"></div>
<p>UDP无连接
  <br> 还没仔细折腾过呢..
</p>
<div class="line_item line_item_display xiaoshujiang_element" data-line="97"></div>
<div class="xiaoshujiang_element xsj_anchor">
  <a name="e58f82e88083e69da5e6ba90_9" class="blank_anchor_name"></a>
  <a id="e58f82e88083e69da5e6ba90_9" class="blank_anchor_id"></a>
  <a name="参考来源" class="blank_anchor_name"></a>
  <a id="参考来源" class="blank_anchor_id"></a>
</div>
<h3>参考/来源</h3>
<div class="line_item line_item_display xiaoshujiang_element" data-line="99"></div>
<p><a href="http://blog.51cto.com/yangrong/1339593">python socket编程详细介绍-功夫猫-51CTO博客</a>
  <br>
  <a href="https://www.cnblogs.com/fanweibin/p/5053328.html">Python之socket（套接字） - 永远不会懂 - 博客园</a>
  <br>
  <a href="https://www.cnblogs.com/aylin/p/5572104.html">python之socket编程 - 张岩林 - 博客园</a>
</p>
