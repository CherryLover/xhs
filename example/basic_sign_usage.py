import datetime
import json
import os
import atexit
import requests
from bs4 import BeautifulSoup

from xhs import XhsClient
from sign_helper import SignHelper
from share_link_parser import parse_share_link


# 全局的 SignHelper 实例
_sign_helper = None

def get_sign_helper(a1):
    global _sign_helper
    if _sign_helper is None:
        _sign_helper = SignHelper(cookie_value=a1)
    return _sign_helper

def cleanup():
    """程序退出时清理资源"""
    global _sign_helper
    if _sign_helper:
        _sign_helper.close()

# 注册程序退出时的清理函数
atexit.register(cleanup)

def sign(uri, data=None, a1="", web_session=""):
    # 使用全局的 SignHelper 实例进行签名
    sign_helper = get_sign_helper(a1)
    return sign_helper.sign(uri, data)
    
def get_first_normal_note(xhs_client, type: str = "normal"):
    like_notes = None
    # 从本地文件中读取点赞笔记
    with open("output/result/like_notes.json", "r", encoding="utf-8") as f:
        like_notes = json.load(f)
    
    # 获取第一个普通笔记
    target_note = None
    for note in like_notes["notes"]:
        if note["type"] == type:
            target_note = note
            break
    if target_note is None:
        print("没有找到笔记")
        return
    print(f"尝试获取({target_note['type']})笔记：{target_note['display_title']} {target_note['note_id']}")
    # 获取笔记详情
    note_id = target_note["note_id"]
    note_token = target_note["xsec_token"]
    note_info = xhs_client.get_note_by_id(note_id, note_token)
    with open(f"output/result/normal_note_info_{type}.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(note_info, indent=2, ensure_ascii=False))
    print(f"笔记详情已保存到 normal_note_info_{type}.json")
    

def get_user_like_notes(xhs_client, user_id):
    user_info = xhs_client.get_user_info(user_id)
    with open("output/result/user_info.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(user_info, indent=2, ensure_ascii=False))
    print("用户信息已保存到 user_info.json")
    
    like_notes = xhs_client.get_user_like_notes(user_id)
    with open("output/result/like_notes.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(like_notes, indent=2, ensure_ascii=False))
    print("用户点赞笔记已保存到 like_notes.json")

if __name__ == '__main__':
    cookie = "abRequestId=3d8983fd-0774-5021-afe5-91a715a9fc66; a1=19452faac32onyn8kwmbmwdm8twli3b25jk7nu6dr30000421691; webId=1a949ba2138c8e0ee166c4d33ce939a7; gid=yj4qd0Y4YW28yj4qd0Yy428vKdM1S6U8xfi23TCAYjUdT0q861Dl6D88848KKJW880K4SWiJ; web_session=0400698c34a8f1112a5acedd49354b68911d2e; customer-sso-sid=68c5174570031110560055878183567fbe5b3fde; x-user-id-creator.xiaohongshu.com=5d40ebb90000000010037a0c; customerClientId=854346337484963; access-token-creator.xiaohongshu.com=customer.creator.AT-68c517457003111056170663zpp17hoarxnoqbce; galaxy_creator_session_id=CG1YdObVpvDyUwbTOpgb3CyicvOzmnGEHpm4; galaxy.creator.beaker.session.id=1736218834507086145307; xsecappid=xhs-pc-web; webBuild=4.54.0; acw_tc=0a0bb12f17365590080705993eca76e52a9c1500c162cd4d2173ab5e59f5c7; websectiga=634d3ad75ffb42a2ade2c5e1705a73c845837578aeb31ba0e442d75c648da36a; sec_poison_id=add8da06-fc42-475c-96f8-2d21a8f37af2"
    
    share_info = "http://xhslink.com/a/vUTC3L6EXo12，复制本条信息，打开【小红书】App查看精彩内容！"
    xhs_client = XhsClient(cookie, sign=sign)
    
    # 创建输出目录
    os.makedirs("output/result", exist_ok=True)
    
    # 解析分享链接
    parse_share_link(share_info)
    
    user_id = "5d40ebb90000000010037a0c"
    # get_user_like_notes(xhs_client, user_id)
    # get_first_normal_note(xhs_client, "normal")
    # get_first_normal_note(xhs_client, "video")
