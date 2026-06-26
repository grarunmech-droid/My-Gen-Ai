import streamlit as st
from google import genai
from google.genai import errors  # Imported to gracefully catch future API errors

# UI Setup
st.markdown(
  """
  <h1 style='text-align: center;'> Python AI Assistant</h1>
  <p style='text-align: center; font-size:18px;'>
    Ask any Python programming question.
  </p>
  """,
  unsafe_allow_html=True,
)

# Initialize Client using Streamlit Secrets for production safety
if "mychat" not in st.session_state:
    try:
        # st.secrets automatically reads from your Streamlit Cloud dashboard settings
        robo = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
        st.session_state.mychat = robo.chats.create(model="gemini-flash-lite-latest")
    except Exception as e:
        st.error("Failed to initialize the AI Client. Please check your Secret keys configuration.")

# User Input
question = st.text_input("", placeholder="Enter your Python question here...")
col1, col2, col3 = st.columns([4, 1, 4])
with col2:
  send = st.button("Send")

response_placeholder = st.empty()

# Execute call with robust error handling to reveal hidden error strings
if send and question:
  if "mychat" in st.session_state:
      with st.spinner("Thinking..."):
          try:
              response = st.session_state.mychat.send_message(question)
              response_placeholder.write(response.text)
          except errors.ClientError as ce:
              # This will bypass Streamlit's redaction and print the exact raw API error message
              st.error(f"Google API Client Error: {ce}")
          except Exception as e:
              st.error(f"An unexpected error occurred: {e}")
  else:
      st.error("Chat session is not initialized.")
