from urllib.request import *
from urllib.parse import *
import json
import base64
from PIL import Image
import numpy as np

ak="9xSGZD4Awmz4oDxnvalZA1Iz"
sk="tmWVFxHltxIKasmy8BUKKCIRMX5CwcZh"

def getCaptcha():
    with open("./cap.jpg",'wb') as f:
        r = urlopen("http://cardcenter.bjedu.cn/becom-sccms-web/servlet/validateCodeServlet").read()
        f.write(r)

def solveCaptcha(path):
    im = Image.open(path)
    im = im.convert("L")  # 灰值化

    img = im.copy() #二值化-----------
    w,h = img.size

    img = np.array(img)

    for y in range(0, w):
        for x in range(0, h):
            if img[x,y]>150:
                img[x,y]=255
            else:
                img[x,y]=0

    for y in range(1, w-1):
        for x in range(1, h-1):
            count = 0
            if img[x, y - 1] > 245:
                count = count + 1
            if img[x, y + 1] > 245:
                count = count + 1
            if img[x - 1, y] > 245:
                count = count + 1
            if img[x + 1, y] > 245:
                count = count + 1
            if count > 2:
                img[x, y] = 255

            if (img[x,y-1]>245 and img[x,y+1]>245)or(img[x-1,y]>245 and img[x+1,y]>245):
                img[x,y]=255

    for y in range(0, w - 1):
        for x in range(0, h - 1):
            cur_pixel = img[x, y]  # 当前像素点的值
            if y == 0:  # 第一行
                if x == 0:  # 左上顶点,4邻域
                    # 中心点旁边3个点
                    sum = int(cur_pixel) \
                          + int(img[x, y + 1]) \
                          + int(img[x + 1, y]) \
                          + int(img[x + 1, y + 1])
                    if sum <= 2 * 245:
                        img[x, y] = 0
                elif x == h - 1:  # 右上顶点
                    sum = int(cur_pixel) \
                          + int(img[x, y + 1]) \
                          + int(img[x - 1, y]) \
                          + int(img[x - 1, y + 1])
                    if sum <= 2 * 245:
                        img[x, y] = 0
                else:  # 最上非顶点,6邻域
                    sum = int(img[x - 1, y]) \
                          + int(img[x - 1, y + 1]) \
                          + int(cur_pixel) \
                          + int(img[x, y + 1]) \
                          + int(img[x + 1, y]) \
                          + int(img[x + 1, y + 1])
                    if sum <= 3 * 245:
                        img[x, y] = 0
            elif y == w - 1:  # 最下面一行
                if x == 0:  # 左下顶点
                    # 中心点旁边3个点
                    sum = int(cur_pixel) \
                          + int(img[x + 1, y]) \
                          + int(img[x + 1, y - 1]) \
                          + int(img[x, y - 1])
                    if sum <= 2 * 245:
                        img[x, y] = 0
                elif x == h - 1:  # 右下顶点
                    sum = int(cur_pixel) \
                          + int(img[x, y - 1]) \
                          + int(img[x - 1, y]) \
                          + int(img[x - 1, y - 1])

                    if sum <= 2 * 245:
                        img[x, y] = 0
                else:  # 最下非顶点,6邻域
                    sum = int(cur_pixel) \
                          + int(img[x - 1, y]) \
                          + int(img[x + 1, y]) \
                          + int(img[x, y - 1]) \
                          + int(img[x - 1, y - 1]) \
                          + int(img[x + 1, y - 1])
                    if sum <= 3 * 245:
                        img[x, y] = 0
            else:  # y不在边界
                if x == 0:  # 左边非顶点
                    sum = int(img[x, y - 1]) \
                          + int(cur_pixel) \
                          + int(img[x, y + 1]) \
                          + int(img[x + 1, y - 1]) \
                          + int(img[x + 1, y]) \
                          + int(img[x + 1, y + 1])

                    if sum <= 3 * 245:
                        img[x, y] = 0
                elif x == h - 1:  # 右边非顶点
                    sum = int(img[x, y - 1]) \
                          + int(cur_pixel) \
                          + int(img[x, y + 1]) \
                          + int(img[x - 1, y - 1]) \
                          + int(img[x - 1, y]) \
                          + int(img[x - 1, y + 1])

                    if sum <= 3 * 245:
                        img[x, y] = 0
                else:  # 具备9领域条件的
                    sum = int(img[x - 1, y - 1]) \
                          + int(img[x - 1, y]) \
                          + int(img[x - 1, y + 1]) \
                          + int(img[x, y - 1]) \
                          + int(cur_pixel) \
                          + int(img[x, y + 1]) \
                          + int(img[x + 1, y - 1]) \
                          + int(img[x + 1, y]) \
                          + int(img[x + 1, y + 1])
                    if sum <= 4 * 245:
                        img[x, y] = 0
    img = Image.fromarray(img)
    #img.show()
    img.save("capEd.jpg")

def getToken(ak,sk):
    r = urlopen("https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"%(ak,sk)).read()
    return json.loads(r)["access_token"]

def ocr(imgbytes):
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    img = base64.b64encode(imgbytes)
    params = {"image": img}
    access_token = getToken(ak,sk)
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    r = Request(request_url, data=urlencode(params).encode(), headers=headers)
    r = urlopen(r)
    #print(access_token)
    a = json.loads(r.read())
    a = a["words_result"]
    if len(a) < 1:
        return None
    else:
        return a[0]["words"].replace(" ","").lower()

def main(p):
    solveCaptcha(p)
    with open("capEd.jpg", "rb") as f:
        return ocr(f.read())
if __name__=="__main__":
    getCaptcha()
    #solveCaptcha("./captcha/cap.jpg")
    s=main("./cap.jpg")
    print(s)