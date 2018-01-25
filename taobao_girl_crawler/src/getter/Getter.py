from bs4 import BeautifulSoup
import requests
import re
import json
from src.header import *
from src.getter.Getter import *


def getUserIdList(page):
    user_info_template = "姓名：{}\n身高：{}\n体重：{}\n地址：{}"
    param = {"currentPage": str(page)}
    response = requests.get(url="https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8", params=param,
                            headers=getHeader())
    response.encoding = response.apparent_encoding
    load_dict = json.loads(response.text)
    user_info_list = load_dict.get("data").get("searchDOList")
    for user_info in user_info_list:
        user_id = user_info.get("userId")
        name = user_info.get("realName")
        height = user_info.get("height")
        weight = user_info.get("weight")
        city = user_info.get("city")
        user_info_str = user_info_template.format(name, height, weight, city)
        yield user_info_str, user_id, name


def get_img_info(user_id):
    pre_page = requests.get("https://mm.taobao.com/self/album/open_album_list.htm",
                            params={"user_id": user_id, "_charset": "utf-8"},
                            headers=getHeader())
    pre_page.encoding = pre_page.apparent_encoding
    soup = BeautifulSoup(pre_page.text, "html.parser")
    imglist = soup.find_all("a", attrs={"class", "mm-first"})
    # 获得一个用户的相册id
    ablumIds = []
    for img in imglist:
        href = img["href"]
        try:
            ablumId = re.findall(r"album_id=[0-9]{9}", href)[0].replace("album_id=", "")
            ablumIds.append(ablumId)
        except:
            pass

    # 返回用户ablum的图片信息
    for ablumId in ablumIds:
        tmpUrl = "https://mm.taobao.com/album/json/get_album_photo_list.htm"
        tmptext = requests.get(tmpUrl, params={"user_id": user_id, "album_id": ablumId})
        tmpjson = json.loads(tmptext.text)
        ablum_infos = tmpjson.get("picList")
        if ablum_infos is None:
            continue
        for ablum_info in ablum_infos:
            picUrl = ablum_info.get("picUrl")
            picUrl = ("https:" + picUrl).replace("290x10000", "620x10000")
            print(picUrl)
            yield requests.get(picUrl).content, ablumId
