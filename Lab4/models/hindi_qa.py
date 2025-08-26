from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch

# Load once globally (Hindi model)
model_name_hi = "ai4bharat/indic-bert"
tokenizer_hi = AutoTokenizer.from_pretrained(model_name_hi)
model_hi = AutoModelForQuestionAnswering.from_pretrained(model_name_hi)

# Base Hindi context
base_context_hi = """
सौरमंडल सूर्य और उसके चारों ओर परिक्रमा करने वाले ग्रहों, उपग्रहों, क्षुद्रग्रहों और धूमकेतुओं का समूह है। 
इसमें आठ ग्रह शामिल हैं: बुध, शुक्र, पृथ्वी, मंगल, बृहस्पति, शनि, यूरेनस और नेपच्यून। 
सूर्य इस प्रणाली का केंद्र है और यह सभी ग्रहों को अपने गुरुत्वाकर्षण बल से बाँधे रखता है। 
पृथ्वी तीसरा ग्रह है और यह जीवन को बनाए रखने में सक्षम है। 
शनि के चारों ओर सुंदर वलय होते हैं और बृहस्पति सबसे बड़ा ग्रह है।
"""

def answer_hindi(question, extra_context=None, lang="hi"):
    """
    Answer Hindi questions using IndicBERTv2 QA model.

    Parameters:
        question (str): Hindi question.
        extra_context (str or None): Additional context to append (optional).
        lang (str): Language code (default is 'hi').

    Returns:
        str: Extracted answer from the combined context.
    """
    try:
        if lang == "hi":
            tokenizer = tokenizer_hi
            model = model_hi
            context = base_context_hi
        else:
            return f"Language '{lang}' not supported yet."

        # Append extra context if provided
        if extra_context:
            context = f"{context.strip()}\n{extra_context.strip()}"

        # Tokenize inputs
        inputs = tokenizer(question, context, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)

        # Get predicted answer span
        start_idx = torch.argmax(outputs.start_logits)
        end_idx = torch.argmax(outputs.end_logits) + 1

        answer = tokenizer.convert_tokens_to_string(
            tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][start_idx:end_idx])
        )

        return answer.strip()
    except Exception as e:
        return f"Error during QA inference: {e}"
