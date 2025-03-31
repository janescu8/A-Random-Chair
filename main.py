import streamlit as st
import os
import random
from PIL import Image

SUPPORTED_FORMATS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')

def get_image_files(folder_path):
    return [file for file in os.listdir(folder_path) if file.lower().endswith(SUPPORTED_FORMATS)]

def main():
    st.title("🪑泡泡 × 經典名椅系列")
    img_folder = "img"

    if not os.path.exists(img_folder):
        st.error(f"找不到資料夾: {img_folder}")
        return

    image_files = get_image_files(img_folder)

    if not image_files:
        st.warning("資料夾裡沒有支援的圖片格式。")
        return

    # 初始化 session state
    if "current_image" not in st.session_state:
        st.session_state.current_image = random.choice(image_files)

    # 按鈕：抽一張新圖片
    if st.button("🔁 抽另一個主題"):
        st.session_state.current_image = random.choice(image_files)

    selected_image = st.session_state.current_image
    image_path = os.path.join(img_folder, selected_image)

    st.subheader(f"你抽到的圖片是：`{selected_image}`")
    st.image(Image.open(image_path), use_container_width=True)

if __name__ == "__main__":
    main()
