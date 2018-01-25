import os
from src.getter.Getter import getUserIdList,get_img_info
path_dir = "../data/{}"

def writeSimple(dirName, user_info_str):
    savePath = path_dir.format(dirName)
    try:
        os.mkdir(savePath)
        with open(savePath + "/" + dirName + ".txt", "w") as f:
            f.write(user_info_str)
    except:
        pass


def writePhoto(content,ablumId,dirName,photoName):
    savePth = path_dir.format(dirName) + "/" + ablumId
    try:
        os.mkdir(savePth)
    except:
        pass
    with open(savePth+"/"+photoName+".jpg","wb") as f:
        f.write(content)


def writeInfo(page):
    for user_info_str, user_id, name in getUserIdList(page):
        writeSimple(name, user_info_str)
        i = 0;
        for content,ablumId in get_img_info(user_id):
            photoName = ablumId+str(i)
            dirName = name
            writePhoto(content,ablumId,dirName,photoName)
            i+=1