import streamlit as st
import os
from document_processor import DocumentProcessor
from chat_assistant import ChatAssistant

# Set page config
st.set_page_config(page_title="Smart Document Chat Assistant", page_icon="📚", layout="wide")

def main():
    st.title("📚 Smart Document Chat Assistant")
    st.markdown("Upload a PDF and chat with its content using AI!")
    
    # Initialize session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'document_processed' not in st.session_state:
        st.session_state.document_processed = False
    if 'chat_assistant' not in st.session_state:
        st.session_state.chat_assistant = None
    
    # Sidebar for document upload
    with st.sidebar:
        st.header("Document Upload")
        
        # API Key input
        api_key = st.text_input("OpenAI API Key", type="password", 
                               help="Enter your OpenAI API key to enable chat functionality")
        
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        
        if uploaded_file is not None and api_key:
            if st.button("Process Document"):
                with st.spinner("Processing document..."):
                    # Process the document
                    processor = DocumentProcessor()
                    vector_store = processor.process_pdf(uploaded_file)
                    
                    # Initialize chat assistant
                    st.session_state.chat_assistant = ChatAssistant(vector_store)
                    st.session_state.document_processed = True
                    st.session_state.chat_history = []
                    
                st.success("Document processed successfully! You can now chat with it.")
    
    # Main chat interface
    if st.session_state.document_processed and st.session_state.chat_assistant:
        st.header("💬 Chat with your document")
        
        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask a question about your document..."):
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = st.session_state.chat_assistant.get_response(prompt)
                    st.markdown(response)
            
            # Add assistant response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    else:
        st.info("👆 Upload a PDF file and enter your OpenAI API key in the sidebar to get started!")
        
        # Instructions
        st.markdown("""
        ### How to use:
        1. **Get an OpenAI API key** from https://platform.openai.com/api-keys
        2. **Enter your API key** in the sidebar
        3. **Upload a PDF** document you want to chat with
        4. **Click "Process Document"** to analyze the content
        5. **Start chatting** with your document!
        
        ### Features:
        - Extract text from PDF documents
        - Create searchable embeddings of document content
        - Ask questions and get AI-powered answers based on your document
        - Maintain conversation history during your session
        """)

if __name__ == "__main__":
    main()