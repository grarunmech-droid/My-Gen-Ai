import streamlit as st
from google import genai
from google.genai import errors

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

# Initialize BOTH Client and Chat in Streamlit memory
if "mychat" not in st.session_state or "robo" not in st.session_state:
    try:
        # Save the client connection to session state
        st.session_state.robo = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
        # Save the chat instance to session state
        st.session_state.mychat = st.session_state.robo.chats.create(model="gemini-flash-lite-latest")
    except Exception as e:
        st.error("Failed to initialize the AI Client. Check your Secret keys configuration.")

# User Input
question = st.text_input("", placeholder="Enter your Python question here...")
col1, col2, col3 = st.columns([4, 1, 4])
with col2:
  send = st.button("Send")

response_placeholder = st.empty()

# Execute call
if send and question:
  if "mychat" in st.session_state:
      with st.spinner("Thinking..."):
          try:
              # Calls the persistent chat session with the living client connection
              response = st.session_state.mychat.send_message(question)
              response_placeholder.write(response.text)
          except errors.ClientError as ce:
              st.error(f"Google API Client Error: {ce}")
          except Exception as e:
              st.error(f"An unexpected error occurred: {e}")
  else:
      st.error("Chat session is not initialized.")
