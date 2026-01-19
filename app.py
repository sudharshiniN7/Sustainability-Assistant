import streamlit as st
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
st.set_page_config(
    page_title="ECOBOT",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 ECOBOT")
st.write("Upload documents and ask sustainability questions.")

# Predefined sustainability knowledge (Layer 1)
knowledge_base = {
    "climate change": "Climate change refers to long-term changes in temperature and weather patterns, mainly caused by human activities like burning fossil fuels.",
    "global warming": "Global warming is the increase in Earth's average surface temperature due to greenhouse gases such as CO₂.",
    "sustainability": "Sustainability means meeting present needs without harming the ability of future generations to meet their needs.",
    "renewable energy": "Renewable energy comes from natural sources like sunlight, wind, and water that do not run out.",
    "recycling": "Recycling is the process of converting waste materials into new products to reduce pollution and save resources."
}
st.subheader("📄 Upload your document")

uploaded_file = st.file_uploader(
    "Upload a text file (.txt)",
    type=["txt"]
)

document_text = ""

if uploaded_file is not None:
    document_text = uploaded_file.read().decode("utf-8",errors="ignore")
    st.success("Document uploaded successfully!")

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

    # 🔹 Layer 1: Predefined knowledge
    for key in knowledge_base:
        if key in user_question:
            st.success("✅ Answer found (Predefined)")
            st.write(knowledge_base[key])
            st.caption("📊 Confidence: 90%")
            found = True
            break

    # 🔹 Layer 2: Uploaded document search
    if not found and document_text:
        for line in document_text.split("\n"):
            if any(word in line.lower() for word in user_question.split()):
                st.info("📄 Answer from uploaded document")
                st.write(line)
                st.caption("📊 Confidence: 70%")
                found = True
                break

    # 🔹 No answer
    if not found:
        st.warning("❓ I don’t have an answer yet.")
        st.caption("📊 Confidence: 0%")
