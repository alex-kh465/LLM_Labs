import streamlit as st
from story_generator import StoryGenerator
import time
import pandas as pd

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
page = st.sidebar.radio("Go to", ["Story Generator", "Model Comparison"])

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

else:  # Model Comparison page
    st.title("🤖 Model Comparison")
    
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