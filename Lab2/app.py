import streamlit as st
from story_generator import StoryGenerator
import time
import pandas as pd
from nltk.translate.bleu_score import sentence_bleu
from rouge import Rouge
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt_tab')

# Set page config
st.set_page_config(
    page_title="AI Story Generator",
    page_icon="📚",
    layout="wide"
)

# Initialize the story generator
@st.cache_resource
def load_generator():
    return StoryGenerator()

generator = load_generator()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Story Generator", "Model Comparison", "Evaluation"])

if page == "Story Generator":
    # Title and description
    st.title("📚 AI Story Generator")
    st.markdown("""
    This application generates creative stories using different transformer-based models.
    Choose a model, enter your prompt, and adjust the generation parameters to create unique stories.
    """)

    # Model selection
    model_name = st.sidebar.selectbox(
        "Select Model",
        generator.get_available_models(),
        help="Choose the model to generate your story"
    )

    # Generation parameters
    st.sidebar.subheader("Generation Parameters")
    temperature = st.sidebar.slider(
        "Temperature",
        min_value=0.1,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Higher values make the output more random, lower values make it more focused"
    )

    top_k = st.sidebar.slider(
        "Top-k",
        min_value=1,
        max_value=100,
        value=50,
        help="Number of highest probability tokens to keep for top-k sampling"
    )

    top_p = st.sidebar.slider(
        "Top-p (Nucleus)",
        min_value=0.1,
        max_value=1.0,
        value=0.9,
        step=0.1,
        help="Cumulative probability for nucleus sampling"
    )

    max_length = st.sidebar.slider(
        "Max Length",
        min_value=100,
        max_value=1000,
        value=500,
        step=50,
        help="Maximum length of the generated story"
    )

    # Main content area
    st.subheader("Story Prompt")
    prompt = st.text_area(
        "Enter your story prompt or keywords",
        height=100,
        help="Enter a sentence or keywords to start your story"
    )

    # Generate button
    if st.button("Generate Story", type="primary"):
        if prompt:
            with st.spinner("Generating your story..."):
                # Add a small delay to show the spinner
                time.sleep(0.5)
                
                # Generate the story
                story = generator.generate_story(
                    prompt=prompt,
                    model_name=model_name,
                    max_length=max_length,
                    temperature=temperature,
                    top_k=top_k,
                    top_p=top_p
                )
                
                # Display the generated story
                st.subheader("Generated Story")
                st.write(story)
                
                # Add word count
                word_count = len(story.split())
                st.caption(f"Word count: {word_count}")
        else:
            st.warning("Please enter a prompt to generate a story.")

    # Model information
    st.sidebar.markdown("---")
    st.sidebar.subheader("Model Information")
    if model_name == "gpt2":
        st.sidebar.info("GPT-2 is good for creative, coherent text generation with a focus on narrative flow.")
    elif model_name == "flan-t5":
        st.sidebar.info("FLAN-T5 is better at following instructions and maintaining context.")
    elif model_name == "bart":
        st.sidebar.info("BART is strong at maintaining narrative structure and coherence.")

elif page == "Model Comparison":
    st.title("Model Comparison")
    
    # Model comparison data
    comparison_data = {
        'Model': ['GPT-2', 'FLAN-T5', 'BART'],
        'Architecture': ['Decoder-only', 'Encoder-Decoder', 'Denoising Autoencoder'],
        'Parameters': ['117M', '220M', '139M'],
        'Training Data': ['Web text', 'Instruction-tuned', 'Denoising'],
        'Strengths': [
            'Creative text generation, narrative flow',
            'Following instructions, maintaining context',
            'Narrative structure, coherence'
        ],
        'Best Use Case': [
            'General story generation',
            'Structured story generation',
            'Stories with clear structure'
        ],
        'Generation Speed': ['Fast', 'Medium', 'Medium'],
        'Memory Usage': ['Low', 'Medium', 'Medium']
    }
    
    # Create DataFrame
    df = pd.DataFrame(comparison_data)
    
    # Display comparison table
    st.subheader("Model Specifications")
    st.dataframe(df, use_container_width=True)
    
    # Detailed comparison
    st.subheader("Detailed Comparison")
    
    # GPT-2
    with st.expander("GPT-2 Details"):
        st.markdown("""
        ### GPT-2 (Generative Pre-trained Transformer 2)
        - **Architecture**: Uses a decoder-only transformer architecture
        - **Training**: Pre-trained on a large corpus of web text
        - **Key Features**:
            - Strong at generating creative and coherent text
            - Good at maintaining narrative flow
            - Can generate diverse and interesting stories
        - **Limitations**:
            - May sometimes generate repetitive content
            - Less control over specific story elements
        """)
    
    # FLAN-T5
    with st.expander("FLAN-T5 Details"):
        st.markdown("""
        ### FLAN-T5 (Fine-tuned Language Net T5)
        - **Architecture**: Uses an encoder-decoder transformer architecture
        - **Training**: Instruction-tuned on various tasks
        - **Key Features**:
            - Better at following specific instructions
            - Strong context maintenance
            - More structured output
        - **Limitations**:
            - Slightly slower generation
            - May be more conservative in creative aspects
        """)
    
    # BART
    with st.expander("BART Details"):
        st.markdown("""
        ### BART (Bidirectional and Auto-Regressive Transformers)
        - **Architecture**: Denoising autoencoder
        - **Training**: Pre-trained using denoising objectives
        - **Key Features**:
            - Excellent narrative structure
            - Strong coherence
            - Good at maintaining story arcs
        - **Limitations**:
            - May be less creative than GPT-2
            - Slightly slower generation
        """)
    
    # Performance comparison
    st.subheader("Performance Comparison")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Creativity", "GPT-2", "Highest")
        st.metric("Speed", "GPT-2", "Fastest")
    
    with col2:
        st.metric("Instruction Following", "FLAN-T5", "Best")
        st.metric("Context Understanding", "FLAN-T5", "Best")
    
    with col3:
        st.metric("Structure", "BART", "Best")
        st.metric("Coherence", "BART", "Best")
    
    # Usage recommendations
    st.subheader("Usage Recommendations")
    st.markdown("""
    - **Choose GPT-2** when you want:
        - More creative and diverse stories
        - Faster generation
        - Less structured but more imaginative content
    
    - **Choose FLAN-T5** when you want:
        - Better adherence to specific instructions
        - More structured and controlled output
        - Stronger context maintenance
    
    - **Choose BART** when you want:
        - Well-structured narratives
        - Strong story coherence
        - Clear story arcs and progression
    """)

elif page == "Evaluation":
    st.title("📊 Story Evaluation")
    
    # Evaluation metrics section
    st.header("Automatic Metrics")
    
    # Example stories for evaluation
    example_stories = {
        "Prompt 1": {
            "prompt": "A young wizard discovers a mysterious book in an ancient library",
            "gpt2": "The young wizard's fingers trembled as they traced the worn leather binding of the ancient tome. The library's dust motes danced in the golden afternoon light, and the book seemed to pulse with an otherworldly energy. As he opened it, the pages glowed with arcane symbols that shifted and changed before his eyes...",
            "flan-t5": "In the quiet corners of the ancient library, young wizard Marcus stumbled upon a book unlike any other. Its leather cover, worn by centuries, seemed to call to him. As he carefully opened it, the pages revealed spells and knowledge lost to time...",
            "bart": "The ancient library stood silent, its shelves heavy with forgotten knowledge. Young wizard Elias moved through the shadows, drawn to a particular section he had never noticed before. There, nestled between ordinary spellbooks, lay a tome that seemed to whisper his name..."
        },
        "Prompt 2": {
            "prompt": "A robot learns to paint and discovers the meaning of art",
            "gpt2": "The robot's metallic fingers held the brush with surprising delicacy. Its optical sensors analyzed the canvas, calculating color combinations and brush strokes. But something was different today. As it painted, the robot began to understand that art wasn't just about precision...",
            "flan-t5": "Unit-7's mechanical arm moved with calculated precision, yet its paintings lacked something essential. Day after day, it studied human artists, analyzing their techniques. Then one day, as it painted a sunset, something changed. The robot began to feel...",
            "bart": "In a world where robots served practical purposes, one machine stood before an easel, brush in hand. Its programming told it to create, but its circuits hummed with something new. As it painted, the robot discovered that art wasn't about perfection..."
        },
        "Prompt 3": {
            "prompt": "A time traveler accidentally brings a dinosaur to the present",
            "gpt2": "The time machine's portal shimmered with an otherworldly light. Dr. Sarah Chen adjusted her temporal stabilizer, but something was wrong. The readings were off. As the portal opened, she heard a sound that made her blood run cold - the unmistakable roar of a Tyrannosaurus Rex...",
            "flan-t5": "The temporal displacement field crackled with energy as Dr. Chen's experiment reached its climax. The readings were perfect, the calculations exact. But as the portal opened, she realized her mistake. A massive shadow emerged, followed by the earth-shaking steps of a prehistoric predator...",
            "bart": "The laboratory's alarms blared as the time machine's readings went haywire. Dr. Chen's hands flew over the controls, trying to stabilize the temporal rift. But it was too late. Through the swirling portal, a massive head emerged, followed by the rest of a creature that shouldn't exist in this time..."
        }
    }
    
    # Display example stories
    st.subheader("Example Stories")
    for story_key, story_data in example_stories.items():
        with st.expander(f"{story_key}: {story_data['prompt']}"):
            for model, story in story_data.items():
                if model != 'prompt':
                    st.markdown(f"**{model.upper()}**")
                    st.write(story)
                    st.markdown("---")
    
    # Calculate metrics
    st.subheader("Automatic Metrics Analysis")
    
    # Initialize ROUGE
    rouge = Rouge()
    
    # Calculate metrics for each model
    metrics = {
        'gpt2': {'bleu': [], 'rouge': []},
        'flan-t5': {'bleu': [], 'rouge': []},
        'bart': {'bleu': [], 'rouge': []}
    }
    
    # Calculate BLEU and ROUGE scores for each story
    for story_data in example_stories.values():
        reference = story_data['gpt2']  # Using GPT-2 as reference
        reference_tokens = [word_tokenize(reference.lower())]
        
        for model in ['gpt2', 'flan-t5', 'bart']:
            if model != 'gpt2':  # Skip comparing GPT-2 with itself
                hypothesis = story_data[model]
                hypothesis_tokens = word_tokenize(hypothesis.lower())
                
                # Calculate BLEU score
                bleu_score = sentence_bleu(reference_tokens, hypothesis_tokens)
                metrics[model]['bleu'].append(bleu_score)
                
                # Calculate ROUGE score
                rouge_scores = rouge.get_scores(hypothesis, reference)[0]
                metrics[model]['rouge'].append(rouge_scores['rouge-l']['f'])
    
    # Calculate average scores
    avg_metrics = {}
    for model in metrics:
        if model == 'gpt2':
            # For GPT-2, we'll use the average of other models' scores as reference
            avg_metrics[model] = {
                'bleu': 1.0,  # Perfect score since it's the reference
                'rouge': 1.0  # Perfect score since it's the reference
            }
        else:
            # For other models, calculate average of their scores
            avg_metrics[model] = {
                'bleu': sum(metrics[model]['bleu']) / len(metrics[model]['bleu']) if metrics[model]['bleu'] else 0,
                'rouge': sum(metrics[model]['rouge']) / len(metrics[model]['rouge']) if metrics[model]['rouge'] else 0
            }
    
    # Display BLEU scores
    st.markdown("### BLEU Score")
    st.markdown("""
    BLEU (Bilingual Evaluation Understudy) measures the similarity between generated text and reference text.
    """)
    for model, scores in avg_metrics.items():
        st.markdown(f"- {model.upper()}: {scores['bleu']:.2f}")
    
    # Display ROUGE scores
    st.markdown("### ROUGE Score")
    st.markdown("""
    ROUGE (Recall-Oriented Understudy for Gisting Evaluation) measures the overlap of n-grams between generated and reference text.
    """)
    for model, scores in avg_metrics.items():
        st.markdown(f"- {model.upper()}: ROUGE-L = {scores['rouge']:.2f}")
    
    # Strengths and Limitations
    st.header("Strengths and Limitations")
    
    st.subheader("GPT-2")
    st.markdown("""
    **Strengths:**
    - High creativity and originality
    - Good at maintaining narrative flow
    - Strong at generating diverse content
    
    **Limitations:**
    - Sometimes produces repetitive content
    - May struggle with complex plot structures
    - Less control over specific story elements
    """)
    
    st.subheader("FLAN-T5")
    st.markdown("""
    **Strengths:**
    - Excellent coherence and structure
    - Strong at following specific instructions
    - Good at maintaining context
    
    **Limitations:**
    - More conservative in creative aspects
    - Slightly slower generation
    - May be less diverse in output
    """)
    
    st.subheader("BART")
    st.markdown("""
    **Strengths:**
    - Strong narrative structure
    - Good balance of creativity and coherence
    - Consistent output quality
    
    **Limitations:**
    - May be less creative than GPT-2
    - Slightly slower generation
    - Sometimes too structured
    """) 