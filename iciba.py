#coding=utf-8
# barton.li@primerobotics.com
# 2023/12/15
# learn

import os, time
import hashlib
import requests
from lxml import etree

class IcibaHtml(object):

    def __init__(self):
        pass

    def md5(self, data):
        md5hash = hashlib.md5(data.encode())
        return md5hash.hexdigest()

    def load(self, url, path):
        file = path + self.md5(url)
        data = []
        if os.path.exists(file):
            with open(file, "r", encoding="utf-8") as f:
                for line in f.readlines():
                    if len(line) == 0:
                        continue
                    data.append(line.split('|'))
        else:
            data = self.course(url)
            if not len(data):
                return data
            
            with open(file, "w", encoding="utf-8") as f:
                for line in data:
                    f.writelines('|'.join(line))
                    f.writelines('\n')
            
            time.sleep(1)

        return data
    
    def loadClass(self, id):
        path = "static\\{}\\".format(id)
        if not os.path.exists(path):
            os.mkdir(path)

        p = 1
        data = []
        while True:
            print("download page: " + str(p))
            url = "https://word.iciba.com/?action=words&class={}&course={}".format(id, p) 
            resp = self.load(url, path)
            if not len(resp):
                break
            data.extend(resp)
            p = p + 1
            pass

        return data

    def course(self, url):
        response = requests.get(url)
        html = response.content

        element = etree.HTML(html)
        nodes = element.xpath('//ul[@class="word_main_list"]//li')
        data = []
        for node in nodes:
            span = node.xpath('./div[@class="word_main_list_w"]//span')[0]
            title = span.attrib.get('title')

            a = node.xpath('./div[@class="word_main_list_y"]//a')[0]
            id = a.attrib.get('id')

            span = node.xpath('./div[@class="word_main_list_s"]//span')[0]
            val = span.attrib.get('title')
            data.append([title, val, id])
        
        return data


if __name__ == '__main__':
    html = IcibaHtml()
    html.loadClass(11)
    # html.load("https://word.iciba.com/?action=words&class=11&course=181", "static\\11\\")


