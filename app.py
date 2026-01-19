import streamlit as st

st.set_page_config(
    page_title="Sustainability Learning Assistant",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Sustainability Learning Assistant")
st.write("Ask questions about sustainability and get simple answers.")

question = st.text_input("Ask your question:")

if question:
    st.success("✅ App is working correctly!")
    st.write("You asked:", question)
