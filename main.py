#这个程序的目的是模仿下putty客户端的功能，主要是为了实现命令行界面的功能
#要解决的第一个问题是关于重复建立session的问题，这个问题在之前给集成的人跑脚本的时候就发现了，这次相办法解决这个问题
#要解决的第二个问题就是如何解决显示当前所在文件夹的功能，这个已经暂时想到了如何解决
#接下来要解决的，就是如何处理在退出session之后，还能回到这之前的session的问题
#第四个要解决的，就是前台界面的问题，这个可以设计一个界面
#扩展需求：显示在网页端的方法，可以考虑使用本地django来实现这个目的（这个和后面使用Qt设计前台的选择一个就可以了）
#扩展需求，将用户输入的主机地址，用户名和密码存储到一个文件夹里面去
#扩展需求：支持在前台显示之前连接过IP地址，可以通过选择连接过去连接过的主机进行操作
#扩展需求，支持多主机部署（使用fabric模块进行操作，使用get和put方法）
#扩展需求：支持多主机信息采集，比如内存情况
#扩展需求：支持多主机的定时任务，这个需要考虑下如何在后台运行改程序
#扩展需求：支持在一个窗口打开另一个窗口，但是使用同一文件里面的信息
#扩展需求：支持输入密码本，来寻找主机的密码，后期需要支持暴力破解密码的功能
#扩展需求：支持使用多线程
#扩展需求：支持对多主机的密码进行修改（这个功能之前已经实现过了，但是还不太完善，这个想办法做两个接口出来
#扩展需求：支持对程序生成的密码文件进行加密和解密的功能
#扩展需求：支持对程序进行pyinstaller加工成EXE文件
#扩展需求：支持使用Qt设计的前台（前后台进行分离）
#get到一个新技能，前后端分离，业务模块之间松耦合，能加快开发，解除各个模块之间的依赖，这个真的很重要

from time import ctime ,sleep  
from fabric import Connection
import sys
import os 
import getpass


#函数menu：显示编译阶段的前台界面显示菜单

def menu():
    print('''
    ----------------------------------------------------------------------------------------------------------------------
                                             Apollo 0.0                                                                   
                                             1.新建ssh连接
                                             2.历史ssh连接
                                             3.多主机传输文件
                                             4.多主机部署执行
                                             5.多主机信息采集
                                             6.多主机定时任务设置
                                             7.多主机密码修改
                                             8.主机密码破解
                                             0.退出
                                                                                        Code by Liuzeng
    
    ''')

#获取用户输入参数
def getmenu():
    menu()
    try:
        selectinfo = int(input('请选择功能模块： '))
        if not selectinfo:
            print('即将退出程序，请稍等！')
            sys.exit()
        elif selectinfo == 1:
            MenuNewssh()
        elif selectinfo == 2:
            MenuOpensshcsv()
        elif selectinfo == 3:
            MenuFabricGetOrPut()
        elif selectinfo == 4:
            MenuFabricRunDouble()
        elif selectinfo == 5:
            MenuHostInfoCollect()
        elif selectinfo == 6:
            MenuTimeTask()
        elif selectinfo == 7:
            MenuPasswordChange()
        elif selectinfo == 8:
            MenuPasswordCracking()
        else :
            print('输入有误！请重新输入')
            getmenu()
    except Exception as identifier:
        print('无法识别的输入，请重新输入')
        getmenu()



#各个模块的菜单界面展示
def MenuNewssh():
    print('>>>>>请按照提示进行输入\n')
    hostinfo = [] 
    hostip = input ('请输入主机IP地址 : ')
    hostinfo.append(hostip)
    hostusername = input ('请输入用户名 ： ')
    hostinfo.append(hostusername)
    hostpassword = input('请输入密码 ：')
    hostinfo.append(hostpassword)
    #print(hostinfo)
    Newssh(hostinfo)



def MenuOpensshcsv():
    pass
def MenuFabricGetOrPut():
    pass
def MenuFabricRunDouble():
    pass 
def MenuHostInfoCollect():
    pass
def MenuTimeTask():
    pass
def MenuPasswordChange():
    pass
def MenuPasswordCracking():
    pass

#第一个模块的设计，这个模块设计成两个部分，一部分从用户输入读取相关信息，另一个部分是建立连接，中间要加入一个校验的功能
#校验功能的作用是判断用户的输入是否能够连接到主机，如果有误，重新进行密码输入，如果无误，建立连接，并且将主机信息保存到相关csv文件中
#保存模块的设计：先判断该主机的该用户是否已经添加到文件中，如果添加过，则不再添加，如果没有添加过，添加进去


#设计类一：HostConn，负责建立ssh连接对象
class HostConn():#info传入一个列表，为主机的信息
    def __init__(self,info):
        self.host=info[0]
        self.username = info[1]
        self.password = info[2]
        self.run = Connection(self.host,self.username,port = 22,connect_kwargs={"password": self.password}).run


def Newssh(hostinfo):
    host = HostConn(hostinfo)
    try:
        host.run('echo "Connect to the remote host successfully!!!"')
    except Exception as identifier:
        print('主机连接失败，请重新输入相关信息')
        MenuNewssh()
    infoincsv(hostinfo)
    SSHCommand(host)


def infoincsv(hostinfo):
    mark = False
    with open('hostinfo.csv','r') as f:
        for line in f:
            host = line.strip().split(',')
            if hostinfo[0] == host[0]:
                mark = True            
    #print(mark)
    if not mark :
        with open('hostinfo.csv','a') as f:
            #print(hostinfo,file = f)
            for i in hostinfo:
                print(i,end = ',',file = f)
            print('',file =f)


def SSHCommand(host):
    mark = True
    while mark:
        sshcommand = input ('>>>>>>>>')
        if sshcommand == 'exit' :
            mark = False
        else :
            host.run('ls')

    


















if __name__ == '__main__':
    mark = True
    while mark:
        try:
            getmenu()
            exittrigger = int(input('是否退出？ 0 ：退出  1 ：暂不，继续执行其他任务 '))
            if exittrigger:
                pass 
            else:
                mark =False
        except Exception as identifier:
            print('无法识别的输入，请重新输入')
            getmenu()



























