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
st.title("Crop image")

st.info("**Select the area of the image you want to crop and transcribe. You will be able to preview and refine your selection. If you want some additional guidance please visit our [tips](tips) page.**")

## APP BODY ##
if 'img_file' not in st.session_state:
	st.error("❌ There was an error. No image found. Please go back.")

	one_of_five, two_of_five, three_of_five, four_of_five, five_of_five = st.columns([2, 3, 3, 3, 2])

	with three_of_five:
		if st.button('Back', use_container_width=True):
			st.switch_page("streamlit_app.py")

else:
	one_of_three, two_of_three, three_of_three = st.columns([2, 2.79, 2])
	with two_of_three:
		if st.session_state['img_file']:
			img = Image.open(st.session_state['img_file'])

			# Get a cropped image from the frontend
			st.session_state['cropped_img'] = st_cropper(img, box_color="#0f6787ff", stroke_width=5)

			st.sidebar.markdown(
				"""
				<p style="text-align: justify;">
					Select the area of interest and press:
				</p>
				""",
				unsafe_allow_html=True)


			# Add a 'Crop' button to finalize the crop
			if st.sidebar.button('Crop', use_container_width=True, key="sidebar_crop"):
				st.switch_page("pages/preview.py")

st.sidebar.divider()

st.sidebar.markdown("""<div style="text-align: justify;"><b>OCaRctic</b> performs optical character recognition followed by AI enhanced correction using <b>Snowflake Arctic</b> and is hosted by <b>Streamlit</b>.</div>""", unsafe_allow_html=True)

st.sidebar.divider()
st.sidebar.markdown("""<div style="text-align: center;"><b>João L. Neto</b></div>""", unsafe_allow_html=True)

social_media_links = ["https://github.com/jlnetosci"]
colors = ["#ffffff"]

social_media_icons = SocialMediaIcons(social_media_links, colors)
social_media_icons.render(sidebar=True, justify_content="center")