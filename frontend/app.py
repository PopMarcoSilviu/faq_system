import streamlit as st
import requests

# Backend URL (service name if in Docker Compose)
BACKEND_URL = "http://backend:8000/ask-question"

# Configure page layout
st.set_page_config(
    page_title="Semantic FAQ Chat",
    layout="wide"
)

st.title("Semantic FAQ Chat")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_metadata" not in st.session_state:
    st.session_state.current_metadata = None

# Sidebar for metadata
with st.sidebar:
    st.header("Latest Query Info")
    
    if st.session_state.current_metadata:
        st.subheader(" Source")
        st.write(st.session_state.current_metadata.get("source", "N/A"))
        
        st.subheader(" Matched Question")
        st.write(st.session_state.current_metadata.get("matched_question", "N/A"))
    else:
        st.info("Ask a question to see matching information!")
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.current_metadata = None
        st.rerun()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What's your question?"):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(BACKEND_URL, json={"user_question": prompt})
                
                if response.ok:
                    data = response.json()
                    answer = data.get("answer", "No answer")
                    source = data.get("source", "Unknown")
                    matched_question = data.get("matched_question", "N/A")
                    
                    # Display answer
                    st.markdown(answer)
                    
                    # Update metadata
                    st.session_state.current_metadata = {
                        "source": source,
                        "matched_question": matched_question
                    }
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    st.rerun()
                    
                else:
                    error_msg = f"Backend error: {response.status_code}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    
            except requests.exceptions.RequestException as e:
                error_msg = f"Connection error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})