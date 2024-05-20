import streamlit as st
import os
import io
import base64
import base64
from streamlit_cropper import st_cropper
from PIL import Image
from st_pages import hide_pages
from st_social_media_links import SocialMediaIcons

#### STATIC ####
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, 'logo.png')

def get_base64_of_image(image_path):
    with open(image_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode()

def add_logo():
    image_base64 = get_base64_of_image(IMAGE_PATH)
    st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] {{
                background-image: url('data:image/png;base64,{image_base64}');
                background-repeat: no-repeat;
                padding-top: 40px;
                background-position: 20px 20px;
                background-size:  90%;  /* Adjust this value to control the size */
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

#### STREAMLIT APP ####
## ADDITIONAL CONFIG ##
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

add_logo()

hide_pages(["streamlit_app", "crop", "preview", "refine", "refined", "transcription", "tips"])

# Customizing Streamlit decoration
st.markdown("""
<style>
    [data-testid="stDecoration"] {
        background-image: linear-gradient(90deg, #2ab5e8ff, #48bfebff);
    }
</style>""",
unsafe_allow_html=True)

## TITLE AND INFO ##
st.title("Upload")

st.info("**On the left-side menu, please upload the image you want to transcribe and click \"Next\"**")

# File upload and image processing
st.session_state['img_file'] = st.sidebar.file_uploader(label='Upload a file', type=['png', 'jpg'])

if st.session_state['img_file'] is not None:
    if st.sidebar.button('Next', use_container_width=True, key="next"):
        st.switch_page("pages/crop.py")

st.sidebar.divider()

## ADD EXAMPLE FILE ##
if 'example1_content' not in st.session_state: 
    example1 = os.path.join(BASE_DIR, 'examples/en-newspaper.jpg')
    with open(example1, 'rb') as file:
        st.session_state['example1_content'] = file.read()
else: pass

example = st.sidebar.expander(label="Download an example", expanded=False)
example.markdown(
    """
    <p style="text-align: justify;">
        If you don't have a document to transcribe but still want to try out the tool, you can download this example file.
    </p>
    """,
    unsafe_allow_html=True)
example.download_button(label="en-newspaper",
        data=st.session_state['example1_content'],
        file_name="en-newspaper.jpg",
        mime="image/jpg", use_container_width=True, key="example1_button")

st.sidebar.divider()

st.sidebar.markdown("""<div style="text-align: justify;"><b>OCaRctic</b> performs optical character recognition followed by AI enhanced correction using <b>Snowflake Arctic</b> and is hosted by <b>Streamlit</b>.</div>""", unsafe_allow_html=True)

st.sidebar.divider()
st.sidebar.markdown("""<div style="text-align: center;"><b>João L. Neto</b></div>""", unsafe_allow_html=True)

social_media_links = ["https://github.com/jlnetosci"]
colors = ["#ffffff"]

social_media_icons = SocialMediaIcons(social_media_links, colors)
social_media_icons.render(sidebar=True, justify_content="center")