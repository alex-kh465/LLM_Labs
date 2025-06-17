# Story Generation using Transformer Models

This project implements a story generation system using transformer-based models and provides a comparative study of different models for creative text generation.

## Models Used
1. GPT-2 (Small)
2. FLAN-T5 (Base)
3. BART (Base)

## Features
- Story generation from prompts
- Adjustable generation parameters (temperature, top-k, top-p)
- Interactive Streamlit interface
- Comparative analysis of different models

## Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Streamlit app:
```bash
streamlit run app.py
```

## Usage
1. Enter a story prompt or keywords
2. Select the model to use
3. Adjust generation parameters if desired
4. Click "Generate Story" to create your story

## Model Comparison
- GPT-2: Good for creative, coherent text generation
- FLAN-T5: Better at following instructions and maintaining context
- BART: Strong at maintaining narrative structure and coherence

## Implementation Details
The system uses the Hugging Face Transformers library and implements:
- Tokenization and prompt formatting
- Temperature-based sampling
- Top-k and top-p (nucleus) sampling
- Maximum length control
- Story coherence checks 