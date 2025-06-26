import streamlit as st
import google.generativeai as genai
import os

# Set up your API Key
# IMPORTANT: Your API Key is already inserted here.
os.environ["GOOGLE_API_KEY"] = "AIzaSyC31Ty3oNZFvB-qLmC_DL3M9FjwP-DzTD0"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# --- UI/UX Design Principles for Sasi AI Studio ---

st.set_page_config(
    page_title="Sasi AI Studio",
    page_icon="✨", # A little sparkle for a nice touch
    layout="centered",
    initial_sidebar_state="auto"
)

# 1. Clarity & Branding
st.title("✨ Sasi AI Studio ✨")
st.write("ඔයාගේ යාළුවා, Sasi AI Bot එක්ක කතා කරන්න. මට ඔයාගේ ප්‍රශ්නවලට උත්තර දෙන්න, කතන්දර කියන්න, අලුත් දේවල් කියා දෙන්න පුළුවන්.")

# 2. Consistency & Visual Hierarchy
# We'll use a consistent theme provided by Streamlit by default
# The title and description create a clear visual hierarchy.

# 3. Affordance & Feedback
# The text input clearly shows where to type, and the send button is obvious.
# The AI's response provides direct feedback.

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Set up the Generative Model
# Using 'gemini-2.0-flash' which is a common and often widely available model in the free tier.
model = genai.GenerativeModel('gemini-2.0-flash') 
chat = model.start_chat(history=[])

# Custom initial message from the AI for a friendly start
if not st.session_state.messages:
    initial_message = "හායි! මම Sasi AI Bot. ඔයාට කොහොමද උදව් කරන්න පුළුවන්?"
    with st.chat_message("assistant"):
        st.markdown(initial_message)
    st.session_state.messages.append({"role": "assistant", "content": initial_message})

# Accept user input
if prompt := st.chat_input("Sasi AI Bot එක්ක කතා කරන්න..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Send user prompt to the AI model
    with st.chat_message("assistant"):
        with st.spinner("Sasi AI Bot හිතනවා..."): # Provides feedback to the user
            try:
                response = chat.send_message(prompt)
                full_response = response.text
            except Exception as e:
                full_response = f"කණගාටුයි, Sasi AI Bot ට උත්තර දෙන්න බැරි වුණා. Error එක: {e}"
                st.error(full_response) # Display error in red
            
        st.markdown(full_response)
    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- Additional UI/UX elements ---
st.sidebar.title("ගැන")
st.sidebar.info(
    "Sasi AI Studio කියන්නේ Google Gemini AI API එක පාවිච්චි කරලා හදපු සරල AI Chatbot එකක්. "
    "මේක හදලා තියෙන්නේ කැම්පස් Project එකක් සඳහා. "
    "මට ඔයාගේ ප්‍රශ්නවලට උත්තර දෙන්න, කතන්දර කියන්න, අලුත් දේවල් කියා දෙන්න පුළුවන්."
)