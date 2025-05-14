import streamlit as st
import numpy as np
import os
import tempfile
from PIL import Image
import io
import time

# Import custom modules
from chatbot import ChatbotInterface
from model import SkinLesionClassifier
from image_preprocessing import preprocess_image
from utils import get_progress_placeholder, explain_prediction
from assets.info_content import (
    get_app_description,
    get_disclaimer_text,
    get_educational_content,
    get_next_steps
)
from assets.sample_images import get_example_images

# Set page configuration
st.set_page_config(
    page_title="Skin Cancer Prediction Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables if they don't exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_stage" not in st.session_state:
    st.session_state.current_stage = "introduction"
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None
if "preprocessed_image" not in st.session_state:
    st.session_state.preprocessed_image = None
if "prediction" not in st.session_state:
    st.session_state.prediction = None
if "confidence" not in st.session_state:
    st.session_state.confidence = None
if "user_responses" not in st.session_state:
    st.session_state.user_responses = {}
if "chatbot" not in st.session_state:
    st.session_state.chatbot = ChatbotInterface()

# Create main layout
st.title("Skin Cancer Prediction Assistant")

# Sidebar with information
with st.sidebar:
    st.header("About this Application")
    st.markdown(get_app_description())
    
    st.header("Important Disclaimer")
    st.warning(get_disclaimer_text())
    
    st.header("Educational Resources")
    st.markdown(get_educational_content())
    
    # Example images section 
    st.header("Example Images")
    st.caption("These are examples of the types of skin lesion images our system can analyze:")
    
    example_col1, example_col2 = st.columns(2)
    for idx, (label, image_path) in enumerate(get_example_images()):
        if idx % 2 == 0:
            with example_col1:
                st.image(image_path, caption=label, use_column_width=True)
        else:
            with example_col2:
                st.image(image_path, caption=label, use_column_width=True)

# Initialize the model
@st.cache_resource
def load_model():
    return SkinLesionClassifier()

model = load_model()

# Main content area
col1, col2 = st.columns([3, 2])

with col1:
    # Chat interface
    st.header("Chat Assistant")
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "assistant":
            with st.chat_message("assistant", avatar="🔬"):
                st.write(message["content"])
        else:
            with st.chat_message("user", avatar="👤"):
                st.write(message["content"])
    
    # Get the next chatbot message based on current stage
    if not st.session_state.chat_history or st.session_state.current_stage == "introduction":
        # Initial greeting
        welcome_msg = st.session_state.chatbot.get_welcome_message()
        st.session_state.chat_history.append({"role": "assistant", "content": welcome_msg})
        st.session_state.current_stage = "guidance"
        st.rerun()
    
    # User input
    user_input = st.chat_input("Type your message here...")
    if user_input:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Process user message based on current stage
        response, next_stage = st.session_state.chatbot.process_message(
            user_input, 
            st.session_state.current_stage, 
            st.session_state.user_responses,
            st.session_state.prediction,
            st.session_state.confidence
        )
        
        # Add chatbot response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        # Update stage if changed
        if next_stage != st.session_state.current_stage:
            st.session_state.current_stage = next_stage
        
        st.rerun()

with col2:
    # Image upload and results area
    st.header("Image Analysis")
    
    # Image upload
    uploaded_file = st.file_uploader("Upload an image of the skin lesion", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None and (st.session_state.uploaded_image is None or uploaded_file.name != st.session_state.uploaded_image.name):
        # Process the new image
        st.session_state.uploaded_image = uploaded_file
        
        # Display original image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Process image
        with st.spinner("Processing image..."):
            # Preprocess the image
            processed_img = preprocess_image(image)
            st.session_state.preprocessed_image = processed_img
            
            # Make prediction
            progress_placeholder = get_progress_placeholder(st)
            
            for percent_complete in range(0, 101, 10):
                time.sleep(0.1)  # Simulate processing time
                progress_placeholder.progress(percent_complete)
            
            prediction_result, confidence = model.predict(processed_img)
            st.session_state.prediction = prediction_result
            st.session_state.confidence = confidence
            
            # Update chat with the new information
            if prediction_result is not None:
                result_message = st.session_state.chatbot.get_prediction_message(
                    prediction_result, confidence
                )
                st.session_state.chat_history.append({"role": "assistant", "content": result_message})
                st.session_state.current_stage = "post_prediction"
        
        st.rerun()
    
    # Display prediction results if available
    if st.session_state.prediction is not None and st.session_state.confidence is not None:
        st.subheader("Prediction Results")
        
        # Visual indicator of risk level
        risk_color = "#ff0000" if st.session_state.prediction == "Melanoma" else "#00cc00"
        risk_label = "High Risk" if st.session_state.prediction == "Melanoma" else "Low Risk"
        
        st.markdown(f"""
        <div style="padding: 10px; border-radius: 5px; background-color: {risk_color}; color: white; text-align: center; margin-bottom: 15px;">
            <h3 style="margin: 0;">{risk_label}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col_result1, col_result2 = st.columns(2)
        
        with col_result1:
            st.metric("Classification", st.session_state.prediction)
        
        with col_result2:
            st.metric("Confidence", f"{st.session_state.confidence:.1f}%")
        
        # Explanation of the prediction
        st.subheader("Explanation")
        st.write(explain_prediction(st.session_state.prediction, st.session_state.confidence))
        
        # Recommendations based on prediction
        st.subheader("Recommended Next Steps")
        st.info(get_next_steps(st.session_state.prediction))
        
        # Reset button
        if st.button("Start New Analysis"):
            # Reset session state
            st.session_state.chat_history = []
            st.session_state.current_stage = "introduction"
            st.session_state.uploaded_image = None
            st.session_state.preprocessed_image = None
            st.session_state.prediction = None
            st.session_state.confidence = None
            st.session_state.user_responses = {}
            st.rerun()