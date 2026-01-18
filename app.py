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
    
    def split_into_chunks(self, text, size=300, overlap=50):
        # break text into smaller pieces that overlap a bit
        # smaller chunks = more precise answers
        words_list = text.split()
        chunks_list = []
        
        i = 0
        while i < len(words_list):
            chunk_text = ' '.join(words_list[i:i + size])
            if len(chunk_text.split()) > 30:  # ignore tiny chunks
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
            return None, 0
        
        # turn question into vector
        q_vector = self.vec.transform([user_question])
        
        # compare with all chunks
        scores = cosine_similarity(q_vector, self.vectors)
        
        # find best match
        best_idx = np.argmax(scores)
        best_score = scores[0][best_idx]
        
        # lowered threshold for better matching
        if best_score > 0.05:  # more lenient threshold
            return self.text_chunks[best_idx], best_score
        return None, 0
    
    def make_simple(self, answer_text):
        # makes the answer easier to understand
        answer_text = re.sub(r'\s+', ' ', answer_text).strip()
        
        # break into sentences
        sent_list = re.split(r'[.!?]+', answer_text)
        sent_list = [s.strip() for s in sent_list if len(s.strip()) > 15]
        
        # More aggressive simplification
        easy_words = {
            'sustainability': 'environmental health',
            'mitigation': 'reduction',
            'anthropogenic': 'human-caused',
            'biodiversity': 'variety of life',
            'renewable energy': 'clean energy',
            'greenhouse gases': 'heat-trapping gases',
            'carbon footprint': 'CO2 impact',
            'ecosystem': 'natural environment',
            'photovoltaic': 'solar panels',
            'fossil fuels': 'coal and oil',
            'deforestation': 'forest loss',
            'sustainable development': 'balanced growth',
            'primarily': 'mainly',
            'subsequently': 'then',
            'consequently': 'so',
            'encompasses': 'includes',
            'utilize': 'use',
            'implement': 'put in place',
            'activities that are responsible for': 'things that cause',
            'are embedded in': 'are part of',
            'everyday social practices': 'daily activities',
            'contribute to': 'add to',
            'is also of interest to sociologists because': 'sociologists study this because',
            'result in emissions of': 'create',
            'heating and cooling our homes': 'using home temperature control'
        }
        
        # replace words
        simple_text = answer_text
        for hard_phrase, easy_phrase in easy_words.items():
            simple_text = re.sub(r'\b' + re.escape(hard_phrase) + r'\b', easy_phrase, simple_text, flags=re.IGNORECASE)
        
        # Remove overly complex sentences - keep ONLY simple, direct ones
        simple_sentences = re.split(r'[.!?]+', simple_text)
        simple_sentences = [s.strip() for s in simple_sentences if len(s.strip()) > 15]
        
        # Filter to keep only the most understandable sentences
        clear_sentences = []
        for sentence in simple_sentences:
            # Skip sentences that are still too complex
            if len(sentence.split()) < 25 and 'sociologist' not in sentence.lower():
                clear_sentences.append(sentence)
        
        # Take only first 2 clear sentences
        if len(clear_sentences) >= 2:
            final_answer = clear_sentences[0] + '. ' + clear_sentences[1] + '.'
        elif len(clear_sentences) == 1:
            final_answer = clear_sentences[0] + '.'
        else:
            # Fallback: just take first sentence from original
            final_answer = sent_list[0] + '.' if sent_list else "I found information but it's too complex. Try asking differently."
        
        # clean up
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
    # creates example sustainability content (student-friendly version)
    example_docs = """
    What is Climate Change?
    Climate change means long-term changes in Earth's temperature and weather. The planet is getting warmer because humans burn coal, oil, and gas. These fuels release gases that trap heat. This causes problems like melting ice, rising seas, and extreme weather.
    
    What is Global Warming?
    Global warming is the increase in Earth's temperature. It is caused mainly by greenhouse gases from human activities. Carbon dioxide from burning fossil fuels is the biggest cause. Global warming leads to climate change.
    
    Renewable Energy
    Renewable energy comes from natural sources that never run out. Solar panels turn sunlight into electricity. Wind turbines use moving air to make power. Water flowing in rivers creates hydroelectric energy. These clean sources don't pollute like coal and oil do.
    
    Solar Energy
    Solar energy uses the sun's light to make electricity. Solar panels on roofs capture sunlight. This energy is clean and free. Many homes and businesses now use solar power to reduce electricity bills and help the environment.
    
    Wind Energy
    Wind energy uses large turbines with blades that spin in the wind. As they spin, they generate electricity. Wind farms can power thousands of homes. Wind energy is clean and renewable.
    
    Sustainable Development Goals (SDGs)
    The United Nations created 17 goals for a better world by 2030. SDG 4 is Quality Education for everyone. SDG 7 is Clean Energy that everyone can afford. SDG 13 is Climate Action to fight global warming. These goals help make the world better.
    
    What is Biodiversity?
    Biodiversity means all the different plants, animals, and living things on Earth. Healthy biodiversity keeps nature balanced. When forests are cut down or oceans are polluted, many species die. We need biodiversity for clean air, water, and food.
    
    Ecosystems
    An ecosystem is a place where plants, animals, and nature work together. Forests, oceans, and deserts are ecosystems. Healthy ecosystems clean our air and water. They give us food and protect us from disasters.
    
    What is Carbon Footprint?
    Your carbon footprint is how much CO2 you create. Driving cars, using electricity, and buying products all add to it. You can reduce your carbon footprint by walking, biking, using less energy, and recycling.
    
    How to Reduce Carbon Footprint
    Use less electricity at home. Walk or bike instead of driving. Eat less meat. Recycle and reuse things. Plant trees. Buy local products. These small actions help fight climate change.
    
    Greenhouse Gases
    Greenhouse gases trap heat in Earth's atmosphere like a blanket. Carbon dioxide, methane, and nitrous oxide are the main ones. They come from burning fuels, farming, and waste. Too much greenhouse gas causes global warming.
    
    What is Deforestation?
    Deforestation means cutting down forests. Trees are removed for farming, wood, or building. This is bad because trees absorb CO2 and give us oxygen. Less trees means more CO2 and climate change.
    
    Fossil Fuels
    Fossil fuels are coal, oil, and natural gas. They formed from dead plants and animals millions of years ago. Burning them gives energy but releases CO2. This causes pollution and global warming.
    
    Circular Economy
    A circular economy means reusing and recycling everything. Instead of making, using, and throwing away, we repair and reuse. This reduces waste and saves resources. It's better for the planet.
    
    Water Conservation
    Water conservation means using water wisely. Fix leaky taps. Take shorter showers. Don't waste water. Many places face water shortages. Saving water helps everyone and protects nature.
    
    Why is Water Important?
    Water is essential for life. We need it to drink, grow food, and stay clean. Only 3% of Earth's water is fresh. Climate change is making water scarce in many places. We must protect and save water.
    
    Sustainable Agriculture
    Sustainable farming grows food without harming the environment. Farmers use less pesticides, save water, and protect soil. They rotate crops and use natural methods. This keeps land healthy for future generations.
    
    Why Plant Trees?
    Trees absorb CO2 and give oxygen. They provide shade, prevent floods, and give homes to animals. Planting trees fights climate change. One tree can remove tons of CO2 over its lifetime.
    
    What is Recycling?
    Recycling turns old items into new ones. Plastic bottles become new containers. Paper becomes new paper. Recycling saves energy, reduces waste, and protects nature.
    
    What are SDGs?
    SDGs are 17 Sustainable Development Goals by the UN. They aim to end poverty, protect the planet, and ensure peace by 2030. Goal 13 is about climate action. Goal 7 is clean energy. Goal 4 is quality education.
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
            file_content = user_file.read().decode('utf-8' errors='ignore')
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