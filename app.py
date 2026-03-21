import streamlit as st
from src.tutor import answer_question, count_tokens
from src.search import search

st.markdown("""
<style>

body {
    background-color: #0f172a;
    color: white;
}

h1, h2, h3 {
    color: #38bdf8;
}

.stTextInput>div>div>input {
    background-color: #1e293b;
    color: white;
    border-radius: 10px;
}

.stButton>button {
    background-color: #38bdf8;
    color: black;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #0ea5e9;
    color: white;
}

.card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    margin-top: 15px;
}

.metric {
    font-size: 18px;
    font-weight: bold;
    color: #22c55e;
}

</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="AI Tutor", layout="centered")

st.title("📚 Low-Cost AI Tutor")

st.sidebar.title("About")

st.sidebar.write("""
📚 Multi-subject AI Tutor  
⚡ Uses FAISS retrieval  
✂️ Context pruning for cost reduction  
📉 ~80% token savings  

Built for low-resource environments 
""")

st.markdown("""
###  Built for rural education

This AI tutor reduces API cost by **~80% using context pruning**, 
making it efficient for low-bandwidth environments.
""")


st.markdown("---")

question = st.text_input("💬 Ask your question")

if st.button("✨ Get Answer"):

    if question.strip() == "":
        st.warning("Please enter a question")
    else:

        with st.spinner("Thinking..."):
            answer, baseline_tokens, final_tokens = answer_question(question)

        saved = baseline_tokens - final_tokens
        percent = (saved / baseline_tokens) * 100 if baseline_tokens > 0 else 0

        # 📖 Answer
        st.markdown("### 📖 Answer")
        st.write(answer)

        # 📊 Token Metrics (ONLY ONE PLACE)
        st.markdown("### 📊 Token Optimization")

        col1, col2, col3 = st.columns(3)

        col1.metric("Before", baseline_tokens)
        col2.metric("After", final_tokens)
        col3.metric("Saved %", f"{percent:.2f}%")