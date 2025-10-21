# backend/ingest/llm_aggregator.py
from .llm_engines import call_groq, call_gemini  #, call_gpt4all

def query_all_llms(text: str,query):
    """
    Call all integrated LLMs and return a structured response.
    """
    responses = []

    # # HuggingFace
    # hf_answer = call_hf_flant5(text,query)
    # responses.append({
    #     "model": "hf-flan-t5-small",
    #     "answer": hf_answer
    # })
    # Gemini
    gemini_answer = call_gemini(text, query)
    responses.append({"model": "gemini-2.5-flash", "answer": gemini_answer})

    groq_answer = call_groq(text,query)
    cleaned = groq_answer.replace("\n", " ").replace("\r", " ")
    cleaned = " ".join(cleaned.split())

    responses.append({"model":"groq","answer":cleaned})


    # gpt4all_answer = call_gpt4all(text)
    # responses.append({
    #     "model": "gpt4all-lora",
    #     "answer": gpt4all_answer
    # })

    return responses
