#!/usr/bin/env python
# -*- coding: utf-8 -*-

import htmllib
import formatter
import urlparse
import urllib2
import re

rsstemplate = """<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/DTDs/Podcast-1.0.dtd" xmlns:media="http://search.yahoo.com/mrss/">

<channel>
<title>Mátyásföldi istentiszteletek 2018</title>
<description>Mátyásföldi istentiszteletek 2018</description>
<itunes:author>matyasfoldiref.hu</itunes:author>
<link>http://www.matyasfoldiref.hu/2018.-evi</link>
<itunes:image href="http://www.matyasfoldiref.hu/matyasfoldiref-theme/images/banner/banner1200.jpg" />
<!--pubDate> Sun, 09 Oct 2005 21:00:00 PST </pubDate-->
<language>hu-HU</language>
<copyright>Copyright 2018 Cinkota-Mátyásföldi Református Egyházközség </copyright>

<!--items-->
</channel>
</rss>"""

itemtemplate = """    <item>
    <title><!--title--></title>
    <description><!--description--></description>
    <itunes:author>matyasfoldiref.hu</itunes:author>
    <pubDate><!--pubdate--></pubDate>
    <enclosure url="<!--url-->" type="audio/mpeg" />
    </item>"""

class linkcollector(object):
    def __init__(self, pageurl):
        self.pageurl = pageurl

    def collect(self):
        collected_links = []
        def collect_link(attrs):
            d = dict(attrs)
            if 'href' in d:
                href = d['href']
                if '.mp3' in href:
                    collected_links.append(urlparse.urljoin(pageurl, href))

        parser = htmllib.HTMLParser(formatter.NullFormatter())
        parser.start_a = collect_link

        f = urllib2.urlopen(pageurl)
        #f = open('2018.-evi')
        data = f.read()
        f.close()

        parser.feed(data)
        return collected_links

pageurl = 'http://www.matyasfoldiref.hu/2018.-evi'
lc = linkcollector(pageurl)
collected_links = lc.collect()

items = []
for url in collected_links:
    infopart = re.findall('2018.*mp3', url)
    if infopart:
        infopart = infopart[0]
        dt = infopart[0:4] + '-' + infopart[4:6] + '-' + infopart[6:8]
    else:
        infopart = url
        dt = '2018-01-01'
    item = itemtemplate
    item = item.replace('<!--title-->', infopart)
    item = item.replace('<!--description-->', url)
    item = item.replace('<!--url-->', url)
    item = item.replace('<!--pubdate-->', dt)

    items.append({'dt': dt, 'item': item})

items.sort(key=lambda x:x['dt'])
items = [ item['item'] for item in items ]

rss = rsstemplate.replace('<!--items-->', "\n".join(items))

print (rss)
