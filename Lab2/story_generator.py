import torch
from transformers import (
    GPT2LMHeadModel, GPT2Tokenizer,
    T5ForConditionalGeneration, T5Tokenizer,
    BartForConditionalGeneration, BartTokenizer
)
import numpy as np

class StoryGenerator:
    def __init__(self):
        # Initialize models and tokenizers
        self.models = {
            'gpt2': {
                'model': GPT2LMHeadModel.from_pretrained('gpt2'),
                'tokenizer': GPT2Tokenizer.from_pretrained('gpt2')
            },
            'flan-t5': {
                'model': T5ForConditionalGeneration.from_pretrained('google/flan-t5-base'),
                'tokenizer': T5Tokenizer.from_pretrained('google/flan-t5-base')
            },
            'bart': {
                'model': BartForConditionalGeneration.from_pretrained('facebook/bart-base'),
                'tokenizer': BartTokenizer.from_pretrained('facebook/bart-base')
            }
        }
        
        # Move models to GPU if available
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        for model_info in self.models.values():
            model_info['model'].to(self.device)

    def generate_story(self, prompt, model_name='gpt2', max_length=500, 
                      temperature=0.7, top_k=50, top_p=0.9):
        """
        Generate a story based on the given prompt using the specified model.
        
        Args:
            prompt (str): The story prompt or keywords
            model_name (str): Name of the model to use ('gpt2', 'flan-t5', or 'bart')
            max_length (int): Maximum length of the generated story
            temperature (float): Sampling temperature
            top_k (int): Top-k sampling parameter
            top_p (float): Top-p (nucleus) sampling parameter
            
        Returns:
            str: Generated story
        """
        model_info = self.models[model_name]
        model = model_info['model']
        tokenizer = model_info['tokenizer']
        
        # Format prompt based on model
        if model_name == 'flan-t5':
            prompt = f"Write a story about: {prompt}"
        elif model_name == 'bart':
            prompt = f"Write a story: {prompt}"
            
        # Tokenize input
        inputs = tokenizer(prompt, return_tensors='pt').to(self.device)
        
        # Generate story
        with torch.no_grad():
            if model_name == 'gpt2':
                outputs = model.generate(
                    inputs['input_ids'],
                    max_length=max_length,
                    temperature=temperature,
                    top_k=top_k,
                    top_p=top_p,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id
                )
            else:  # T5 and BART
                outputs = model.generate(
                    inputs['input_ids'],
                    max_length=max_length,
                    temperature=temperature,
                    top_k=top_k,
                    top_p=top_p,
                    do_sample=True,
                    num_beams=4,
                    early_stopping=True
                )
        
        # Decode and return the generated text
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Clean up the generated text
        if model_name == 'gpt2':
            # Remove the prompt from the generated text
            generated_text = generated_text[len(prompt):].strip()
        
        return generated_text

    def get_available_models(self):
        """Return list of available models"""
        return list(self.models.keys()) 