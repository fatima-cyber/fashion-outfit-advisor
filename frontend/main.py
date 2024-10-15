import streamlit as st
import requests
import json

# Set up the Streamlit page with title, header, and description
st.set_page_config(page_title="Fashion Outfit Advisor", page_icon="👗")
st.header('Fashion Outfit Advisor')
st.write('Get personalized fashion advice for your outfits!')
st.write('[![view source code ](https://img.shields.io/badge/view_source_code-gray?logo=github)](https://github.com/fatima-cyber/fashion-outfit-advisor)')

# Function to get a new session ID from the backend
def get_new_session_id():
    url = "http://backend:8000/create-session-id"
    try:
        response = requests.post(url)
        if response.status_code == 200:
            return response.json()["session_id"]
        else:
            st.error(f"Failed to get new session ID. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        st.error(f"Error connecting to the backend: {str(e)}")
        return None

# Initialize session state for chat history and session ID
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'session_id' not in st.session_state or st.session_state.session_id is None:
    st.session_state.session_id = get_new_session_id()

# Sidebar options for starting a new chat and displaying current session ID
st.sidebar.header("Options")
new_chat = st.sidebar.button("New Chat")
if new_chat:
    st.session_state.chat_history = []
    st.session_state.session_id = get_new_session_id()

st.sidebar.text("Session ID: " + str(st.session_state.session_id))

# Display chat history if there are any previous messages
if st.session_state.chat_history:
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Function to send message to backend API and get response
def send_message(message):
    url = f"http://backend:8000/chat?session_id={st.session_state.session_id}"
    headers = {"Content-Type": "application/json"}
    data = {"message": message}
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json()["response"]
    else:
        return "Error: Unable to get response from the server."

# Function to send image to backend server for processing
def send_image_to_backend(image_bytes=None):
    url = "http://backend:8000/upload-image"
    headers = {"Content-Type": "application/octet-stream"}
    
    if image_bytes is None:
        data = json.dumps({"image": None})
        headers["Content-Type"] = "application/json"
    else:
        data = image_bytes

    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Unable to upload image to the server."}

# Main chat functionality: Get user input, process it, and display response
user_input = st.chat_input("Type your message here...")

if user_input:
    # Display user message and add to chat history
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Get and display bot response, then add to chat history
    bot_response = send_message(user_input)
    with st.chat_message("assistant"):
        st.write(bot_response)
    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})

# Image upload functionality in sidebar
uploaded_file = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"], key="small_uploader")

# Process and send uploaded image to backend
image_bytes = uploaded_file.getvalue() if uploaded_file is not None else None
response = send_image_to_backend(image_bytes)

if uploaded_file is not None:
    # Display the uploaded image in the sidebar
    st.sidebar.image(uploaded_file, caption="Uploaded Image", width=200)
