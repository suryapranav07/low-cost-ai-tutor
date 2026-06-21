import streamlit as st
from src.tutor import answer_question, count_tokens, get_related_concepts
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

st.set_page_config(page_title="AI Tutor", layout="wide")

st.title("Low-Cost AI Tutor")

st.sidebar.title("About")

st.sidebar.write("""
 ●  Multi-subject AI Tutor  
 ●  Uses FAISS retrieval  
 ●  Context pruning for cost reduction  
 ● ~80% token savings  

Built for low-resource environments 
""")

st.markdown("""
### ◉ Built for rural education

This AI tutor reduces API cost by **~80% using context pruning**, 
making it efficient for low-bandwidth environments.
""")


st.markdown("---")



question = st.text_input(
    " Ask your question"
)

if st.button("Get Answer"):

    if question.strip() == "":
        st.warning("Please enter a question")

    else:

        with st.spinner("Running retrieval and context pruning..."):

            answer, baseline_tokens, final_tokens, chunks = answer_question(question)

        saved = baseline_tokens - final_tokens

        percent = (
            saved / baseline_tokens * 100
            if baseline_tokens > 0
            else 0
        )

        st.markdown("---")



       

        st.markdown("## Tutor Response")

        with st.container(border=True):

            st.write(answer)

        related = get_related_concepts(
           question,
           answer
        )
        st.markdown("## Related Concepts")

        with st.container(border=True):

           st.write(related)

        # =========================
        # DASHBOARD
        # =========================

        st.markdown("## Optimization Report")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Retrieved Tokens",
            baseline_tokens
        )

        c2.metric(
            "Sent to LLM",
            final_tokens
        )

        c3.metric(
            "Reduction",
            f"{percent:.1f}%"
        )

        st.markdown("---")

        # =========================
        # PIPELINE
        # =========================

        st.markdown("## Pipeline")

        st.info(
            """
              Question
            → Retrieval
            → Context Pruning
            → LLaMA 3
            → Answer
            """
        )

        st.markdown("---")

        st.caption(
            f"FAISS • Context Pruning • Groq LLaMA 3 • {percent:.1f}% Token Reduction"
        )

