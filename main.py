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
    st.set_page_config(page_title="北歐現代畫展", layout="centered")
    st.title("🌿 北歐現代｜經典名椅互動畫展")

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
            font-size: 18px;
            background-color: #4a4a8a;
            color: white;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
            margin: 10px;
        }}
        .pretty-button:hover {{
            background-color: #3c3c75;
            transform: scale(1.05);
        }}
        #muteToggle {{
            position: fixed;
            top: 15px;
            right: 20px;
            font-size: 24px;
            cursor: pointer;
            background: none;
            border: none;
        }}
    </style>

    <div style="text-align:center;">
        <button id="muteToggle" onclick="toggleMute()">🔊</button>

        <div id="startSection">
            <button class="pretty-button" onclick="startSlideshow()">🎮 開始玩</button>
        </div>

        <img id="slideshow" src="" style="max-width: 90%; max-height: 80vh; border-radius: 8px; cursor: pointer; display: none;" />
        <a id="downloadLink" download style="display:none;"></a>

        <div id="pauseOptions" style="margin-top: 20px; display:none;">
            <button class="pretty-button" onclick="downloadImage()">⬇️ 下載這張圖片</button>
            <button class="pretty-button" onclick="resumeSlideshow()">🔄 繼續玩</button>
        </div>

        <!-- 音樂與音效 -->
        <audio id="bgm" src="/static/sounds/bgm.mp3" loop></audio>
        <audio id="clickSound" src="/static/sounds/click.mp3"></audio>
        <audio id="downloadSound" src="/static/sounds/download.mp3"></audio>
    </div>

    <script>
        const images = {images_base64};
        const names = {image_names};
        let index = 0;
        let intervalId = null;
        let isMuted = false;

        const img = document.getElementById("slideshow");
        const downloadLink = document.getElementById("downloadLink");
        const pauseOptions = document.getElementById("pauseOptions");
        const startSection = document.getElementById("startSection");
        const bgm = document.getElementById("bgm");
        const clickSound = document.getElementById("clickSound");
        const downloadSound = document.getElementById("downloadSound");
        const muteToggle = document.getElementById("muteToggle");

        function showImage() {{
            img.src = images[index];
            downloadLink.href = images[index];
            downloadLink.download = names[index];
        }}

        function startSlideshow() {{
            startSection.style.display = "none";
            img.style.display = "block";
            showImage();
            if (!isMuted) {{
                bgm.play();
            }}
            intervalId = setInterval(() => {{
                index = (index + 1) % images.length;
                showImage();
            }}, 100);
        }}

        function stopSlideshow() {{
            clearInterval(intervalId);
            intervalId = null;
        }}

        function resumeSlideshow() {{
            pauseOptions.style.display = "none";
            intervalId = setInterval(() => {{
                index = (index + 1) % images.length;
                showImage();
            }}, 100);
        }}

        function downloadImage() {{
            if (!isMuted) {{
                downloadSound.play();
            }}
            downloadLink.click();
        }}

        img.addEventListener("click", () => {{
            stopSlideshow();
            pauseOptions.style.display = "block";
            if (!isMuted) {{
                clickSound.play();
            }}
        }});

        function toggleMute() {{
            isMuted = !isMuted;
            bgm.muted = isMuted;
            clickSound.muted = isMuted;
            downloadSound.muted = isMuted;
            muteToggle.innerText = isMuted ? "🔇" : "🔊";
        }}
    </script>
    """, height=750)

if __name__ == "__main__":
    main()
