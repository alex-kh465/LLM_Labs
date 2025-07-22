from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch

def answer_french(question, context):
    """Answer questions in French using CamemBERT fine-tuned on FQuAD"""
    try:
        print("Loading CamemBERT QA model...")

        model_name = "illuin/camembert-base-fquad"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForQuestionAnswering.from_pretrained(model_name)

        inputs = tokenizer(question, context, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)

        start_idx = torch.argmax(outputs.start_logits)
        end_idx = torch.argmax(outputs.end_logits) + 1

        answer = tokenizer.convert_tokens_to_string(
            tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][start_idx:end_idx])
        )
        return answer.strip()
    except Exception as e:
        print(f"Error in French QA: {e}")
        return f"Sorry, I couldn't process your question in French. Error: {e}"
