import sqlite3
import os,json

conn = sqlite3.connect("cardcenter.db")
cur = conn.cursor()

if __name__=="__main__":
    
    noL = []
    with open("./no.list","r") as f:
        noL = [i[:8] for i in f.readlines()]
    workL = set([i[:8] for i in list(os.walk("./data"))[0][2]]) - set([i[0] for i in cur.execute("select id from HighSchool;").fetchall()])-set(noL)-set([i[0] for i in cur.execute("select id from JuniorSchool;").fetchall()])-set([i[0] for i in cur.execute("select id from SorPSchool;").fetchall()])
    print(len(workL))
    for i in workL:
        print(i)
        d = "./data/"+i+".json"
        with open(d,"r",encoding="utf-8") as f:
            r = json.loads(f.read())
            if r["resultCode"]=="0":
                r=r["resultData"]
                id = r["eduId"]
                gender = r["stuGender"]
                name = r["stuName"]
                classNo=r["classNo"]
                grade = r["grade"]
                puid = r["idNo"]
                picUrl = r["picUrl"]
                schoolN = r["office"]["name"]
                schoolC = r["office"]["code"]
                sL = r["schoolLevel"]
                #print(sL)
                cur.execute("insert into %s values ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(("HighSchool" if sL=="3"or sL=="0" else ("JuniorSchool" if sL=="2" else ("SorPSchool" if sL=="1" else None))),id,name,puid,grade,gender,schoolN,schoolC,classNo,picUrl))
            else:
                with open("./no.list","a") as f:
                    f.write(i+"\n")
                
    conn.commit()
    """
    /cmisfolder/photos/2012003/2021/01034018/09067530.JPG
    a=[(1 if i[:2]=="11" else 0) for i in list(os.walk("./data"))[0][2]]
    print(a.count(1))
    """