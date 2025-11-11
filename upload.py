import base64
import requests
from key import GITHUB_TOKEN

# 配置参数（替换为你的信息）
USERNAME = "ShutongLinn"
REPO_NAME = "PaperCutting_Agent"
BRANCH = "main"

LOCAL_IMAGE_PATH = "imgs/animal.jpeg"
REMOTE_IMAGE_NAME = "imgs/animal.jpeg"


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

    # 3. 发送请求（如果文件已存在，会自动覆盖）
    response = requests.put(url, json=data, headers=headers)
    result = response.json()

    # 4. 处理响应，返回图片直接访问链接
    if response.status_code in [201, 200]:
        # 成功：返回raw.githubusercontent.com格式的链接
        raw_url = result["content"]["download_url"]
        print(f"上传成功！图片链接：{raw_url}")
        return raw_url
    else:
        print(f"上传失败：{result.get('message', '未知错误')}")
        return None


# 调用函数上传图片
if __name__ == "__main__":
    image_url = upload_image_to_github(LOCAL_IMAGE_PATH, REMOTE_IMAGE_NAME)
    # 上传成功后，可直接将image_url用于你的豆包API调用
    if image_url:
        print("可用于豆包API的图片链接：", image_url)
