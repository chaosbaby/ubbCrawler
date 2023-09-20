from ast import main
from sys import implementation
import db, parser,osutil
import sqlite3



def to_files(fr=1,to=2,path = 'resource/',ext = "txt",encoding="GB2312"):
    db_path="resource/test.db"
    t_name="chess_play"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    sqlStr = "select * from %s where id>=%d and id<=%d"%(t_name,fr,to)
    c.execute(sqlStr)
    rets = c.fetchall()
    for item in rets:
        ubb = parser.to_ubb(dict(item))
        osutil.savePlay(path,item["id"],ubb,ext,encoding)

    
from clize import run
if __name__ == '__main__':
    run(to_files)
    
