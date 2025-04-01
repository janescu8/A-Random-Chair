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
    <div style="text-align:center;">
        <img id="slideshow" src="" style="max-width: 90%; max-height: 80vh; border-radius: 8px; cursor: pointer;" />
        <br/>
        <a id="downloadLink" download style="display:none;"></a>
        <div id="continueSection" style="margin-top: 20px; display:none;">
            <button onclick="resumeSlideshow()" style="padding:10px 20px; font-size:16px;">🔄 繼續玩</button>
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

        function showImage() {{
            img.src = images[index];
            downloadLink.href = images[index];
            downloadLink.download = names[index];
        }}

        function startSlideshow() {{
            intervalId = setInterval(() => {{
                index = (index + 1) % images.length;
                showImage();
            }}, 200);
        }}

        function stopSlideshow() {{
            clearInterval(intervalId);
            intervalId = null;
        }}

        function resumeSlideshow() {{
            continueSection.style.display = "none";
            startSlideshow();
        }}

        img.addEventListener("click", () => {{
            stopSlideshow();
            downloadLink.click();
            continueSection.style.display = "block";
        }});

        // 初始化
        showImage();
        startSlideshow();
    </script>
    """, height=650)

if __name__ == "__main__":
    main()
