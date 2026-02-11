
"""
Company Knowledge Page (RAG)
"""
import streamlit as st
import tempfile
import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import config

# Initialize embeddings model only once
@st.cache_resource
def get_embeddings_model():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def format_docs(docs):
    """Format retrieved documents into a single context string."""
    return "\n\n".join(doc.page_content for doc in docs)

def process_document(uploaded_file):
    """
    Process uploaded document into vector store
    """
    try:
        # Save temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        # Load document
        if uploaded_file.name.endswith('.pdf'):
            loader = PyPDFLoader(tmp_path)
        else:
            loader = TextLoader(tmp_path)
            
        docs = loader.load()
        
        # Split text
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        final_documents = text_splitter.split_documents(docs)
        
        # Create vectors
        embeddings = get_embeddings_model()
        vector_store = FAISS.from_documents(final_documents, embeddings)
        
        # Cleanup
        os.unlink(tmp_path)
        
        return vector_store
        
    except Exception as e:
        st.error(f"Error processing document: {str(e)}")
        return None

def show():
    st.markdown('<h2 class="gradient-header">🏢 Company Knowledge Base</h2>', unsafe_allow_html=True)
    st.markdown("Upload company documents (PDF/TXT) and ask questions about products.")

    # Sidebar for upload
    with st.sidebar:
        st.markdown("### 📂 Document Upload")
        uploaded_file = st.file_uploader("Upload Product Catalog/Docs", type=['pdf', 'txt'])
        
        if st.button("🗑️ Clear Context", use_container_width=True):
            if "vector_store" in st.session_state:
                del st.session_state.vector_store
            if "process_file" in st.session_state:
                del st.session_state.process_file
            st.rerun()

    # Process File
    if uploaded_file and ("process_file" not in st.session_state or st.session_state.process_file != uploaded_file.name):
        with st.spinner("Processing document... (This typically takes 10-20 seconds)"):
            vector_store = process_document(uploaded_file)
            if vector_store:
                st.session_state.vector_store = vector_store
                st.session_state.process_file = uploaded_file.name
                st.success("✅ Document processed successfully!")
            else:
                st.error("Failed to process document.")
    
    # Check if context exists
    if "vector_store" not in st.session_state:
        st.info("👈 Please upload a document in the sidebar to start chatting.")
        return

    # Chat Interface
    st.markdown("---")
    
    # Initialize chat history
    if "rag_chat_history" not in st.session_state:
        st.session_state.rag_chat_history = []

    # Display history
    for message in st.session_state.rag_chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input
    if prompt := st.chat_input("Ask about products in the document..."):
        # User message
        st.session_state.rag_chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI Response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing document..."):
                try:
                    llm = ChatGroq(
                        groq_api_key=config.GROQ_API_KEY,
                        model_name="llama-3.3-70b-versatile"
                    )
                    
                    # Strict System Prompt
                    prompt_template = ChatPromptTemplate.from_template(
                        """
                        Answer the questions based on the provided context only.
                        If the answer is not in the context, reply exactly: "Product information not found in the uploaded document."
                        Do not hallucinate or use outside knowledge.
                        
                        <context>
                        {context}
                        </context>
                        
                        Question: {input}
                        """
                    )
                    
                    # Build LCEL retrieval chain (replaces deprecated create_stuff_documents_chain / create_retrieval_chain)
                    retriever = st.session_state.vector_store.as_retriever()
                    
                    rag_chain = (
                        {"context": retriever | format_docs, "input": RunnablePassthrough()}
                        | prompt_template
                        | llm
                        | StrOutputParser()
                    )
                    
                    answer = rag_chain.invoke(prompt)
                    
                    st.markdown(answer)
                    st.session_state.rag_chat_history.append({"role": "assistant", "content": answer})
                    
                except Exception as e:
                    st.error(f"Error generating response: {str(e)}")
