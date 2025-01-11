import re
import os
import requests
from bs4 import BeautifulSoup

def get_meta_tag_by_key(key, tags):
    """获取指定key的meta标签内容"""
    result = []
    for tag in tags:
        if tag.get("name") == key:
            result.append(tag.get("content"))
    if len(result) == 0:
        return ['']
    return result

def parse_share_link(share_info: str, save_html: bool = True) -> dict:
    """
    解析小红书分享链接，获取帖子详情
    
    Args:
        share_info: 分享链接文本，例如："http://xhslink.com/a/vUTC3L6EXo12，复制本条信息，打开【小红书】App查看精彩内容！"
        save_html: 是否保存HTML到本地文件（默认为True，但会在解析完成后删除）
        
    Returns:
        dict: 包含帖子标题、内容、图片等信息的字典
    """
    # 确保输出目录存在
    os.makedirs("output/result", exist_ok=True)
    
    # 提取分享链接
    url = re.search(r'http://xhslink\.com/a/\w+', share_info)
    if not url:
        raise ValueError("无效的分享链接")
    
    url = url.group(0)
    print(f"解析分享链接成功: {url}")
    
    last_path = url.split("/")[-1].split("?")[0]
    html = ""
    
    # 检查本地是否存在
    html_file = f"output/result/share_link_{last_path}.html"
    if os.path.exists(html_file):
        print(f"本地已存在 {html_file}")
        with open(html_file, "r", encoding="utf-8") as f:
            html = f.read()
    else:
        html = requests.get(url).text
        
    if save_html:
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"分享链接已保存到 {html_file}")
    
    try:
        # 解析HTML
        beautiful_html = BeautifulSoup(html, "html.parser")
        meta_tags = beautiful_html.find_all("meta")
        
        # 提取meta信息
        post_title = get_meta_tag_by_key("og:title", meta_tags)[0]
        post_content = get_meta_tag_by_key("description", meta_tags)[0]
        post_images = get_meta_tag_by_key("og:image", meta_tags)
        post_type = get_meta_tag_by_key("og:type", meta_tags)[0]

        post_comment_count = get_meta_tag_by_key("og:xhs:note_comment", meta_tags)[0]
        post_like_count = get_meta_tag_by_key("og:xhs:note_like", meta_tags)[0]
        post_collect_count = get_meta_tag_by_key("og:xhs:note_collect", meta_tags)[0]
        post_video_time = get_meta_tag_by_key("og:videotime", meta_tags)[0]
        post_video_quality = get_meta_tag_by_key("og:videoquality", meta_tags)[0]
        post_video_url = get_meta_tag_by_key("og:video", meta_tags)[0]
        
        # 提取用户名
        username_tag = beautiful_html.find("span", class_="username")
        username = username_tag.text if username_tag else ""
        
        result = {
            "post_title": post_title,
            "post_content": post_content,
            "post_images": post_images,
            "post_type": post_type,
            "username": username,
            "post_comment_count": post_comment_count,
            "post_like_count": post_like_count,
            "post_collect_count": post_collect_count,
            "post_video_time": post_video_time,
            "post_video_quality": post_video_quality,
            "post_video_url": post_video_url
        }
        
        print("解析结果:")
        for key, value in result.items():
            print(f"{key}: {value}")
            
        return result
    finally:
        # 无论解析是否成功，都删除临时HTML文件
        if os.path.exists(html_file):
            os.remove(html_file)
            print(f"已删除临时文件: {html_file}")

if __name__ == '__main__':
    # 示例使用
    share_info = "http://xhslink.com/a/vUTC3L6EXo12，复制本条信息，打开【小红书】App查看精彩内容！"
    parse_share_link(share_info) 