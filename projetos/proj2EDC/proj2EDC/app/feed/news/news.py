from urllib.request import urlopen
import xml.etree.ElementTree as ET

def getNews(num=3):
    file = urlopen("https://www.autoblog.com/rss.xml")
    tree = ET.parse(file)
    root = tree.getroot()
    result = []

    count = 0;
    for x in root.findall('./channel/item'):
        if count >= num:
            break
        new = {}
        new['title'] = x.find('./title').text
        new['link'] = x.find('./link').text
        new['image'] = x.find('./enclosure').attrib['url']

        result.append(new)
        count += 1

    return result






