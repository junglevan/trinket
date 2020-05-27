'''
#七层网络模型#之4_Transport Layer:TCP & UDP
共同点:
ADDR(IP,port)
    IP可以选择三种类型:
        1-0.0.0.0-表示来者不拒,且访问本目标地址形式不限
        2-127.0.0.1-表示仅授权本人, 访问本目标地址仅通过回环(0.0.0.0/127.0.0.1)
        3-*私网地址-表示仅授权此私网IP,访问本目标地址仅通过此私网地址
    port:(0,2**16-1(65535)) 建议>8000绕开一些专属PORT 我的阿里云安全组为聊天室项目设置了TCP 46320-46330; UDP 12380-12390
不能重复绑定地址,收发listen等动作时如本身无绑定地址则默认绑定('0.0.0.0',随机分配的端口)(信息记录在socket对象laddr中)
不能既listen又connect
socket关闭的时后,文件描述符fd会变成-1
  e.g. <socket.socket [closed] fd=-1, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0>

不同:
UDP两端可以平等地互相盲发消息,若当时的ADDR不存在,则消息丢失(客户端和服务端几乎不重要了);
TCP则要先保证connect成功,之后,客户端和服务端不重要
如果连不上服务端, 客户端Connection refused或者卡住(但这个时候服务端再listen似乎并没有用);
connect阻塞或完成后, laddr会变成内网IP,在连结状态下(断开后则相应无)会有raddr是连结方的外网IP
e.g. 一端<socket.socket fd=12, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('192.168.1.136', 57346), raddr=('47.111.237.250', 46329)> & 另一端<socket.socket fd=14, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('172.16.77.214', 46329), raddr=('113.215.186.206', 57346)>  (其中sockfd.family/type/proto可访问 fd/laddr/raddr不可访问,#**dir(socket)#)
任意一端退出时,每次收到的消息成为b"",第二次发送的消息触发BrokenPipeError(但实际报错似乎有1秒不到的延时或许为了对应网络不稳定)

*私网地址(其他都是外网): 
    属于a类)10.0.0.0~10.255.255.255
    属于b类)172.16.0.0~172.31.255.255
    属于c类)192.168.0.0~192.168.255.255
**dir(socket): #socket作为一个类
    ['settimeout'(设置accept和recv的timeouterror的秒数,None则不会timeout),......]
'''

#tcp_server
from socket import *

sockfd=socket()
sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR,1) #立即回收端口,常用于测试
sockfd.bind(('0.0.0.0',12306))
sockfd.listen()
c,a=sockfd.accept() #阻塞函数,得到c代理<socket_socked fd=13, family=AddressFamily.AF_INET,type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 12306), raddr=('127.0.0.1', 38884)>; c.close()的时候fd变成-1
c.send(b'hh') #raddr(并不能引用)不复存在是 send一次照常 第二次BrokenPipeError
c.recv(1024) #阻塞函数 raddr不复存在时[永远]返回空, 可设置c.settimeout(10) 10s收不到报错 None时没有期限; bytes data
c.close()
sockfd.close()

#tcp_telnet
'''
telnet 0.0.0.0 12306
hiya from telnet~~
roger that from server
[ctrl ]到命令行 可以quit; c代理或socket关闭时也会退出(正常情况下)]
'''

#tcp_client
from socket import *

sockfd = socket()
sockfd.connect(('0.0.0.0',12306)) #connect后(server listen后)自动会bind一个地址, 也可以自行在前bind
sockfd.send(b'hiya from client') 
sockfd.recv(1024)
sockfd.close()


#udp_server
from socket import *

sockfd=socket(AF_INET, SOCK_DGRAM)
sockfd.bind(('0.0.0.0',12306))
sockfd.sendto(b"hiya from server", ('192.168.1.136',23333))
msg,a=sockfd.recvfrom(1024)
sockfd.close()



#udp_client
from socket import *

sockfd=socket(AF_INET, SOCK_DGRAM)
sockfd.bind(('0.0.0.0',23333))
sockfd.sendto(b"hoya from client", ("0.0.0.0", 12306))
msg, a=sockfd.recvfrom(1024)
sockfd.close()
