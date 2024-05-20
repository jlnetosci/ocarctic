import streamlit as st
import os
import io
import base64
from streamlit_cropper import st_cropper
from PIL import Image
from st_pages import hide_pages
from st_social_media_links import SocialMediaIcons

#### STATIC ####
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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

#### FUNCTIONS ####

#### STREAMLIT APP ####
## ADDITIONAL CONFIG ##
st.set_page_config(initial_sidebar_state="expanded")

add_logo()

hide_pages(["streamlit_app", "crop", "preview", "refine", "refined", "transcription", "tips"])

# Customize stDecoration colors
st.markdown("""
<style>
    [data-testid="stDecoration"] {
        background-image: linear-gradient(90deg, #2ab5e8ff, #48bfebff);
    }
</style>""",
unsafe_allow_html=True)

## TITLE AND INFO ##
st.title("Refined selection")

st.info("**This is a preview of your refined selection. Please choose an option of the menu to proceed.**")

## APP BODY ##
if 'refined_selection' not in st.session_state:
    st.error("❌ There was an error. No refined selection found. Please go back.")

    one_of_five, two_of_five, three_of_five, four_of_five, five_of_five = st.columns([2, 3, 3, 3, 2])

    with three_of_five:
        if st.button('Back', use_container_width=True):
            st.switch_page("streamlit_app.py")

else:
    # Save cropped image to BytesIO buffer
    cropped_buffer = io.BytesIO()
    st.session_state['refined_selection'].save(cropped_buffer, format='PNG')
    cropped_data = cropped_buffer.getvalue()
    
    # Display the cropped image
    #width larger than height
    if st.session_state['refined_selection'].size[0] >= st.session_state['refined_selection'].size[1]:
        width=700
    else: #height larger than height
        width=int(round(st.session_state['refined_selection'].size[0]*700/st.session_state['refined_selection'].size[1], 0))

    st.image(cropped_data, width=width, use_column_width="always")

    st.sidebar.write("Please select an option:")

    if st.sidebar.button("Reupload image", use_container_width=True, key="reupload_image"):
        st.switch_page("streamlit_app.py")

    if st.sidebar.button("Back", use_container_width=True, key="back"):
        st.switch_page("pages/refine.py")

    if st.sidebar.button("Transcribe", use_container_width=True, key="transcribe"):
        st.switch_page("pages/transcription.py")

st.sidebar.divider()

st.sidebar.markdown("""<div style="text-align: justify;"><b>OCaRctic</b> performs optical character recognition followed by AI enhanced correction using <b>Snowflake Arctic</b> and is hosted by <b>Streamlit</b>.</div>""", unsafe_allow_html=True)

st.sidebar.divider()
st.sidebar.markdown("""<div style="text-align: center;"><b>João L. Neto</b></div>""", unsafe_allow_html=True)

social_media_links = ["https://github.com/jlnetosci"]
colors = ["#ffffff"]

social_media_icons = SocialMediaIcons(social_media_links, colors)
social_media_icons.render(sidebar=True, justify_content="center")