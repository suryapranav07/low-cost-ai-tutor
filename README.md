# 📚 Low-Cost AI Tutor (Context Pruning + RAG)

An intelligent, curriculum-aligned AI tutor designed for **low-resource environments**.  
This system reduces LLM usage cost by **~80% using context pruning**, making it suitable for rural education where bandwidth and compute are limited.

---

## 🚀 Problem Statement

Traditional AI tutors rely on large models and send **full textbook context**, leading to:

- ❌ High API cost  
- ❌ High latency  
- ❌ Large data transfer  

---

## 💡 Our Solution

We built a **context-aware tutoring system** that:

- Ingests full textbooks (PDFs)
- Retrieves only relevant content
- Applies **multi-stage context pruning**
- Sends minimal tokens to the LLM

---

## 🧠 Key Innovation: Context Pruning

Instead of sending raw textbook content, we:

1. 🔍 Retrieve relevant chunks (FAISS)
2. 🎯 Filter by subject
3. ✂️ Extract key concepts (semantic pruning)
4. 📉 Limit context size
5. ⚡ Send only essential information to LLM

---

## 📊 Results

| System | Tokens Used |
|--------|------------|
| Baseline RAG | ~500–800 tokens |
| Our System | ~50–100 tokens |

👉 **Token Reduction: ~80–90%**

---

## 🏗️ Architecture


PDF Textbooks
↓
Chunking
↓
Embeddings (Sentence Transformers)
↓
FAISS Retrieval
↓
Subject Filtering
↓
Semantic Pruning (Summarization)
↓
Context Reduction
↓
LLM (Groq)
↓
Final Answer


---

## 📦 Tech Stack

- 🧠 LLM: Groq (LLaMA 3)
- 🔍 Retrieval: FAISS
- 📄 PDF Processing: PyMuPDF
- 🔤 Embeddings: Sentence Transformers
- 🌐 UI: Streamlit
- ⚡ Optimization: Context Pruning + Compression

---

## 🖥️ Features

- 📚 Multi-subject support (Science, Math, Social Science)
- ⚡ Fast and low-cost responses
- 📉 Token usage tracking
- 🎯 Curriculum-aligned answers
- 🌐 Simple web interface

---

## 🧪 Example

### Input:

Solve x² - 5x + 6 = 0


### Output:
- Step-by-step solution
- Correct roots
- Explanation

### Token Optimization:

Before: 582
After: 73
Saved: 87%


---

## ⚙️ Setup Instructions

### 1️⃣ Clone repo

```bash
git clone <your_repo_url>
cd ai_tutor
2️⃣ Install dependencies
pip install -r requirements.txt
3️⃣ Add API keys

Create .env file:

GROQ_API_KEY=your_key
SCALEDOWN_API_KEY=your_key
4️⃣ Run the app
streamlit run app.py
📁 Project Structure
ai_tutor/
├── app.py
├── src/
│   ├── ingest.py
│   ├── create_index.py
│   ├── search.py
│   ├── tutor.py
├── requirements.txt
├── .gitignore
🎯 Why This Matters

This system makes AI tutoring:

💰 Affordable
📡 Low-bandwidth friendly
🌍 Accessible in rural areas
🏆 Hackathon Highlights
✔ Context pruning reduces cost by ~80%
✔ Works on full textbooks
✔ Multi-subject support
✔ Real-time answering
✔ Efficient and scalable
🔮 Future Improvements
📊 Visual token comparison graphs
👤 Student-level personalization
🌐 Offline support
📱 Mobile-friendly UI
👨‍💻 Team
Surya Pranav
Sai Sri Harshas
⭐ Acknowledgements
Groq API
Sentence Transformers
FAISS
Streamlit
