import chardet
from lxml import etree
import re
from reqaio import aio
import parser
from cmdhelper import wrapper

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

def crawl_from_to(start=1,end=2):
    """
        Crawls from start to end
    """
    ids = range(start, end)
    urlTemp = "http://www.dpxq.com/hldcg/search/view_m_%d.html"
    urls = [urlTemp % id for id in ids]
    rets = []
    

    def ubb_crawl_cb(url, content):
        coding = chardet.detect(content)['encoding'] or "GB2312"
        content = content.decode(coding, 'ignore')
        ubbplay = ubbParse(content) 
        ubb = parser.convert_to_dic(ubbplay)
        rets.append(ubb)
    aio.run(urls, ubb_crawl_cb)
    return rets

from clize import run
if __name__ == '__main__':
    wrapper.__name__ = "__main__"
    run(wrapper.jsonfy_this(crawl_from_to))

