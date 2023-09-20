from ast import Num
import chardet
from lxml import etree
import re
from reqaio import aio
import parser,db
from cmdhelper import wrapper
import os

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

def crawl_from(start=1,count=10):
    """
        Crawls from start to end
    """
    ids = range(start, start+count)
    urlTemp = "http://www.dpxq.com/hldcg/search/view_m_%d.html"
    urls = [urlTemp % id for id in ids]
    rets = []
    

    def ubb_crawl_cb(url, content):
        coding = chardet.detect(content)['encoding'] or "GB2312"
        content = content.decode(coding, 'ignore')
        ubbplay = ubbParse(content) 
        ubb = parser.to_dic(ubbplay)
        rets.append(ubb)
    aio.run(urls, ubb_crawl_cb)
    return rets



import sqlite3
# def crawl_to_db(start,end,db_path,t_name):
def crawl_to_db(to=1,db_path="resource/test.db",t_name="chess_play"):
    """
        Crawls from maxid with count afterwards
    """
    # db_path = "resource/test.db"
    # t_name = "chess_play"
    maxid = max_id()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    ids = range(maxid, to)
    urlTemp = "http://www.dpxq.com/hldcg/search/view_m_%d.html"
    urls = [urlTemp % id for id in ids]
    def ubb_crawl_cb(url, content):
        coding = chardet.detect(content)['encoding'] or "GB2312"
        content = content.decode(coding, 'ignore')
        ubbplay = ubbParse(content) 
        ubb = parser.to_dic(ubbplay)
        query, values = db.toSqlPairs(ubb, t_name)
        print(url)
        c.execute(query, values)
    aio.run(urls, ubb_crawl_cb)
    conn.commit()
    conn.close()

def savePlay(dir, title, content, ext="txt", encoding="utf-8"):
    # code = content.encode()
    # content = code.decode(encoding, 'ignore')

    # local = r"{}\{}".format(dir, encoding)
    local = os.path.join(dir,encoding) 
    file = title + "." + ext
    path = os.path.join(local, file)
    if not os.path.exists(local):
        os.mkdir(local)
    print(path)
    try:
        with open(path, "w", encoding=encoding) as f:
            f.write(content)
            f.close()
    except Exception as e:
        print("play %s save as file has failed" % title)
        print(e)
        pass

def max_id():
    db_path="resource/test.db"
    t_name="chess_play"
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("select max(id) from chess_play")
    maxid = c.fetchone()[0]
    return maxid
    


def crawl_to_file(count=1,path="resource/"):
    """
        Crawls from start to end to db
    """
    # db_path = "resource/test.db"
    # t_name = "chess_play"
    maxid = max_id()
    ids = range(maxid, maxid + count)
    urlTemp = "http://www.dpxq.com/hldcg/search/view_m_%d.html"
    urls = [urlTemp % id for id in ids]

    def ubb_crawl_cb(_, content):
        coding = chardet.detect(content)['encoding'] or "GB2312"
        content = content.decode(coding, 'ignore')
        ubbplay = ubbParse(content) 
        ubb = parser.to_dic(ubbplay)
        savePlay(path,ubb['id'],ubbplay)


    aio.run(urls, ubb_crawl_cb)

from clize import run
if __name__ == '__main__':
    run(wrapper.jsonfy_this(crawl_from) ,crawl_to_db,max_id,crawl_to_file)

