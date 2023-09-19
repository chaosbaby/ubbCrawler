import chardet
from lxml import etree
import re
from reqaio import aio
import json
import parser

playXpath = '//*[@id="dhtmlxq_view"]//text()'
xpathMoveStr = '//*[@type="text/javascript"]//text()'
ubbMovePattern = "\[DhtmlXQ_movelist\][\s\S]*\[/DhtmlXQ_movelist\]"


def ubbParse(c):
    content = etree.HTML(c)
    ubbPlay = content.xpath(playXpath)
    ubbMoveList = content.xpath(xpathMoveStr)
    ubbMoveStr = " ".join(ubbMoveList)
    ubbMove = re.findall(ubbMovePattern, ubbMoveStr)[0]
    ubbMove = "\r\n%s" % ubbMove
    ubbPlayStr = " ".join(ubbPlay)
    ubbPlayStr = re.sub(ubbMovePattern, ubbMove, ubbPlayStr)
    return ubbPlayStr

def test():
    ids = range(1, 2)
    urlTemp = "http://www.dpxq.com/hldcg/search/view_m_%d.html"
    urls = [urlTemp % id for id in ids]
    rets = []
    

    def ubb_crawl_cb(url, content):
        coding = chardet.detect(content)['encoding'] or "GB2312"
        content = content.decode(coding, 'ignore')
        ubbplay = ubbParse(content) 
        ubb = parser.convert_to_json(ubbplay)
        jsonUbb = json.dumps(ubb, ensure_ascii=False)
        rets.append(jsonUbb)
    aio.run(urls, ubb_crawl_cb)
    return rets

from clize import run
if __name__ == '__main__':
    run(test)

