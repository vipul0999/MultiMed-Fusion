# backend/ingest/llm_engines.py
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from django.conf import settings
import google.genai as genai

from django.conf import settings
from groq import Groq
# -----------------------------
# HuggingFace local model wrapper
# -----------------------------
hf_tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
hf_model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")

def call_hf_flant5(query: str, chunk: str, max_length=256) -> str:
    """Call HuggingFace Flan-T5 model locally with query + chunk."""
    prompt = f"""
    You are a medical assistant helping a doctor.

    Doctor's query: "{query}"
    Patient file context: "{chunk}"

    Answer the query based only on the patient file context. 
    If the context does not answer the query, reply: "Not enough information in records."
    """

    inputs = hf_tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        outputs = hf_model.generate(**inputs, max_length=max_length)
    answer = hf_tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer.strip()



# -----------------------------
# GPT4All local model wrapper
# # -----------------------------
# from gpt4all import GPT4All
#
# gpt4all_model = GPT4All(model_name="gpt4all-lora-quantized")  # make sure model is downloaded locally
#
# def call_gpt4all(text: str, max_tokens=256) -> str:
#     """Call GPT4All model locally."""
#     answer = gpt4all_model.generate(text, max_tokens=max_tokens)
#     return answer

# ========== Gemini Setup ==========


def call_gemini(query: str, chunk: str) -> str:
    GEMINI_API_KEY = settings.GEMINI_API_KEY

    gemini_client = genai.Client(api_key=GEMINI_API_KEY)

    """Call Gemini API for text generation."""
    prompt = (
        f"You are a medical assistant.\n"
        f"Doctor's query: {query}\n\n"
        f"Patient file: {chunk}\n\n"
        f"Answer strictly based on this context. "
    )
    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Gemini error: {str(e)}"




def call_groq(query: str, chunk: str) -> str:
    """
    Call Groq API for medical query + patient chunk.
    """
    GROQ_API_KEY = settings.GROQ_API_KEY
    groq_client = Groq(api_key=GROQ_API_KEY)

    prompt = (
        f"You are a medical assistant.\n"
        f"Doctor's query: {query}\n\n"
        f"Patient file context: {chunk}\n\n"
        f"Answer strictly based on the patient file context. "
        f"If the context does not contain the answer, respond with "
        f'"Not enough information in records."'
    )

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,  # Optional: for more consistent responses
            max_tokens=1024  # Optional: limit response length
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Groq error: {str(e)}"