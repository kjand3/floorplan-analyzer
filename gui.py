from floorplan_analyzer.config.settings import settings
from PIL import Image
from main import run
from pathlib import Path
import streamlit as st
import glob
import os
import shutil

### This script was developed with the help of ChatGPT ###

st.set_page_config(page_title="Floorplan Analyzer Tool", layout="centered")
st.title("Floorplan Analyzer Tool")
st.image(Image.open("logo.png"))


uploaded_files = st.file_uploader(
    "Choose file(s) to upload", accept_multiple_files=True, type=["pdf", "jpg", "png"]
)

user_temp_dir = Path("user_temp")
user_temp_dir.mkdir(exist_ok=True)
settings.mode = "inference"

if uploaded_files:
    st.success(f"{len(uploaded_files)} file(s) uploaded.")
    for uploaded_file in uploaded_files:
        save_path = os.path.join(user_temp_dir, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

    if st.button("Run Inference"):
        with st.spinner("Running model inference..."):
            try:
                run("user_temp/")
                st.success("✅ Inference completed!")
                st.write("### Output:")
                result_path = settings.inference_config.results_output_path
                for file in glob.glob(result_path + "/*"):
                    image = Image.open(file)
                    st.image(image, caption="Processed Image", use_container_width=True)

            except Exception as e:
                st.error(f"Error during inference: {e}")
    if st.button("Cleanup & Reset"):
        shutil.rmtree("user_temp/")
        shutil.rmtree(settings.inference_config.results_output_path)
else:
    st.info("Please upload file(s) to begin.")
