import streamlit as st
import os
import base64
import random

SUPPORTED_FORMATS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')

def get_image_files(folder_path):
    return [file for file in os.listdir(folder_path) if file.lower().endswith(SUPPORTED_FORMATS)]

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def main():
    st.title("🖼️ 經典名椅互動畫展")

    img_folder = "img"
    if not os.path.exists(img_folder):
        st.error("找不到圖片資料夾")
        return

    image_files = get_image_files(img_folder)
    if not image_files:
        st.warning("沒有找到任何圖片")
        return

    # 隨機順序排列
    random.shuffle(image_files)

    # 將所有圖片轉 base64 給前端用 JS 播放
    images_base64 = [
        f"data:image/{img.split('.')[-1]};base64,{encode_image_to_base64(os.path.join(img_folder, img))}"
        for img in image_files
    ]

    image_names = image_files  # 保留原始檔名對應

    # 傳到 HTML 中播放 + 下載功能
    st.components.v1.html(f"""
    <div style="text-align: center;">
        <img id="slideshow" src="" style="max-width: 90%; max-height: 80vh; border-radius: 8px; cursor: pointer;" />
        <br/>
        <a id="downloadLink" download style="display: inline-block; margin-top: 10px; font-size: 1.1em;">⬇️ 下載目前圖片</a>
    </div>
    <script>
        const images = {images_base64};
        const imageNames = {image_names};
        let index = 0;
        const imgTag = document.getElementById("slideshow");
        const downloadLink = document.getElementById("downloadLink");

        function updateImage() {{
            imgTag.src = images[index];
            downloadLink.href = images[index];
            downloadLink.download = imageNames[index];
            index = (index + 1) % images.length;
        }}

        // 每 200ms 換一張圖
        setInterval(updateImage, 200);

        // 點圖片就觸發下載
        imgTag.addEventListener("click", () => {{
            downloadLink.click();
        }});

        // 初始化
        updateImage();
    </script>
    """, height=600)

if __name__ == "__main__":
    main()
