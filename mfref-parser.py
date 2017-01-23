#!/usr/bin/env python
# -*- coding: utf-8 -*-

import htmllib
import formatter
import urlparse
import urllib2

rsstemplate = """<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/DTDs/Podcast-1.0.dtd" xmlns:media="http://search.yahoo.com/mrss/">

<channel>
<title>Mátyásföldi istentiszteletek 2017</title>
<description>Mátyásföldi istentiszteletek 2017</description>
<itunes:author>Szabó Péter</itunes:author>
<link>http://www.matyasfoldiref.hu/2017.-evi</link>
<itunes:image href="http://www.matyasfoldiref.hu/matyasfoldiref-theme/images/banner/banner1200.jpg" />
<!--pubDate> Sun, 09 Oct 2005 21:00:00 PST </pubDate-->
<language>hu-HU</language>
<copyright>Copyright 2017 Cinkota-Mátyásföldi Református Egyházközség </copyright>

<!--items-->
</channel>
</rss>"""

itemtemplate = """    <item>
    <title><!--title--></title>
    <description><!--description--></description>
    <itunes:author> matyasfoldiref.hu </itunes:author>
    <!--pubDate> Thu, 16 Jun 2005 5:00:00 PST </pubDate-->
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

        #f = urllib2.urlopen(pageurl)
        f = open('2017.-evi')
        data = f.read()
        f.close()

        parser.feed(data)
        return collected_links

pageurl = 'http://www.matyasfoldiref.hu/2017.-evi'
lc = linkcollector(pageurl)
collected_links = lc.collect()

items = []
for cl in collected_links:
    item = itemtemplate
    item = item.replace('<!--title-->', cl)
    item = item.replace('<!--description-->', cl)
    item = item.replace('<!--url-->', cl)
    items.append(item)

rss = rsstemplate.replace('<!--items-->', "\n".join(items))

print (rss)
