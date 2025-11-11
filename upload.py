import base64
import requests
import os
from key import GITHUB_TOKEN

USERNAME = "ShutongLinn"
REPO_NAME = "PaperCutting_Agent"
BRANCH = "main"

def get_file_sha(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['sha']
    elif response.status_code == 404:
        # 文件不存在
        return None
    else:
        print(f"Failed to check file existence: {response.json().get('message', 'Unknown error')}")
        return None


def upload_image_to_github(local_path, remote_name):
    # 1. 读取本地图片并转换为Base64
    with open(local_path, "rb") as f:
        image_data = f.read()
    base64_data = base64.b64encode(image_data).decode("utf-8")

    # 2. 构造GitHub API请求参数
    url = f"https://api.github.com/repos/{USERNAME}/{REPO_NAME}/contents/{remote_name}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "message": f"Upload {remote_name}",  # 提交信息
        "content": base64_data,              # Base64编码的图片内容
        "branch": BRANCH
    }
    sha = get_file_sha(url, headers)
    if sha is not None:
        data["sha"] = sha

    # 3. 发送请求（如果文件已存在，会自动覆盖）
    response = requests.put(url, json=data, headers=headers)
    result = response.json()

    # 4. 处理响应，返回图片直接访问链接
    if response.status_code in [201, 200]:
        raw_url = result["content"]["download_url"]
        return raw_url
    else:
        print(f"上传失败：{result.get('message', '未知错误')}")
        return None
    
# 批量上传所有图片
def batch_upload(LOCAL_DIR, REMOTE_DIR):
    img_url = []
    for filename in os.listdir(LOCAL_DIR):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff")):
            input_path = os.path.join(LOCAL_DIR, filename)
            output_path = os.path.join(REMOTE_DIR, f"edge_{filename}")
            processed = upload_image_to_github(input_path, output_path)
            if processed:
                img_url.append(processed)

    print(f"完成 {len(img_url)} 张图片的上传。")
    print(f"图片链接：{img_url}")
    return img_url
