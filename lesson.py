import streamlit as st

# Set page title and style to match app.py
st.set_page_config(page_title="Text Input Page", layout="wide")
st.title("Knowledge Graph Curriculum Customizer")
st.write("Enter your text below. This page uses the same style as the main app, but is fully independent.")

# Text input area
user_text = st.text_area("Paste your text here:", height=200)

# Show the input value (for demonstration)
if user_text:
    st.success("Text stored in variable!")
    st.write(user_text)
else:
    st.info("Please enter some text above.")

# The variable 'user_text' contains the input text for further processing 