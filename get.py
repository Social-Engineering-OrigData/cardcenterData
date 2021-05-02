#from gittle import Gittle
import os
from urllib.request import *
from urllib.error import *
from urllib.parse import *
import socket
import json
from time import sleep
import http.client
from doLogin import Login

#09068048
dataDir = "./data"
r=""

def readCookie():
    with open("./cookie","r") as f:
        return f.read()

def setCookie(cookie):
    with open("./cookie","w") as f:
        return f.write(cookie)

def pading(e,d=6):
    r = str(e)
    while(len(r)<d):
        r = "0"+r
    return r

def readlast():
    with open("./lastId", "r") as f:
        return f.read()

def setlast(eduId):
    print(eduId,"setId")
    with open("lastId","w") as f:
        f.write(eduId)
        f.flush()

cookie=readCookie()


#jeesite.session.id=f62002fc173c460dadc8c4b514cbe590
def getData(eduId):
    headers={
        "Cookie":cookie,
        "User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0"
    }
    r = Request("http://cardcenter.bjedu.cn/becom-sccms-web/a/card/studentCardQueryInfo/getStudentConfirm",headers=headers,data=urlencode({"educationId":eduId}).encode())
    try:
        data = urlopen(r).read()
        return data
    except URLError as e:
#    except socket.timeout,URLError as e:
        print(eduId, e)
        return getData(eduId)


def writeData(eduId,data):
    with open(os.path.join(dataDir, "%s.json" % (eduId)), "wb") as f:
        f.write(data)

def submit(commit):
    pass
    """
    global r

    remote = r.create_remote(name='github', url='git@github.com:Garin0828/cardcenterData.git')

    r.execute("git add *")
    r.commit("-m %s"%(commit))
    print(dir(r))
    remote.remote().push("main")
    """

def main():
    li = readlast()
    y = li[:2]
    c = li[2:]

    deadc=0
    submitc=0
    for i in range(int(c),900000):
        sleep(1)
        eduId = y+pading(i)
        d = getData(eduId)
        print(d)
        if json.loads(d.decode())["resultCode"] == "1":
            if i>200000:
                deadc += 1
            print(eduId,"not found")
        else:
            submitc += 1
            deadc = 0
            writeData(eduId,d)
            print(eduId,"ok")
        setlast(y+pading(int(i)+1))

        if submitc > 10:
            submit("owo")
            submitc = 0
        if deadc > 10000:
            break
    return 0
#11341253
if __name__=="__main__":
    def r():
        global cookie
        try:
            main()
        except json.decoder.JSONDecodeError:
            print("reLogin")
            cookie=Login()
            print(cookie)
            return r()
    r()
