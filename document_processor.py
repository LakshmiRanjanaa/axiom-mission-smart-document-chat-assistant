import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
import streamlit as st

class DocumentProcessor:
    """Handles PDF processing and vector store creation"""
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # Size of each text chunk
            chunk_overlap=200,  # Overlap between chunks to maintain context
            length_function=len,
        )
        self.embeddings = OpenAIEmbeddings()  # OpenAI embeddings for text vectorization
    
    def extract_text_from_pdf(self, uploaded_file):
        """Extract text content from uploaded PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            
            # Extract text from each page
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                text += f"\n--- Page {page_num + 1} ---\n{page_text}"
            
            return text
        
        except Exception as e:
            st.error(f"Error extracting text from PDF: {str(e)}")
            return None
    
    def create_text_chunks(self, text):
        """Split text into manageable chunks for processing"""
        if not text:
            return []
        
        # Create Document objects for LangChain processing
        documents = [Document(page_content=text, metadata={"source": "uploaded_pdf"})]
        
        # Split documents into smaller chunks
        chunks = self.text_splitter.split_documents(documents)
        
        return chunks
    
    def create_vector_store(self, chunks):
        """Create FAISS vector store from text chunks"""
        if not chunks:
            return None
        
        try:
            # Create vector store using FAISS (Facebook AI Similarity Search)
            vector_store = FAISS.from_documents(chunks, self.embeddings)
            return vector_store
        
        except Exception as e:
            st.error(f"Error creating vector store: {str(e)}")
            return None
    
    def process_pdf(self, uploaded_file):
        """Complete pipeline: PDF -> text -> chunks -> vector store"""
        # Step 1: Extract text from PDF
        text = self.extract_text_from_pdf(uploaded_file)
        if not text:
            return None
        
        # Step 2: Split text into chunks
        chunks = self.create_text_chunks(text)
        if not chunks:
            st.error("No text chunks created from the document")
            return None
        
        st.info(f"Created {len(chunks)} text chunks from your document")
        
        # Step 3: Create vector store for similarity search
        vector_store = self.create_vector_store(chunks)
        
        return vector_store