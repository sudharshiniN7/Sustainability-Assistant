import streamlit as st
if "theme" not in st.session_state:
    st.session_state.theme = "Light"
st.set_page_config(
    page_title="ECOBOT",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------- SIDEBAR SETTINGS ----------------
with st.sidebar:
    st.title("⚙️ ECOBOT Settings")

    st.session_state.theme = st.radio(
       "Choose Theme",
       ["Light", "Dark"],
       index=0 if st.session_state.theme == "Light" else 1
    )


    st.markdown("---")

    st.markdown("### ℹ️ About")
    st.write("ECOBOT is a sustainability learning assistant for students.")
    st.write("Upload documents and ask questions from them.")

    st.markdown("---")

    if st.button("🗑️ Clear uploaded document"):
        st.session_state.pop("document_text", None)
        st.success("Document cleared!")

st.markdown("""
<style>

/* REMOVE STREAMLIT WHITE HEADER SPACE */
header {visibility: hidden;}
.stApp {
    margin-top: -80px;
}

/* ECOBOT TITLE */
h1 {
    color: #000000 !important;
}

/* SUBTITLE TEXT */
div[data-testid="stMarkdown"] p {
    color: #000000 !important;
    font-weight: 500;
}

/* INPUT BOX TEXT */
input {
    color: #000000 !important;
}

</style>
""", unsafe_allow_html=True)
# =======================
# ⚙️ SIDEBAR SETTINGS
# =======================
st.sidebar.title("⚙️ Settings")

# Theme toggle
theme = st.sidebar.radio(
    "Theme",
    ["Light 🌞", "Dark 🌙"],
    index=0
)

# Confidence toggle
show_confidence = st.sidebar.checkbox(
    "Show confidence score",
    value=True
)

# App info
st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ About ECOBOT")
st.sidebar.markdown("""
ECOBOT is a sustainability learning assistant for students.

**Features:**
- Predefined sustainability knowledge  
- Document upload & Q&A  
- Confidence scoring  

Built for academic submission 🎓
""")

# Reset button
if st.sidebar.button("🔄 Clear uploaded document"):
    if "document_text" in st.session_state:
        del st.session_state["document_text"]
    st.sidebar.success("Document cleared!")
# =======================
# 🎨 THEME STYLING
# =======================
if theme == "Dark 🌙":
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #0f2a30, #0a1f24);
        color: white;
    }
    input, textarea {
        background-color: #1e3a40 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

else:  # Light theme
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #e8f4ff, #f5fbff);
        color: black;
    }
    input, textarea {
        background-color: #ffffff !important;
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
st.set_page_config(
    page_title="ECOBOT",
    page_icon="🌱",
    layout="wide"
)
st.title("🌱 ECOBOT")
st.markdown(
    "<div class='subtitle'>Your sustainability learning companion 📘🌍</div>",
    unsafe_allow_html=True
)

# Predefined sustainability knowledge (Layer 1)
knowledge_base = {
    "climate change": "Climate change refers to long-term changes in temperature and weather patterns, mainly caused by human activities like burning fossil fuels.",
    "global warming": "Global warming is the increase in Earth's average surface temperature due to greenhouse gases such as CO₂.",
    "sustainability": "Sustainability means meeting present needs without harming the ability of future generations to meet their needs.",
    "renewable energy": "Renewable energy comes from natural sources like sunlight, wind, and water that do not run out.",
    "recycling": "Recycling is the process of converting waste materials into new products to reduce pollution and save resources."
}
st.markdown("<div class='card'>", unsafe_allow_html=True)

st.subheader("📄 Upload your document")
uploaded_file = st.file_uploader(
    "Upload a text file (.txt)",
    type=["txt"]
)

st.markdown("</div>", unsafe_allow_html=True)


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

st.markdown("<div class='card'>", unsafe_allow_html=True)

question = st.text_input("💬 Ask your question:")

st.markdown("</div>", unsafe_allow_html=True)


if question:
    user_question = question.lower()
    found = False

    # 🔹 Layer 1: Predefined knowledge
    for key in knowledge_base:
        if key in user_question:
            st.success("✅ Answer found (Predefined)")
            st.write(knowledge_base[key])
            if show_confidence:
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
