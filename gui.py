import glob
import os
import shutil
import atexit 
import sys
from pathlib import Path

import streamlit as st
from PIL import Image

from floorplan_analyzer.config.settings import settings, ModeEnum
from main import run

# This script was developed with the help of ChatGPT
st.set_page_config(page_title="Floorplan Analyzer", layout="centered")
st.title("Floorplan Analyzer")
st.image(Image.open("logo.png"))


# Show user input file options
uploaded_files = st.file_uploader(
    "Choose file(s) to upload", accept_multiple_files=True, type=["pdf", "jpg", "png"]
)


# Create temporary directories to show results
user_temp_dir = Path("user_temp")
user_temp_dir.mkdir(exist_ok=True)
settings.mode = ModeEnum.INFERENCE
results_path = settings.inference_config.results_output_path
settings.data_config.raw_data_path = str(user_temp_dir)



def cleanup_temp_dir():
    if os.path.exists(user_temp_dir):
        shutil.rmtree(user_temp_dir)        
    sys.exit(0)

atexit.register(cleanup_temp_dir)


# inference the floor plan analyzer after files are uploaded
if uploaded_files:
    st.success(f"{len(uploaded_files)} file(s) uploaded.")
    for uploaded_file in uploaded_files:
        save_path = os.path.join(user_temp_dir, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

    if st.button("Run Inference"):
        with st.spinner("Running model inference..."):
            try:
                run(settings)
                st.success("Inference completed!")
                st.write("### Output:")
                for file in glob.glob(results_path + "/*"):
                    image = Image.open(file)
                    st.image(image, use_container_width=True)

            except Exception as e:
                st.error(f"Error during inference: {e}")
    if st.button("Cleanup & Reset"):
        shutil.rmtree("user_temp/")
        shutil.rmtree(settings.inference_config.results_output_path)
else:
    st.info("Please upload file(s) to begin.")



