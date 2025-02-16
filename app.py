# Python In-built packages
from pathlib import Path
import PIL

# External packages
import streamlit as st

# Local Modules
import settings
import helper

# Setting page layout
st.set_page_config(
    page_title="Object Detection using YOLOv8",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page heading
st.markdown(
    """
    <div style="background-color:  gray; padding: 5px; border-radius: 2px;">
        <h1 style="color: yellow; font-size: 50px; font-weight: bold; text-align: center;">
            Object Detection & Tracking using YOLOv8
        </h1>
    </div>
    """, 
    unsafe_allow_html=True
)


# '''Modify Team member'''
# Styling function to avoid repetitive code
def create_row(role, name, id, bg_color, font_color):
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; 
                    align-items: center; background-color: {bg_color}; 
                    padding: 10px; border-radius: 8px; font-size: 25px;">
            <span style="font-weight: bold; color: {font_color};">{role}</span>
            <span style="font-weight: bold; color: {font_color};">{name}</span>
            <span style="font-weight: bold; color: {font_color};">ID: {id}</span>
        </div>
        """, 
        unsafe_allow_html=True
    )


# Create rows with different roles, colors, and appropriate font colors
create_row("Team Leader:", "Md. An Nahian Prince", "12105007", 
          "#0d47a1", "#ffffff")  # Dark blue background with white text


create_row("Team Assistant:", "Shithi Rani Roy", "12105009", 
           "#fff8cc", "#705600")  # Yellowish background with dark yellow text

create_row("Team Assistant:", "Ramjan Hossain", "12005034", 
           "#fff8cc", "#705600")  # Yellowish background with dark yellow text

# Sidebar
st.sidebar.header("Machine Learning Model Config.")

# Model Options
model_type = st.sidebar.radio(
    "Select Format", ['Detection', 'Segmentation'])

confidence = float(st.sidebar.slider(
    "Select Model Confidence Level", 1, 100, 40)) / 100
# min: 1 -> max: 100 -> default: 40 result in percentage

# Selecting Detection Or Segmentation
if model_type == 'Detection':
    model_path = Path(settings.DETECTION_MODEL)
elif model_type == 'Segmentation':
    model_path = Path(settings.SEGMENTATION_MODEL)

# Load Pre-trained ML Model
try:
    model = helper.load_model(model_path)
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)

st.sidebar.header("Image/Video Configuration")
source_radio = st.sidebar.radio(
    "Select Source", settings.SOURCES_LIST)

source_img = None
# If image is selected
if source_radio == settings.IMAGE:
    source_img = st.sidebar.file_uploader(
        "Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

    col1, col2 = st.columns(2)

    with col1:
        try:
            if source_img is None:
                default_image_path = str(settings.DEFAULT_IMAGE)
                default_image = PIL.Image.open(default_image_path)
                st.image(default_image_path, caption="Default Image",
                         use_column_width=True)
            else:
                uploaded_image = PIL.Image.open(source_img)
                st.image(source_img, caption="Uploaded Image",
                         use_column_width=True)
        except Exception as ex:
            st.error("Error occurred while opening the image.")
            st.error(ex)

    with col2:
        if source_img is None:
            default_detected_image_path = str(settings.DEFAULT_DETECT_IMAGE)
            default_detected_image = PIL.Image.open(
                default_detected_image_path)
            st.image(default_detected_image_path, caption='Detected Image',
                     use_column_width=True)
        else:
            if st.sidebar.button('Detect Objects'):
                res = model.predict(uploaded_image,
                                    conf=confidence
                                    )
                boxes = res[0].boxes
                res_plotted = res[0].plot()[:,:,::-1]
                st.image(res_plotted, caption='Detected Image',
                         use_column_width=True)
                try:
                    with st.expander("Detection Results"):
                        for box in boxes:
                            st.write(box.data)
                except Exception as ex:
                    # st.write(ex)
                    st.write("No image is uploaded yet!")

elif source_radio == settings.VIDEO:
    helper.play_stored_video(confidence, model)

elif source_radio == settings.WEBCAM:
    helper.play_webcam(confidence, model)

elif source_radio == settings.YOUTUBE:
    helper.play_youtube_video(confidence, model)

else:
    st.error("Please select a valid source type!")
