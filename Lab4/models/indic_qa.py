from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch

def answer_indic(question, context, lang="hi"):
    """Answer questions in Indic languages using IndicBERTv2 fine-tuned for QA (Hindi default)"""
    try:
        print(f"Loading IndicBERTv2 QA model for language: {lang}...")
        
        # Use the appropriate language-specific fine-tuned model
        if lang == "hi":
            model_name = "ai4bharat/IndicBERTv2-MLQA-hi"
        else:
            return f"Language '{lang}' not supported yet in this script."

        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForQuestionAnswering.from_pretrained(model_name)

        inputs = tokenizer(question, context, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)

        start_idx = torch.argmax(outputs.start_logits)
        end_idx = torch.argmax(outputs.end_logits) + 1

        answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][start_idx:end_idx]))
        return answer.strip()
    except Exception as e:
        print(f"Error in Indic QA: {e}")
        return f"Sorry, I couldn't process your question in Indic language. Error: {e}"
