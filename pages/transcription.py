import streamlit as st
import os
import io
import base64
import pytesseract
import requests
import json
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

def call_ai_api(text, instruction):
    quiqui = os.environ["QUIQUI"]

    url = "https://api.together.xyz/inference"
    payload = {
        "model": "Snowflake/snowflake-arctic-instruct",
        "prompt": f"{instruction}\n{text}",
        "max_tokens": 1500,
        "temperature": 0.3,
        "top_p": 0.9,
        "top_k": 5,
        "repetition_penalty": 1
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {quiqui}"
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    result = response.json()
    txt = result["output"]["choices"][0]["text"]
    return txt

def ai_correction():
    instruction = """
    Correct this sentence. Please don't add any other words.
    """
    try:
        if 'text' in st.session_state:
            st.session_state['ai_corrected_text'] = call_ai_api(st.session_state['text'], instruction)
        st.session_state['latest_correction'] = st.session_state['ai_corrected_text']
    except Exception as e:
        st.error(f"Error in AI-enhanced correction: {e}")

def download_corrected_text():
    if 'latest_correction' in st.session_state:
        text_to_download = st.session_state['latest_correction']
        st.download_button(
            label="Download corrected text",
            data=text_to_download,
            file_name="corrected_text.txt",
            mime="text/plain"
        )

def add_chat_interface():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    def update_chat():
        user_message = st.session_state.user_input
        st.session_state.chat_history.append({"role": "user", "message": user_message})
        ai_response = call_ai_api(st.session_state['latest_correction'] + "\n\nUser: " + user_message, "")
        st.session_state.chat_history.append({"role": "ai", "message": ai_response})
        st.session_state.user_input = ""  # Clear input field

    # Display chat history
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(f"**You:** {chat['message']}")
        else:
            st.markdown(f"{chat['message']}")

    # User input for new query
    st.text_input("Ask the AI about specific words or sentences:", key="user_input", on_change=update_chat)

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

style = "<style>h2 {text-align: center;}</style>"
st.markdown(style, unsafe_allow_html=True)

## TITLE AND INFO ##
st.title("Transcription")

st.info("**Your text will be transcribed in this page below your selected image. If your input is long, please be patient. You can interact with the AI for assistance.**")

## APP BODY ##
if 'cropped_img' not in st.session_state and 'refined_selection' not in st.session_state:
    st.error("❌ There was an error. No cropped image found. Please go back.")

    one_of_five, two_of_five, three_of_five, four_of_five, five_of_five = st.columns([2, 3, 3, 3, 2])

    with three_of_five:
        if st.button('Back', use_container_width=True):
            st.switch_page("streamlit_app.py")

elif 'refined_selection' in st.session_state:
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

    st.image(cropped_data, width=width, use_column_width="never")

    if "text" not in st.session_state:
        st.session_state['text'] = pytesseract.image_to_string(st.session_state['refined_selection']).replace('\f', '')
    st.write(st.session_state['text'])

    if st.sidebar.button("✨ AI-enhanced correction", use_container_width=True, key="ai"):
        st.session_state['correction_mode'] = 'ai'
        ai_correction()

else:
    cropped_buffer = io.BytesIO()
    st.session_state['cropped_img'].save(cropped_buffer, format='PNG')
    cropped_data = cropped_buffer.getvalue()
    
    # Display the cropped image
    #width larger than height
    if st.session_state['cropped_img'].size[0] >= st.session_state['cropped_img'].size[1]:
        width=700
    else: #height larger than height
        width=int(round(st.session_state['cropped_img'].size[0]*700/st.session_state['cropped_img'].size[1], 0))

    st.image(cropped_data, width=width, use_column_width="never")

    st.session_state['text'] = pytesseract.image_to_string(st.session_state['cropped_img'])
    st.write(st.session_state['text'])

    if st.sidebar.button("✨ AI-enhanced correction", use_container_width=True, key="ai"):
        st.session_state['correction_mode'] = 'ai'
        ai_correction()

# Check if AI-enhanced correction mode is active
if st.session_state.get('correction_mode') == 'ai':
    st.subheader("AI-enhanced correction")
    if 'ai_corrected_text' in st.session_state:
        st.write(st.session_state['ai_corrected_text'])
    download_corrected_text()
    add_chat_interface()

st.sidebar.divider()

st.sidebar.markdown("""<div style="text-align: justify;"><b>OCaRctic</b> performs optical character recognition followed by AI enhanced correction using <b>Snowflake Arctic</b> and is hosted by <b>Streamlit</b>.</div>""", unsafe_allow_html=True)

st.sidebar.divider()
st.sidebar.markdown("""<div style="text-align: center;"><b>João L. Neto</b></div>""", unsafe_allow_html=True)

social_media_links = ["https://github.com/jlnetosci"]
colors = ["#ffffff"]

social_media_icons = SocialMediaIcons(social_media_links, colors)
social_media_icons.render(sidebar=True, justify_content="center")