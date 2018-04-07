# -*- coding: utf-8 -*-
#
# Flaskフレームワークを使用した蔵書管理ツール
#
# Copyright (c) 2018 YA-androidapp(https://github.com/YA-androidapp) All rights reserved.

import urllib.request
import xml.etree.ElementTree as ET

isbn = '978**********'
isbn = isbn.replace('-', '').replace(' ', '')
if isbn.isdigit() and len(isbn) == 13:
    url = 'http://iss.ndl.go.jp/api/sru?operation=searchRetrieve&query=isbn=' + isbn
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        # TODO
        xml = response.read().decode(response.headers.get_content_charset())
        xml = xml.replace('&lt;', '<').replace('&gt;', '>').replace(
            '&apos;', '\'').replace('&quot;', '"').replace('&amp;', '&')
        root = ET.fromstring(xml)
        # print(root.tag, root.attrib)
        # '{http://www.loc.gov/zing/srw/}searchRetrieveResponse'

        # for e in root.getiterator("{http://www.loc.gov/zing/srw/}searchRetrieveResponse"):
        #     for f in e.getiterator("{http://www.loc.gov/zing/srw/}records"):
        #         for g in f.getiterator("{http://www.loc.gov/zing/srw/}record"):
        #             for h in g.getiterator("{http://www.loc.gov/zing/srw/}recordData"):
        #                 for i in h.getiterator("{http://purl.org/dc/elements/1.1/}title"):
        #                     print(i.tag, i.text)
        #                 for k in h.getiterator("{http://purl.org/dc/elements/1.1/}publisher"):
        #                     print(k.tag, k.text)

        print(root.find(".//{http://purl.org/dc/elements/1.1/}title").text)
        # print(root.find(".//{http://purl.org/dc/elements/1.1/}publisher").text)
        for k in root.findall(".//{http://purl.org/dc/elements/1.1/}publisher"):
            print(k.text)
        # print(root.find(
        #     ".//{http://www.loc.gov/zing/srw/}searchRetrieveResponse/records/record/recordData").tag)
