
import os
def savePlay(dir, title, content, ext="txt", encoding="utf-8"):
    local = os.path.join(dir,encoding) 
    file = str(title) + "." + ext
    path = os.path.join(local, file)
    if not os.path.exists(local):
        os.mkdir(local)
    print(path)
    try:
        with open(path, "w", encoding=encoding,errors="ignore") as f:
            f.write(content)
            f.close()
    except Exception as e:
        print("play %s save as file has failed" % title)
        print(e)
        pass

