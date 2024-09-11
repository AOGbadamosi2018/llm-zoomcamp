import streamlit as st
import time
import uuid

from rag import rag
from db import save_conversation, save_feedback

def main():
    st.title("Course Assistant")

    # Session state initialization
    if 'conversation_id' not in st.session_state:
        st.session_state.conversation_id = str(uuid.uuid4())
    if 'count' not in st.session_state:
        st.session_state.count = 0

    # Course selection
    course = st.selectbox(
        "Select a course:",
        ["machine-learning-zoomcamp", "data-engineering-zoomcamp", "mlops-zoomcamp"]
    )

    # User input
    user_input = st.text_input("Enter your question:")

    if st.button("Ask"):
        with st.spinner('Processing...'):
            output = rag(user_input, course)
            st.success("Completed!")
            st.write(output)
            
            # Save conversation to database
            save_conversation(st.session_state.conversation_id, user_input, output, course)

    # Feedback buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("+1"):
            st.session_state.count += 1
            save_feedback(st.session_state.conversation_id, 1)
    with col2:
        if st.button("-1"):
            st.session_state.count -= 1
            save_feedback(st.session_state.conversation_id, -1)

    st.write(f"Current count: {st.session_state.count}")

if __name__ == "__main__":
    main()