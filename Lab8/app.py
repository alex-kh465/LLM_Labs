import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from deep_translator import GoogleTranslator
from langdetect import detect
from langchain.schema import Document

# --- Helper: Split translation into safe chunks (only for LLM response) ---
def translate_large_text(text, source_lang, target_lang, chunk_size=4000):
    translator = GoogleTranslator(source=source_lang, target=target_lang)
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    translated_chunks = [translator.translate(chunk) for chunk in chunks]
    return " ".join(translated_chunks)

# --- PAGE CONFIG ---
st.set_page_config(page_title="Domain Chatbot (Lab 8)", layout="centered")
st.title("💬 Domain-Specific Chatbot with LangChain + Groq")

# --- 1. LOAD DOMAIN KNOWLEDGE ---
st.sidebar.header("1. Upload Domain Data")
uploaded_file = st.sidebar.file_uploader("Upload a TXT file", type=["txt"])

if uploaded_file:
    # Read uploaded text file
    file_content = uploaded_file.read().decode("utf-8")
    documents = [Document(page_content=file_content)]
    
    # Split text into chunks
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = splitter.split_documents(documents)
    
    # Create vector store using FAISS
    embeddings = HuggingFaceEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k":3})

    # --- 2. SETUP LLM (Groq) ---
    st.sidebar.header("2. LLM API Key")
    groq_api_key = st.sidebar.text_input("Enter Groq API Key", type="password")
    if groq_api_key:
        llm = ChatGroq(api_key=groq_api_key, model_name="openai/gpt-oss-20b")  # or llama3

        # --- 3. BUILD RAG CHAIN ---
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff"
        )

        # --- 4. MULTILINGUAL CHAT ---
        user_query = st.text_input("Ask me anything (any language):")

        if user_query:
            # Detect language
            detected_lang = detect(user_query)
            
            # Translate user query directly (short input = no chunking needed)
            query_en = GoogleTranslator(source='auto', target='en').translate(user_query)
            
            # Get response from LLM
            answer_en = qa_chain.run(query_en)
            
            # Translate LLM response back to original language using chunking
            final_answer = translate_large_text(answer_en, "en", detected_lang)
            
            st.markdown("**Answer:**")
            st.write(final_answer)
    else:
        st.warning("Please enter your Groq API key to continue.")
else:
    st.info("Please upload a domain-specific TXT file to get started.")
