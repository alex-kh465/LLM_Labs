import streamlit as st
import os
from utils.pdf_utils import extract_text_from_pdf
from utils.stt import transcribe_audio
from utils.tts import speak
from models.english_qa import answer_english
from models.indic_qa import answer_hindi
from models.international_qa import answer_french
import tempfile

# Set page config
st.set_page_config(
    page_title="Multilingual QA System",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .language-section {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        background-color: #f8f9fa;
    }
    .answer-box {
        background-color: #e8f4fd;
        border-left: 4px solid #1f77b4;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
        color: #000000;
    }
    .error-box {
        background-color: #ffe6e6;
        border-left: 4px solid #ff4444;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'pdf_texts' not in st.session_state:
    st.session_state.pdf_texts = {}
if 'question' not in st.session_state:
    st.session_state.question = ""
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'show_answers' not in st.session_state:
    st.session_state.show_answers = False

def load_pdf_texts():
    """Load text from PDF files"""
    pdf_files = {
        'English': 'sample_docs/english solar.pdf',
        'Hindi': 'sample_docs/hindi solar.pdf',
        'French': 'sample_docs/french solar.pdf'
    }
    
    texts = {}
    for lang, file_path in pdf_files.items():
        if os.path.exists(file_path):
            try:
                texts[lang] = extract_text_from_pdf(file_path)
                st.success(f"✅ {lang} PDF loaded successfully")
            except Exception as e:
                st.error(f"❌ Error loading {lang} PDF: {e}")
                texts[lang] = ""
        else:
            st.warning(f"⚠️ {lang} PDF not found: {file_path}")
            texts[lang] = ""
    
    return texts



# Main app
def main():
    st.markdown('<h1 class="main-header">🌍 Multilingual Question Answering System</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📋 System Information")
        st.info("""
        This system can answer questions in:
        - 🇺🇸 English (FLAN-T5)
        - 🇮🇳 Hindi (Indic-BERT)
        - 🇫🇷 French (CamemBERT)
        
        Upload audio or type your question!
        """)
        
        st.header("📄 Document Status")
        if st.button("🔄 Load PDF Documents"):
            with st.spinner("Loading PDF documents..."):
                st.session_state.pdf_texts = load_pdf_texts()
    
    # Load PDFs if not already loaded
    if not st.session_state.pdf_texts:
        with st.spinner("Loading PDF documents..."):
            st.session_state.pdf_texts = load_pdf_texts()
    
    # Question input section
    st.header("❓ Ask Your Question")
    
    # Create tabs for different input methods
    tab1, tab2 = st.tabs(["💬 Text Input", "🎤 Audio Input"])
    
    with tab1:
        question = st.text_input(
            "Enter your question:",
            value=st.session_state.question,
            placeholder="e.g., What is solar system?"
        )
        if question:
            st.session_state.question = question
    
    with tab2:
        uploaded_audio = st.file_uploader(
            "Upload an audio file (WAV format)",
            type=['wav'],
            help="Upload a WAV audio file with your question"
        )
        
        if uploaded_audio is not None:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                tmp_file.write(uploaded_audio.read())
                temp_audio_path = tmp_file.name
            
            try:
                with st.spinner("🔊 Transcribing audio..."):
                    transcribed_question = transcribe_audio(temp_audio_path)
                    st.session_state.question = transcribed_question
                    st.success(f"📝 Transcribed: {transcribed_question}")
            except Exception as e:
                st.error(f"❌ Error transcribing audio: {e}")
            finally:
                # Clean up temporary file
                if os.path.exists(temp_audio_path):
                    os.unlink(temp_audio_path)
    
    # Answer questions if we have a question
    if st.session_state.question and st.button("🚀 Get Answers", type="primary"):
        question = st.session_state.question
        st.session_state.show_answers = True

        # Generate answers and store in session state
        with st.spinner("🧠 Processing your question in all languages..."):
            answers = {}

            # English Answer
            if st.session_state.pdf_texts.get('English'):
                try:
                    answers['english'] = answer_english(question, st.session_state.pdf_texts['English'])
                except Exception as e:
                    answers['english'] = f"Error: {e}"
            else:
                answers['english'] = "English PDF not available"

            # Malayalam Answer
            if st.session_state.pdf_texts.get('Hindi'):
                try:
                    answers['hindi'] = answer_hindi(question, st.session_state.pdf_texts['Hindi'])
                except Exception as e:
                    answers['hindi'] = f"Error: {e}"
            else:
                answers['hindi'] = "Hindi PDF not available"

            # French Answer
            if st.session_state.pdf_texts.get('French'):
                try:
                    answers['french'] = answer_french(question, st.session_state.pdf_texts['French'])
                except Exception as e:
                    answers['french'] = f"Error: {e}"
            else:
                answers['french'] = "French PDF not available"

            st.session_state.answers = answers

    # Display answers if available
    if st.session_state.show_answers and st.session_state.answers:
        st.header("🤖 AI Responses")

        # Add clear button
        if st.button("🔄 Ask New Question", type="secondary"):
            st.session_state.show_answers = False
            st.session_state.answers = {}
            st.session_state.question = ""
            st.rerun()

        # Create columns for different languages
        col1, col2, col3 = st.columns(3)
        
        # English Answer
        with col1:
            st.markdown('<div class="language-section">', unsafe_allow_html=True)
            st.subheader("🇺🇸 English Answer")

            english_answer = st.session_state.answers.get('english', '')
            if english_answer:
                st.markdown(f'<div class="answer-box"><strong>Answer:</strong> {english_answer}</div>', unsafe_allow_html=True)

                # Generate TTS for English
                if st.button("🔊 Generate English Audio", key="en_audio"):
                    with st.spinner("Generating speech..."):
                        try:
                            from gtts import gTTS
                            import tempfile
                            import time

                            # Create temporary file
                            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                                temp_path = tmp_file.name

                            # Generate TTS
                            tts = gTTS(text=english_answer, lang='en')
                            tts.save(temp_path)

                            # Read the audio file
                            with open(temp_path, 'rb') as audio_file:
                                audio_bytes = audio_file.read()

                            st.audio(audio_bytes, format='audio/mp3')
                            st.success("🎵 English audio generated!")

                            # Clean up with retry mechanism
                            try:
                                time.sleep(0.1)  # Small delay
                                os.unlink(temp_path)
                            except:
                                pass  # Ignore cleanup errors

                        except Exception as e:
                            st.error(f"TTS Error: {str(e)}")
            else:
                st.warning("⚠️ English answer not available")

            st.markdown('</div>', unsafe_allow_html=True)
        
        # Malayalam Answer
        with col2:
            st.markdown('<div class="language-section">', unsafe_allow_html=True)
            st.subheader("🇮🇳 Hindi Answer")

            hindi_ans = st.session_state.answers.get('hindi', '')
            if hindi_ans:
                st.markdown(f'<div class="answer-box"><strong>Answer:</strong> {hindi_ans}</div>', unsafe_allow_html=True)

                # Generate TTS for Malayalam
                if st.button("🔊 Generate Hindi Audio", key="ml_audio"):
                    with st.spinner("Generating speech..."):
                        try:
                            from gtts import gTTS
                            import tempfile
                            import time

                            # Create temporary file
                            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                                temp_path = tmp_file.name

                            # Generate TTS
                            tts = gTTS(text=hindi_ans, lang='ml')
                            tts.save(temp_path)

                            # Read the audio file
                            with open(temp_path, 'rb') as audio_file:
                                audio_bytes = audio_file.read()

                            st.audio(audio_bytes, format='audio/mp3')
                            st.success("🎵 Hindi audio generated!")

                            # Clean up with retry mechanism
                            try:
                                time.sleep(0.1)  # Small delay
                                os.unlink(temp_path)
                            except:
                                pass  # Ignore cleanup errors

                        except Exception as e:
                            st.error(f"TTS Error: {str(e)}")
            else:
                st.warning("⚠️Hindi answer not available")

            st.markdown('</div>', unsafe_allow_html=True)
        
        # French Answer
        with col3:
            st.markdown('<div class="language-section">', unsafe_allow_html=True)
            st.subheader("🇫🇷 French Answer")

            french_answer = st.session_state.answers.get('french', '')
            if french_answer:
                st.markdown(f'<div class="answer-box"><strong>Answer:</strong> {french_answer}</div>', unsafe_allow_html=True)

                # Generate TTS for French
                if st.button("🔊 Generate French Audio", key="fr_audio"):
                    with st.spinner("Generating speech..."):
                        try:
                            from gtts import gTTS
                            import tempfile
                            import time

                            # Create temporary file
                            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                                temp_path = tmp_file.name

                            # Generate TTS
                            tts = gTTS(text=french_answer, lang='fr')
                            tts.save(temp_path)

                            # Read the audio file
                            with open(temp_path, 'rb') as audio_file:
                                audio_bytes = audio_file.read()

                            st.audio(audio_bytes, format='audio/mp3')
                            st.success("🎵 French audio generated!")

                            # Clean up with retry mechanism
                            try:
                                time.sleep(0.1)  # Small delay
                                os.unlink(temp_path)
                            except:
                                pass  # Ignore cleanup errors

                        except Exception as e:
                            st.error(f"TTS Error: {str(e)}")
            else:
                st.warning("⚠️ French answer not available")

            st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        🌍 Multilingual QA System | Built with Streamlit & Transformers
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
