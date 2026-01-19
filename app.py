import streamlit as st

st.set_page_config(
    page_title="Sustainability Learning Assistant",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Sustainability Learning Assistant")
st.write("Ask questions about sustainability and get simple answers.")
# Predefined sustainability knowledge (Layer 1)
knowledge_base = {
    "climate change": "Climate change refers to long-term changes in temperature and weather patterns, mainly caused by human activities like burning fossil fuels.",
    "global warming": "Global warming is the increase in Earth's average surface temperature due to greenhouse gases such as CO₂.",
    "sustainability": "Sustainability means meeting present needs without harming the ability of future generations to meet their needs.",
    "renewable energy": "Renewable energy comes from natural sources like sunlight, wind, and water that do not run out.",
    "recycling": "Recycling is the process of converting waste materials into new products to reduce pollution and save resources."
}

question = st.text_input("Ask your question:")

if question:
    user_question = question.lower()

    found = False
    for key in knowledge_base:
        if key in user_question:
            st.success("✅ Answer found")
            st.write(knowledge_base[key])
            found = True
            break

    if not found:
        st.warning("🤔 I don’t have an exact answer yet, but I’m learning!")

