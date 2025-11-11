import os
import cv2
import numpy as np
from upload import batch_upload

LOCAL_IMAGE_PATH = "denoise/"
REMOTE_IMAGE_NAME = "imgs/"

def preprocess_image(img_path, save_path):
    """对输入图片进行去噪和边缘检测"""
    img = cv2.imread(img_path)
    if img is None:
        print(f"⚠️ 无法读取图片：{img_path}")
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    denoised = cv2.GaussianBlur(gray, (5, 5), 0)
    # edges = cv2.Canny(denoised, threshold1=50, threshold2=150)
    cv2.imwrite(save_path, denoised)
    return save_path

# 批量处理所有图片
def batch_processing(INPUT_DIR, OUTPUT_DIR):
    edge_images = []
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff")):
            input_path = os.path.join(INPUT_DIR, filename)
            output_path = os.path.join(OUTPUT_DIR, f"edge_{filename}")
            processed = preprocess_image(input_path, output_path)
            if processed:
                edge_images.append(processed)

    print(f"完成 {len(edge_images)} 张图片的边缘提取。")

if __name__ == "__main__":
    batch_processing("./raw_imgs", "./denoise")
    image_url = batch_upload(LOCAL_IMAGE_PATH, REMOTE_IMAGE_NAME)