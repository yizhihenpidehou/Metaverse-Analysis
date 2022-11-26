#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 提取dblp中的article
from xml.sax.saxutils import escape
import xml.sax
from xml.sax.handler import feature_external_ges



class WorkHandler(xml.sax.ContentHandler):
    res = ''

    def resolveEntity(self, publicID, systemID):
        print("TestHandler.resolveEntity(): %s %s" % (publicID, systemID))
        return systemID

    def __init__(self, ww):
        self.CurrentData = ""
        self.CurrentAttributes = ""
        self.title = ""
        self.year = ""
        self.ee = ""
        self.booktitle = ""
        self.author = ""
        # 筛选文章类型
        self.rightintent = ""
        self.ww = ww

    def startElement(self, tag, attributes):
        print('tag1 here:', tag)
        self.CurrentData = tag
        self.CurrentAttributes = attributes
        # 只关注article，proceedings，inproceedings，phdthesis/masterthesis

        if (tag == "inproceedings"):
            # print ("---------------------------------\n")
            self.ww.write("---------------------------------\n")
            print('yes inproceedings')
            # 保存文章类型,article tag 开始时，提醒下面要开始抓取数据
            self.rightintent = tag

        else:
            return

    def endElement(self, tag):
        print('tag2 here:', tag)
        # print('rightintent:',self.rightintent)
        # 检查文章类型
        if (self.rightintent == "inproceedings"):
            if self.CurrentData == "year":
                # print ("Year:", self.year)
                self.ww.write("Year:" + self.year + "\n")
                # self.__class__.res=self.__class__.res+self.year+';,;'
            elif self.CurrentData == "title":
                # print ("title:", self.title)
                self.ww.write("title:" + self.title + "\n")
                # self.__class__.res=self.__class__.res+self.title+';,;'
            elif self.CurrentData == "booktitle":
                # print ("title:", self.title)
                self.ww.write("booktitle:" + self.booktitle + "\n")
                # self.__class__.res=self.__class__.res+self.title+';,;'

            elif self.CurrentData == "ee":
                # print ("title:", self.title)
                self.ww.write("ee:" + self.ee + "\n")

            elif self.CurrentData == "author":
                # print ("title:", self.title)
                self.ww.write("author:" + self.author + "\n")
                self.author = ""
                # self.__class__.res=self.__class__.res+self.title+';,;'
            self.CurrentData = ""
            print("finish one!")
        else:
            print("other type")
        if (tag == "inproceedings"):  # 在一个article tag结束时，下一次要重新判断
            print("inproceedings end!--------------------")
            self.rightintent = ""

    def characters(self, content):
        if self.rightintent == "inproceedings":
            if self.CurrentData == "year":
                self.year = content
            elif self.CurrentData == "title":
                self.title = content
            elif self.CurrentData == "booktitle":
                self.booktitle = content
            elif self.CurrentData == "ee":
                self.ee = content
            elif self.CurrentData == "author":
                self.author += content
        else:
            return


def start(dblp_path, res_path):
    ww = open(res_path, 'w+')
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    parser.setFeature(feature_external_ges, True)
    Handler = WorkHandler(ww)
    parser.setContentHandler(Handler)

    parser.setEntityResolver(Handler)
    parser.setDTDHandler(Handler)

    parser.parse(dblp_path)

    ww.close()
    return res_path

# dblp_path = "dblp.xml"
# res_path = '11月inproceedings.txt'
# start(dblp_path, res_path)
