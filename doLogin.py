import http.client
import ocrBaidu
from time import sleep

def Login():
    parms = "username=10174389&password=sXK%2BJPuCgETDTMW0YazCxQ%3D%3D&validateCode={}"

    conn = http.client.HTTPConnection("cardcenter.bjedu.cn")
    conn.request("GET", "/becom-sccms-web/a/login",headers={"Connection":"keep-alive"})
    a = conn.getresponse()
    cookie = a.getheader("Set-Cookie").split(";")[0]
    a.read()
    print(cookie)

    while (1):
        conn.request("GET", "/becom-sccms-web/servlet/validateCodeServlet",headers={"Cookie":cookie})
        sleep(1)
        r=conn.getresponse()
        if "Set-Cookie" in r.headers:
            cookie = r.getheader("Set-Cookie").split(";")[0]
            print(cookie)
        a=r.read()
        with open("captcha.jpg", "wb") as e:
            e.write(a)
        c = ocrBaidu.main("captcha.jpg")
        print(c)

        conn.request("POST", "/becom-sccms-web/a/login", body=parms.format(c),headers=
            {
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
                "Cookie":cookie,
                "Content-Type":"application/x-www-form-urlencoded"
            })
        print(parms.format(c))
        r = conn.getresponse()
        a = r.getcode()
        r = r.read().decode()
        if a == 302:
            print(cookie)
            r = cookie
            with open("./cookie","w") as f:
                f.write(cookie)
            return r
        print(r)



if __name__ == "__main__":
    print(Login())
