import sqlite3
import os,json

conn = sqlite3.connect("cardcenter.db")
cur = conn.cursor()

if __name__=="__main__":
    
    for i in list(os.walk("./data"))[0][2]:
        print(i)
        d = "./data/"+i
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
                
                cur.execute("insert into basicData values ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(id,name,puid,grade,gender,schoolN,schoolC,classNo,picUrl))
                
                
    conn.commit()
    """
    a=[(1 if i[:2]=="11" else 0) for i in list(os.walk("./data"))[0][2]]
    print(a.count(1))
    """