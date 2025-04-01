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
    st.set_page_config(page_title="經典名椅互動畫展", layout="centered")
    st.title("🪑 經典名椅互動畫展")

    img_folder = "img"
    if not os.path.exists(img_folder):
        st.error("找不到圖片資料夾")
        return

    image_files = get_image_files(img_folder)
    if not image_files:
        st.warning("沒有找到任何圖片")
        return

    random.shuffle(image_files)

    images_base64 = [
        f"data:image/{img.split('.')[-1]};base64,{encode_image_to_base64(os.path.join(img_folder, img))}"
        for img in image_files
    ]
    image_names = image_files

    st.components.v1.html(f"""
    <style>
        .pretty-button {{
            padding: 15px 30px;
            font-size: 20px;
            background-color: #4a4a8a;
            color: white;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }}
        .pretty-button:hover {{
            background-color: #3c3c75;
            transform: scale(1.05);
        }}
        #slideshow {{
            margin-top: 20px;
        }}
    </style>

    <div style="text-align:center;">
        <div id="startSection">
            <button class="pretty-button" onclick="startSlideshow()">🎮 開始玩</button>
        </div>

        <img id="slideshow" src="" style="max-width: 90%; max-height: 80vh; border-radius: 8px; cursor: pointer; display: none;" />
        <a id="downloadLink" download style="display:none;"></a>

        <div id="continueSection" style="margin-top: 20px; display:none;">
            <button class="pretty-button" onclick="resumeSlideshow()">🔄 繼續玩</button>
        </div>
    </div>

    <script>
        const images = {images_base64};
        const names = {image_names};
        let index = 0;
        let intervalId = null;

        const img = document.getElementById("slideshow");
        const downloadLink = document.getElementById("downloadLink");
        const continueSection = document.getElementById("continueSection");
        const startSection = document.getElementById("startSection");

        function showImage() {{
            img.src = images[index];
            downloadLink.href = images[index];
            downloadLink.download = names[index];
        }}

        function startSlideshow() {{
            startSection.style.display = "none";
            img.style.display = "block";
            showImage();
            intervalId = setInterval(() => {{
                index = (index + 1) % images.length;
                showImage();
            }}, 100);  // 每 0.1 秒切換
        }}

        function stopSlideshow() {{
            clearInterval(intervalId);
            intervalId = null;
        }}

        function resumeSlideshow() {{
            continueSection.style.display = "none";
            intervalId = setInterval(() => {{
                index = (index + 1) % images.length;
                showImage();
            }}, 100);
        }}

        img.addEventListener("click", () => {{
            stopSlideshow();
            downloadLink.click();
            continueSection.style.display = "block";
        }});
    </script>
    """, height=700)

if __name__ == "__main__":
    main()
