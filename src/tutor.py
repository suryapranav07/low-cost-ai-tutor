from src.search import search
from groq import Groq
import requests
import tiktoken
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SCALEDOWN_API_KEY = os.getenv("SCALEDOWN_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

enc = tiktoken.get_encoding("cl100k_base")


# -----------------------------
# TOKEN COUNT
# -----------------------------
def count_tokens(text):
    return len(enc.encode(text))


# -----------------------------
# SUBJECT DETECTION
# -----------------------------
def detect_subject(question):
    q = question.lower()

    if any(w in q for w in ["solve", "equation", "triangle", "probability"]):
        return "math"

    if any(w in q for w in ["photosynthesis", "cell", "acid", "current"]):
        return "science"

    if any(w in q for w in ["democracy", "government", "economy"]):
        return "social science"

    return "general"


# -----------------------------
# SUMMARIZATION (KEY STEP)
# -----------------------------
def summarize_context(text):

    prompt = f"""
Extract the most important points needed to answer a question.

Rules:
- Use bullet points
- 3–5 points only
- Keep it concise
- Do not say "no text provided"

Text:
{text}

Key Points:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# -----------------------------
# SCALEDOWN COMPRESSION
# -----------------------------
def compress_context(text):

    url = "https://api.scaledown.xyz/compress/raw/"

    headers = {
        "Authorization": f"Bearer {SCALEDOWN_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {"text": text}

    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()

        return data.get("compressed_text", text)

    except:
        return text


# -----------------------------
# MAIN FUNCTION
# -----------------------------
def answer_question(question):

    # 1️⃣ detect subject
    subject = detect_subject(question)

    # 2️⃣ retrieve chunks (for baseline)
    chunks = search(question, subject=subject, k=5)

    # -------------------------
    # 🔴 BASELINE CONTEXT
    # -------------------------
    baseline_context = "\n\n".join(chunks)

    if not baseline_context.strip():
        return "No relevant content found in textbooks."

    baseline_tokens = count_tokens(baseline_context)

    # -------------------------
    # 🟢 OPTIMIZED PIPELINE
    # -------------------------

    # Step 1: reduce context size
    base_context = baseline_context[:800]

    # Step 2: summarize
    summary = summarize_context(base_context)

    # Step 3: hard limit
    summary = summary[:400]

    final_tokens = count_tokens(summary)

    # -------------------------
    # 📊 TOKEN COMPARISON
    # -------------------------
    saved = baseline_tokens - final_tokens
    percent = (saved / baseline_tokens) * 100 if baseline_tokens > 0 else 0

    print("\n--- TOKEN COMPARISON ---")
    print("Baseline:", baseline_tokens)
    print("Optimized:", final_tokens)
    print(f"Saved: {saved} ({percent:.2f}%)")
    print("------------------------\n")

    # -------------------------
    # FINAL PROMPT
    # -------------------------
    prompt = f"""
You are a helpful school tutor.

Subject: {subject}

Instructions:
- If math: solve step-by-step
- If science: explain simply
- If social science: explain clearly with examples

Context:
{summary}

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content, baseline_tokens, final_tokens