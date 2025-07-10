from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

def answer_english(question, context):
    """Answer questions in English using FLAN-T5"""
    try:
        print("Loading English model...")
        tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
        model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

        prompt = f"Answer the question based on the context.\nContext: {context[:1000]}\nQuestion: {question}"
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        outputs = model.generate(**inputs, max_length=128)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        print(f"Error in English QA: {e}")
        return f"Sorry, I couldn't process your question in English. Error: {e}"
