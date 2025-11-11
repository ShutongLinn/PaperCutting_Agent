import os
import cv2
import numpy as np
from volcenginesdkarkruntime import Ark
from volcenginesdkarkruntime.types.images.images import SequentialImageGenerationOptions
from key import MY_API_KEY

client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=MY_API_KEY
)
image_urls = [
    "https://c-ssl.duitang.com/uploads/item/201908/20/20190820031627_qahtq.jpeg"  # 直接指向图片的URL
]

if not image_urls:
    print("⚠️ 请先将 processed 文件夹中的图片上传到可访问的 URL，然后填入 image_urls 列表。")
else:
    for img in image_urls:
        imagesResponse = client.images.generate( 
            model="doubao-seedream-4-0-250828", 
            prompt=(
                "假设你是一名剪纸图纹设计师，你的工作是把用户给的图片设计成剪纸图纹，"
                "方便用户打印之后按照上面的纹路直接进行剪纸操作。这里有一张用户给的图片，"
                "请你根据这张图片设计相应的、带颜色的剪纸纹路。"),
            image=img,
            sequential_image_generation="disabled",
            response_format="url",
            size="2K",
            stream=False,
            watermark=True
        ) 
        
        print(imagesResponse.data[0].url)

print("全部处理完成。")