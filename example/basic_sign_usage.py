import datetime
import json
import os
import requests

import xhs.help
from xhs import XhsClient


def sign(uri, data=None, a1="", web_session=""):
    # 填写自己的 flask 签名服务端口地址
    res = requests.post("http://localhost:5005/sign",
                        json={"uri": uri, "data": data, "a1": a1, "web_session": web_session})
    signs = res.json()
    return {
        "x-s": signs["x-s"],
        "x-t": signs["x-t"]
    }
    
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
    cookie = "abRequestId=4bcfbe0a-5cf0-501a-8ad2-0025702fb150; webBuild=4.53.0; xsecappid=xhs-pc-web; a1=19439aca0afu6iynk7jnc749io57kye6yyx8sy2p630000242698; webId=f2b076670b45953600cc23516ce9842f; gid=yj4q4YfDK014yj4q4Yf0jT9CWYIjI82CCS2dEhiyIhA0Iiq8JjiVK9888KY8WjW8WY8KWWKD; web_session=0400698c34a8f1112a5ad30c4f354bdc2f26a8; acw_tc=0ad5304717361338465407556e86a923e3bfbd1c693935183b214d8f2115b7; unread={%22ub%22:%226762d5fd000000000b016959%22%2C%22ue%22:%22677a80e7000000000b023479%22%2C%22uc%22:31}; websectiga=8886be45f388a1ee7bf611a69f3e174cae48f1ea02c0f8ec3256031b8be9c7ee; sec_poison_id=b9256bcb-0949-4a83-8005-1c775b05c60f"
    xhs_client = XhsClient(cookie, sign=sign)
    # get note info
    # note_info = xhs_client.get_note_by_id("63db8819000000001a01ead1")
    # print(datetime.datetime.now())
    # print(json.dumps(note_info, indent=2))
    # print(xhs.help.get_imgs_url_from_note(note_info))
    
    user_id = "5d40ebb90000000010037a0c"
    
    # 创建输出目录
    os.makedirs("output/result", exist_ok=True)

    # get_user_like_notes(xhs_client, user_id)
    
    get_first_normal_note(xhs_client, "normal")
    # get_first_normal_note(xhs_client, "video")
