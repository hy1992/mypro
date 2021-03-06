import requests
from lxml import etree
from threading import Thread
from time import sleep
class TiebaSpider:
    def __init__(self):
        self.url = "http://tieba.baidu.com/f?"
        self.baseurl = "http://tieba.baidu.com/"
        self.headers = {"User-Agent": "Mozilla5.0/"}
        self.pn = 0
        self.page = 1

    def getPage(self, kw, url):
        params = {
            "kw": kw,
            "pn": self.pn
        }
        res = requests.get(url, params=params, headers=self.headers)
        res.encoding = "utf-8"
        return res.text
    def parsePage(self,html):
        parseHtml = etree.HTML(html)
        r_list = parseHtml.xpath('//div[@class="threadlist_title pull_left j_th_tit "]/a/@href')
        url_list = []
        for i in r_list:
            url_list.append(self.baseurl + i.strip())
        return  url_list

    def getImg(self, html):
        parseHtml = etree.HTML(html)
        r_list = parseHtml.xpath('//img[@class="BDE_Image"]/@src')
        return r_list

    def imgPage(self, u_list):
        img_list = []
        for url in u_list:
            res = requests.get(url, headers=self.headers)
            res.encoding = "utf-8"
            img_l = self.getImg(res.text)
            img_list.append(img_l)
        return img_list

    def writeImg(self, img_list):
        lt = []
        for url_list in img_list:
            sleep(0.1)
            t = Thread(target=self.writerFile, args=(url_list,))
            t.start()
            # t.setDaemon(True)
            lt.append(t)
        sleep(0.5)
        for i in lt:
            i.join()
            lt.remove(i)
    def writerFile(self, img_list):
        for url in img_list:
            res = requests.get(url, headers=self.headers)
            data = res.content
            with open("img2/%s.jpg" % url[-12:-4], "wb") as f:
                f.write(data)

    def workOn(self, kw):
        # kw = input("请输入贴吧名称：")
        img_list = []
        while True:
            html = self.getPage(kw, self.url)
            url_list = self.parsePage(html)
            img_list += url_list
            c = input("第%d页已经贴吧已经下载完毕，是否继续(y/n):"%self.page)
            if c == "y":
                self.page += 1
                self.pn = (self.page - 1)*50
            else:
                print("获取资源中，请稍侯...")
                break
        i_list = self.imgPage(img_list)
        self.writeImg(i_list)


if __name__ == "__main__":
    kw = input("请输入贴吧名称：")
    spider = TiebaSpider()
    spider.workOn(kw)