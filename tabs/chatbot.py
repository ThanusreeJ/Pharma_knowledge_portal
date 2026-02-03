"""
AI Chatbot Page
"""
import streamlit as st
from groq import Groq
import config


def get_groq_response(question: str, chat_history: list) -> str:
    """Get response from Groq AI"""
    try:
        if not config.GROQ_API_KEY:
            return "⚠️ Please set your GROQ_API_KEY in the .env file to use the chatbot.\n\nGet a free API key at: https://console.groq.com/"
        
        client = Groq(api_key=config.GROQ_API_KEY)
        
        # System prompt for pharma domain
        system_prompt = """You are a knowledgeable pharmaceutical AI assistant. You help users with:
        - Drug information and mechanisms of action
        - Clinical trial insights
        - Regulatory guidance (FDA, EMA)
        - Research paper summaries
        - Pharma industry news analysis
        - Healthcare and biotech topics
        
        Provide accurate, helpful responses. If unsure, suggest reliable sources like PubMed, FDA.gov, or ClinicalTrials.gov.
        Keep responses concise but informative. Always remind users to consult healthcare professionals for medical advice."""
        
        # Build messages
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add chat history
        for msg in chat_history[-10:]:  # Last 10 messages for context
            messages.append(msg)
        
        # Add current question
        messages.append({"role": "user", "content": question})
        
        # Get response
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=1024
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"❌ Error: {str(e)}\n\nPlease check your GROQ_API_KEY configuration."


def show():
    st.markdown('<h2 class="gradient-header">💬 Pharma Knowledge Chatbot</h2>', unsafe_allow_html=True)
    st.markdown("Ask questions about drugs, clinical trials, research, and pharma industry")
    
    # Initialize chat history if not exists
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for message in st.session_state.chat_history:
        role = message["role"]
        content = message["content"]
        
        if role == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(content)
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(content)
    
    # Chat input
    user_input = st.chat_input("Ask me anything about pharma...")
    
    if user_input:
        # Display user message
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
        
        # Add to history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Get AI response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Thinking..."):
                response = get_groq_response(user_input, st.session_state.chat_history)
            st.markdown(response)
        
        # Add to history
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response
        })
        
        st.rerun()
    
    # Sidebar with example questions
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 💡 Example Questions")
        
        examples = [
            "What is metformin used for?",
            "Explain Phase 3 clinical trials",
            "What are biologics?",
            "How does FDA drug approval work?",
            "Latest in cancer immunotherapy"
        ]
        
        for example in examples:
            if st.button(f"💬 {example}", use_container_width=True, key=f"ex_{example}"):
                st.session_state.example_question = example
                st.rerun()
        
        st.markdown("---")
        
        if st.button("🗑️ Clear Chat History", use_container_width=True, type="secondary"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Show placeholder if no messages
    if not st.session_state.chat_history:
        st.info("""
        👋 **Welcome to the Pharma Knowledge Chatbot!**
        
        I can help you with:
        - Drug information and usage
        - Clinical trial explanations
        - Regulatory guidance
        - Research paper insights
        - Industry trends and news
        
        Try asking a question below or click an example on the sidebar!
        """)
        
        # Check if API key is set
        if not config.GROQ_API_KEY:
            st.warning("""
            ⚠️ **Groq API Key Required**
            
            To use the chatbot, get a free API key at https://console.groq.com/
            
            Then create a `.env` file with:
            ```
            GROQ_API_KEY=your_key_here
            ```
            """)
