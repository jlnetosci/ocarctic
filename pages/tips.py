import streamlit as st
import os
import io
import base64
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
st.set_page_config(initial_sidebar_state="expanded")

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
st.title("Tips")

st.subheader("#1")
st.write("When selecting the cropping area allow the page to process, it takes less than a second but mis-processing might lead to errors.")

st.subheader("#2")
st.write("The quality of the transcription is highly dependent on the crop. Crops with high contrating areas that are not characters might induce noise in the transcription. A couple of examples:")

st.image("img/unadvised_crop.png", use_column_width=True)
st.write("The image above shows an unadvised crop. It presents a high contrasting horizontal line (top), vertical lines (left and right), and partially cut characters (bottom).")

st.image("img/good_crop.png", use_column_width=True)
st.write("A good crop. Focused on characters only.")

st.subheader("#3")
st.write("If you see words or expressions you do not recognize in our AI-enhanced correction, please converse with the AI to get clearer results.")

st.sidebar.markdown("""<div style="text-align: justify;"><b>OCaRctic</b> performs optical character recognition followed by AI enhanced correction using <b>Snowflake Arctic</b> and is hosted by <b>Streamlit</b>.</div>""", unsafe_allow_html=True)

st.sidebar.divider()
st.sidebar.markdown("""<div style="text-align: center;"><b>João L. Neto</b></div>""", unsafe_allow_html=True)

social_media_links = ["https://github.com/jlnetosci"]
colors = ["#ffffff"]

social_media_icons = SocialMediaIcons(social_media_links, colors)
social_media_icons.render(sidebar=True, justify_content="center")