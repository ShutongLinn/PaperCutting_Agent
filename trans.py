from volcenginesdkarkruntime import Ark
from volcenginesdkarkruntime.types.images.images import SequentialImageGenerationOptions
from key import MY_API_KEY

PROMPT = """
目前剪纸爱好者不断增多，一般剪纸爱好者会上网搜索剪纸图纹，然后直接下载并打印出来，按照打印的纹路开始剪裁。对于这些爱好者来说，最难的是寻找剪纸图纹。
假设你是一名平面剪纸图纹设计师，你的工作是根据用户提供的图片，将其设计成平面剪纸图纹，方便用户下载打印，然后进行剪纸操作。

这里有一张用户给的图片，请你根据这张图片设计相应的的剪纸纹路。\n
注意: 
1.生成的纹路只有一层，即无空间层次的。
2.对于复杂图案可以适当简化。
"""

client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=MY_API_KEY
)

image_urls = [
    "https://raw.githubusercontent.com/ShutongLinn/PaperCutting_Agent/main/imgs/edge_animal.jpeg"  # 直接指向图片的URL
]

if not image_urls:
    print("⚠️ 请先将 processed 文件夹中的图片上传到可访问的 URL，然后填入 image_urls 列表。")
else:
    for img in image_urls:
        imagesResponse = client.images.generate( 
            model="doubao-seedream-4-0-250828", 
            prompt=PROMPT,
            image=img,
            sequential_image_generation="disabled",
            response_format="url",
            size="2K",
            stream=False,
            watermark=True
        ) 
        
        print(imagesResponse.data[0].url)

print("全部处理完成。")