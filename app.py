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
# -------- Layer 2: Document-based fallback --------
def search_documents(question, filepath="sustainability_docs.txt"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            paragraphs = f.read().split("\n\n")

        question_words = question.lower().split()

        best_match = ""
        best_score = 0

        for para in paragraphs:
            score = sum(word in para.lower() for word in question_words)
            if score > best_score:
                best_score = score
                best_match = para

        return best_match if best_score > 0 else None

    except FileNotFoundError:
        return None

question = st.text_input("Ask your question:")

if question:
    user_question = question.lower()
    found = False

    for key in knowledge_base:
        if key in user_question:
            st.success("✅ Answer found (Predefined Knowledge)")
            st.write(knowledge_base[key])
            st.caption("📊 Confidence: 90%")

            found = True
            break

    if not found:
        doc_answer = search_documents(user_question)

        if doc_answer:
            st.info("📄 Answer from documents")
            st.write(doc_answer)
            st.caption("📊 Confidence: 60%")

        else:
            st.warning("❓ I don't have an answer yet")
            st.caption("📊 Confidence: 0%")
