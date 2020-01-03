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
from pprint import pprint
import logging 
import logging.config

logging.config.fileConfig('log.conf')

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
            sleep(5)
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
#模块一：输入主机用户名密码，进行资料储存，并且打印SSH命令行界面
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
    print('''
    1.直接搜索：
    2.全量寻找
    0.返回上级菜单    
    ''')
    selectTrigger = input('请输入你的选择：')
    if selectTrigger == '1':
        searchinfo = searchFromCSV()
    elif selectTrigger == '2':
        searchinfo = allFromCSV()
    else:
        getmenu()
    Newssh(searchinfo)


#模块三功能菜单

def MenuFabricGetOrPut():
    print('''
    请选择上传或者下载功能（上传的文件格式应为压缩包格式）
    1.上传
    2.下载
    0.退出到首页''')
    selecttrigger = input('请输入你的选择： ')
    if selecttrigger == '1':
        PutIntoHost()
    elif selecttrigger == '2':
        GetFromHost()
    else:
        getmenu()


def MenuFabricRunDouble():
    print('''
        请选择执行方式：
        1.输入单条命令多主机执行
        2.输入shell脚本执行
    ''')
    selectinfo = input('请选择执行方式： ')
    if selectinfo ==  '2':
        shellBatchRun()
    else:
        BatchRun() 



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
#突然发现保存模块有问题，设计的不合理，如果是一个主机上的其他用户，那就添加不了了，这个现在改一下

#设计类一：HostConn，负责建立ssh连接对象
class HostConn():#info传入一个列表，为主机的信息
    def __init__(self,info):
        self.host=info[0]
        self.username = info[1]
        self.password = info[2]
        self.conn =  Connection(self.host,self.username,port = 22,connect_kwargs={"password": self.password})
        self.put = self.conn.put
        self.get = self.conn.get
        self.run = Connection(self.host,self.username,port = 22,connect_kwargs={"password": self.password}).run

#下面的这三个函数是嵌套的，完成一个命令行界面的功能，其中NewSSH完成信息的收集并且判断是否为新主机
#infoincsv的功能是将新出现的主机添加到文件中去
#SSHcommand是主力，完成命令行的交互，以及错误的显示，只能是一个粗糙的界面，还做不到非常细致，要继续改进
def Newssh(hostinfo):
    host = HostConn(hostinfo)
    try:
        host.run('echo "Connect to the remote host successfully!!!"')
    except Exception as identifier:
        print('主机连接失败，请重新输入相关信息')
        selecttrigger = input('是否继续输入？0:取消 1:继续输入 2：全量查找  ')
        if selecttrigger == '1':
            MenuNewssh()
        elif selecttrigger == '2':
            allFromCSV()
        else:
            getmenu()
            
        
    infoincsv(hostinfo)
    SSHCommand(host)


def infoincsv(hostinfo):
    mark = False
    with open('hostinfo.csv','r') as f:
        for line in f:
            host = line.strip().split(',')
            if hostinfo[0] == host[0] and hostinfo[1] == host[1]:
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
    path = host.run('pwd',hide = True ,warn = True).stdout
    while mark:
        try:
            sshcommand = input ( '['+path+']  ' + '>>>>>')
        except Exception as identifier:
            print('Can not excute this command!!')
            SSHCommand()
        if sshcommand == 'exit' :
            getmenu()
        else:
            if 'cd' in sshcommand:
                sshcommand1 = sshcommand.strip().split(' ')
                if sshcommand1[-1][0]  !=  '/' :
                    commandpath = path +'/'+sshcommand1[-1]
                    sshcommand = 'cd ' + commandpath
            cdcommand = 'cd ' + path
            testerr = host.run(sshcommand,hide = True,warn = True).stderr
            if not testerr:
                pathcommand =cdcommand + '&&' + sshcommand + '&&' + 'pwd'
                try:
                    RunResult =host.run(pathcommand,hide = True ,warn = True)
                    out = RunResult.stdout
                    err = RunResult.stdout
                    clearout = out.strip().split('\n')
                    path = clearout[-1]
                    outs = clearout[0:-1]
                    print(out)
                    #print(err,end = '')
                except Exception as identifier:
                    print('An unknown error had happend,try to connect the remote host agin')
            else:
                print(testerr)
                print('Please check it!!')


#接下来是第二个模块的编写，这个比较简单，完成的功能为显示所有连接过的主机，然后询问连接哪一台，用户输入选择后，开始启动连接    

def searchFromCSV():
    searchHost = input('请输入你想要检索的主机IP：  ')
    searchUsername = input('请输入你想要检索的用户名： ')
    with open('hostinfo.csv','r') as f :
        for line in f:
            hostinfo = line.strip().split(',')
            #print(hostinfo)
            if searchHost == hostinfo[0] and searchUsername == hostinfo[1]:
                return hostinfo
                
    
        print('你检索的用户不存在，请重新检索！')
        MenuOpensshcsv()


def allFromCSV():
    number = 1
    hostdict = {}
    with open('hostinfo.csv','r') as f:
        for line in f:
            info =line.strip().split(',')
            hostip = info[0]
            hostuser = info [1]
            userAtIp = hostuser +'@' +hostip 
            hostdict[number]= userAtIp
            number +=1
    pprint(hostdict)
    seelctTrigger =int(input('请输入你选择的主机的号码：  '))
    hostfromdict =hostdict[seelctTrigger]
    infoSelect = hostfromdict.split('@')
    ip = infoSelect[1]
    user = infoSelect[0]
    with open('hostinfo.csv','r') as f :
        for line in f:
            hostinfo = line.strip().split(',')
            if ip == hostinfo[0] and user == hostinfo[1]:
                return hostinfo
                break


#写一个上面两个的结合体，传入两个参数，分别是主机地址和用户名，下面这个函数进行检索，然后return一个列表出去
#传入的格式要求：root@1.1.1.1这种,不对外暴露接口可以用这种方式传递参数
#            hostip = info[0]
#            hostuser = info [1]
#            userAtIp = hostuser +'@' +hostip 
def searchInCSV(userAtIp):
    infoSelect= userAtIp.strip().split('@')
    ip = infoSelect[1]
    user = infoSelect[0]
    with open('hostinfo.csv','r') as f :
        for line in f:
            hostinfo = line.strip().split(',')
            if ip == hostinfo[0] and user == hostinfo[1]:
                return hostinfo
                break
    return None
   
 

def SelectHost():
    print('请开始输入想要选择的主机，格式应为:  mysql@10.10.10.10,oracle@10.10.10.12,...... 按回车结束输入   ')
    selectString  = input('请开始输入 ： ')
    select1 = selectString.strip().split(',')
    selectList = []
    for useratip in select1:
        selectkey = useratip.strip().split('@')
        ip = selectkey[1]
        user = selectkey[0]
        with open('hostinfo.csv','r') as f :
            for line in f:
                hostinfo = line.strip().split(',')
                if ip == hostinfo[0] and user == hostinfo[1]:
                    selectList.append(hostinfo)
    return selectList


def BatchSelect():
    number = 1
    hostdict = {}
    with open('hostinfo.csv','r') as f:
        for line in f:
            info =line.strip().split(',')
            hostip = info[0]
            hostuser = info [1]
            userAtIp = hostuser +'@' +hostip 
            hostdict[number]= userAtIp
            number +=1
    pprint(hostdict)
    selecttNumber =input('请输入你想要选择的主机的编号，以逗号分隔（注意：应为英文逗号 ，按回车结束输入）  ：  ')
    selectInfo = selecttNumber.strip().split(',')
    #print(selectInfo)
    selectList=[]
    for number in selectInfo:
        number = int(number)
        searchResult = hostdict[number]
        infoSelect = searchResult.split('@')
        #print(infoSelect)
        ip = infoSelect[1]
        user = infoSelect[0]
        #print(ip,user)
        with open('hostinfo.csv','r') as f :
            for line in f:
                hostinfo = line.strip().split(',')
                #print(hostinfo)
                if ip == hostinfo[0] and user == hostinfo[1]:
                    selectList.append(hostinfo)
                    #print(selectList)
    
    print(selectList)
    return selectList

#loglevel记录日志的级别
#runcommand与前面ssh命令行的模块不同之处：接受一个主机和命令的输入，用于批量执行命令的模块
#但是只能跑单条命令
#如果想要跑多条命令的话，后面会增加一个模块，将命令写到一个shell文件中，直接推到服务器上去，然后执行，这个可以和第三个模块的功能一起实现
def runCommand(hostinfo,runcommand):
    host = HostConn(hostinfo)    
    try:
        result = host.run(runcommand,warn =True,hide = True)
        print(hostinfo[0]+ ' : ' + result.stdout)
        logging.debug(hostinfo[0]+ ' : ' +result.stdout)
        #logging.warn(result.warn)
        logging.error(hostinfo[0]+ ' : ' +result.stderr)

    except Exception as identifier:
        print('执行命令失败，请检查原因')


def PutIntoHost():
    print('''
            1.手动输入挑选
            2.按照编号挑选
    
    ''')
    selectMethod = input('请输入挑选方式 ： ')
    if selectMethod == '1':
        hostlist = SelectHost()
    else:
        hostlist = BatchSelect()
    LocalPath = input('请输入选择上传文件的绝对路径： ')
    #print(LocalPath)
    remotepath = input('请输入选择上传文件的主机目录： ')
    #print(remotepath)
    print('请耐心等待，时间视网络速度与文件大小而定  ')
    for Host in hostlist:
        #print(host)
        host = HostConn(Host)
        #host.put(localpath,remotepath)
        try:
            host.put(LocalPath,remotepath)
            print('%s主机传输文件任务完成！ '%Host[0])
            logging.info('%s主机传输文件任务完成,传输文件为%s,传输路径为%s '%(Host[0],LocalPath,remotepath))
            # print(result)
        except Failure as identifier:
            print('%s的%s上传失败'%(host,LocalPath))
        

def GetFromHost():
    print('''
            1.手动输入挑选
            2.按照编号挑选
    
    ''')
    selectMethod = input('请输入挑选方式 ： ')
    if selectMethod == '1':
        hostlist = SelectHost()
    else:
        hostlist = BatchSelect()
    
    remotepath = input('请输入选择下载的文件（输入绝对路径）： ')
    LocalPath = input('请输入选择下载文件的存储路径： ')
    #print(LocalPath)

    #print(remotepath)
    print('请耐心等待，时间视网络速度与文件大小而定  ')
    for Host in hostlist:
        #print(host)
        host = HostConn(Host)
        LocalPath = LocalPath +Host[0] 
        #(localpath,remotepath)
        try:
            host.get(remotepath,LocalPath)
            print('%s主机传输文件任务完成！ '%Host[0])
            logging.info('%s主机传输文件任务完成,下载文件为%s,存储路径为%s '%(Host[0],remotepath,LocalPath))
            # print(result)
        except Exception as identifier:
            print('%s的%s下载失败'%(host,LocalPath))
            logging.warn('%s主机传输文件任务失败,下载文件为%s,存储路径为%s '%(Host[0],remotepath,LocalPath))
           


def BatchRun():
    print('''
            请选择执行命令的主机：
            1.手动输入挑选
            2.按照编号挑选
    
    ''')
    selectMethod = input('请输入挑选方式 ： ')
    if selectMethod == '1':
        hostlist = SelectHost()
    else:
        hostlist = BatchSelect()
    mark = True 
    while mark:
            
        runcommand = input('请输入想要执行的命令： ')
        for host in hostlist:
            runCommand(host,runcommand)
        continuetrigger = input ('是否继续输入命令？ 0：退出 1：继续 ')
        if continuetrigger == '0':
            mark = False


def shellBatchRun():
    pass












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



























