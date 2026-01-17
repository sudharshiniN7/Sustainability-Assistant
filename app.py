"""
Sustainability Learning Chatbot
Made by: Sudharshini N
Purpose: Help students learn sustainability concepts easily
"""

import streamlit as st
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

# My file paths
DOCS_FILE = "sustainability_docs.txt"
SAVED_DATA = "saved_data.pkl"

class SustainabilityChatbot:
    def __init__(self):
        self.text_chunks = []
        self.vec = None
        self.vectors = None
        
    def read_document(self, filepath):
        # reads the knowledge file
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                doc_text = file.read()
            return doc_text
        except:
            return None
    
    def split_into_chunks(self, text, size=500, overlap=100):
        # break text into smaller pieces that overlap a bit
        words_list = text.split()
        chunks_list = []
        
        i = 0
        while i < len(words_list):
            chunk_text = ' '.join(words_list[i:i + size])
            if len(chunk_text.split()) > 50:  # ignore tiny chunks
                chunks_list.append(chunk_text)
            i += size - overlap
        
        return chunks_list
    
    def process_doc(self, text):
        # splits document and creates vectors
        self.text_chunks = self.split_into_chunks(text)
        
        # setup vectorizer
        self.vec = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        # convert text to numbers
        self.vectors = self.vec.fit_transform(self.text_chunks)
        
    def search_answer(self, user_question):
        # finds best matching chunk for the question
        if self.vec is None or self.vectors is None:
            return None
        
        # turn question into vector
        q_vector = self.vec.transform([user_question])
        
        # compare with all chunks
        scores = cosine_similarity(q_vector, self.vectors)
        
        # find best match
        best_idx = np.argmax(scores)
        best_score = scores[0][best_idx]
        
        if best_score > 0.1:  # only return if good enough match
            return self.text_chunks[best_idx], best_score
        return None, 0
    
    def make_simple(self, answer_text):
        # makes the answer easier to understand
        answer_text = re.sub(r'\s+', ' ', answer_text).strip()
        
        # break into sentences
        sent_list = re.split(r'[.!?]+', answer_text)
        sent_list = [s.strip() for s in sent_list if len(s.strip()) > 10]
        
        # replace difficult words with simple ones
        easy_words = {
            'sustainability': 'keeping environment healthy long-term',
            'mitigation': 'reducing',
            'anthropogenic': 'caused by humans',
            'biodiversity': 'different types of plants and animals',
            'renewable energy': 'energy from sun, wind, water',
            'greenhouse gases': 'gases that trap heat',
            'carbon footprint': 'amount of CO2 you produce',
            'ecosystem': 'environment where plants and animals live',
            'photovoltaic': 'solar panels',
            'fossil fuels': 'coal, oil, natural gas',
            'deforestation': 'cutting down forests',
            'climate change': 'Earth getting warmer',
            'sustainable development': 'growing without harming environment'
        }
        
        # replace words
        simple_text = answer_text.lower()
        for hard_word, easy_word in easy_words.items():
            simple_text = simple_text.replace(hard_word.lower(), easy_word)
        
        # rebuild sentences
        simple_sentences = re.split(r'[.!?]+', simple_text)
        simple_sentences = [s.strip().capitalize() for s in simple_sentences if len(s.strip()) > 10]
        
        # keep only important sentences
        final_answer = '. '.join(simple_sentences[:4]) + '.'
        
        final_answer = re.sub(r'\s+', ' ', final_answer)
        final_answer = final_answer.replace('..', '.')
        
        return final_answer
    
    def save_data(self, filepath):
        # saves processed data so we don't process again
        my_data = {
            'chunks': self.text_chunks,
            'vectorizer': self.vec,
            'vectors': self.vectors
        }
        with open(filepath, 'wb') as f:
            pickle.dump(my_data, f)
    
    def load_data(self, filepath):
        # loads already processed data
        try:
            with open(filepath, 'rb') as f:
                my_data = pickle.load(f)
            self.text_chunks = my_data['chunks']
            self.vec = my_data['vectorizer']
            self.vectors = my_data['vectors']
            return True
        except:
            return False

def setup_sample_docs():
    # creates example sustainability content
    example_docs = """
    Climate Change and Global Warming
    Climate change refers to long-term shifts in global temperatures and weather patterns. While climate change is natural, human activities have been the main driver since the 1800s, primarily due to the burning of fossil fuels like coal, oil and gas. Greenhouse gases produced by burning fossil fuels act like a blanket around Earth, trapping heat and raising temperatures. Carbon dioxide and methane are the main greenhouse gases responsible for global warming.
    
    Renewable Energy Sources
    Renewable energy comes from natural sources that are constantly replenished. Solar energy is captured using photovoltaic panels that convert sunlight into electricity. Wind energy uses turbines to generate power from moving air. Hydroelectric power harnesses the energy of flowing water. These clean energy sources produce little to no greenhouse gases and help reduce our carbon footprint.
    
    Sustainable Development Goals
    The United Nations created 17 Sustainable Development Goals (SDGs) to achieve a better future for all. SDG 4 focuses on Quality Education, ensuring inclusive and equitable quality education for all. SDG 7 aims for Affordable and Clean Energy, ensuring access to affordable, reliable, sustainable and modern energy. SDG 13 addresses Climate Action, taking urgent action to combat climate change and its impacts.
    
    Biodiversity and Ecosystems
    Biodiversity refers to the variety of life forms on Earth, including different species of plants, animals, and microorganisms. Healthy ecosystems provide essential services like clean air, water purification, pollination of crops, and climate regulation. Deforestation and habitat destruction are major threats to biodiversity, causing species extinction and ecosystem collapse.
    
    Carbon Footprint and Mitigation
    A carbon footprint is the total amount of greenhouse gases produced by human activities. Reducing our carbon footprint involves using renewable energy, improving energy efficiency, reducing waste, and changing consumption patterns. Mitigation strategies include planting trees, developing clean technologies, and transitioning away from fossil fuels.
    
    Circular Economy
    A circular economy aims to eliminate waste by keeping products and materials in use for as long as possible. This contrasts with the traditional linear economy of take-make-dispose. Circular economy principles include designing for durability, repairing and refurbishing products, recycling materials, and reducing single-use items.
    
    Water Conservation
    Freshwater is a limited resource essential for life. Water conservation involves using water efficiently and reducing unnecessary consumption. Strategies include fixing leaks, using water-efficient appliances, collecting rainwater, and protecting watersheds from pollution. Climate change is affecting water availability in many regions.
    
    Sustainable Agriculture
    Sustainable agriculture produces food while protecting the environment and supporting local communities. Practices include crop rotation, organic farming, reducing pesticide use, conserving water, and maintaining soil health. Sustainable agriculture helps ensure food security while minimizing environmental impact.
    """
    
    with open(DOCS_FILE, 'w', encoding='utf-8') as f:
        f.write(example_docs)

# main app starts here
def main():
    st.set_page_config(
        page_title="Sustainability Chatbot",
        page_icon="🌍",
        layout="wide"
    )
    
    st.title("🌍 Sustainability Learning Assistant")
    st.markdown("*Ask questions about sustainability and get simple answers*")
    
    # setup session variables
    if 'bot' not in st.session_state:
        st.session_state.bot = SustainabilityChatbot()
        st.session_state.is_ready = False
    
    # sidebar stuff
    with st.sidebar:
        st.header("📚 Document Manager")
        
        # check if docs exist
        if not os.path.exists(DOCS_FILE):
            st.warning("No documents found!")
            if st.button("Create Sample Documents"):
                setup_sample_docs()
                st.success("Sample documents created!")
                st.rerun()
        
        # let user upload their own file
        user_file = st.file_uploader(
            "Upload sustainability document (TXT only)",
            type=['txt']
        )
        
        if user_file is not None:
            file_content = user_file.read().decode('utf-8')
            with open(DOCS_FILE, 'w', encoding='utf-8') as f:
                f.write(file_content)
            st.success("File uploaded!")
        
        # button to process documents
        if st.button("🔄 Process Documents"):
            with st.spinner("Processing..."):
                doc_content = st.session_state.bot.read_document(DOCS_FILE)
                if doc_content:
                    st.session_state.bot.process_doc(doc_content)
                    st.session_state.bot.save_data(SAVED_DATA)
                    st.session_state.is_ready = True
                    total_chunks = len(st.session_state.bot.text_chunks)
                    st.success(f"Done! Created {total_chunks} text chunks")
                else:
                    st.error("Couldn't read file")
        
        # try to load saved data
        if not st.session_state.is_ready and os.path.exists(SAVED_DATA):
            if st.session_state.bot.load_data(SAVED_DATA):
                st.session_state.is_ready = True
                chunk_count = len(st.session_state.bot.text_chunks)
                st.info(f"Loaded {chunk_count} chunks from saved data")
        
        # show some stats
        if st.session_state.is_ready:
            st.markdown("---")
            st.metric("Text Chunks", len(st.session_state.bot.text_chunks))
            st.metric("Words in Dictionary", st.session_state.bot.vectors.shape[1])
    
    # main section
    left_col, right_col = st.columns([2, 1])
    
    with left_col:
        st.header("💬 Ask Your Question")
        
        user_q = st.text_input(
            "Type your sustainability question here:",
            placeholder="Example: What is climate change? Why is renewable energy important?"
        )
        
        # show some example questions
        with st.expander("📌 Try These Questions"):
            examples = [
                "What is climate change?",
                "How does solar energy work?",
                "What are the SDGs?",
                "Why is biodiversity important?",
                "How can I reduce my carbon footprint?",
                "What is circular economy?",
                "Why should we save water?"
            ]
            for ex in examples:
                if st.button(ex, key=ex):
                    user_q = ex
        
        # answer the question
        if user_q and st.session_state.is_ready:
            with st.spinner("Searching for answer..."):
                answer_chunk, match_score = st.session_state.bot.search_answer(user_q)
                
                if answer_chunk:
                    st.success("✅ Found an answer!")
                    
                    st.subheader("📖 Easy Explanation")
                    simple_answer = st.session_state.bot.make_simple(answer_chunk)
                    st.info(simple_answer)
                    
                    st.progress(float(match_score), text=f"Match Quality: {match_score:.1%}")
                    
                    # let user see original text if they want
                    with st.expander("🔍 See Original Text"):
                        st.text_area("Original Content", answer_chunk, height=200)
                else:
                    st.warning("⚠️ Couldn't find relevant information. Try asking differently.")
        
        elif user_q and not st.session_state.is_ready:
            st.error("Please process documents first using the button in sidebar")
    
    with right_col:
        st.header("ℹ️ How It Works")
        st.markdown("""
        This chatbot helps you learn about sustainability by:
        
        - 📄 Reading sustainability documents
        - 🔍 Finding relevant information  
        - 💡 Explaining in simple language
        - 🎓 Making learning easier
        
        **Steps to use:**
        1. Upload your documents OR use samples
        2. Click "Process Documents"
        3. Type your question
        4. Get simple explanation
        
        **Cool Features:**
        - Works offline
        - Free to use
        - No complex setup needed
        - Privacy friendly
        - Made for students
        """)
        
        st.markdown("---")
        st.markdown("**Supports UN Goals:**")
        st.markdown("🎓 Quality Education")
        st.markdown("⚡ Clean Energy")  
        st.markdown("🌍 Climate Action")
    
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "Sustainability Learning Assistant | Made for AI for Sustainability Project"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()