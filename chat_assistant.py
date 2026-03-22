from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import streamlit as st

class ChatAssistant:
    """Handles chat functionality with document context"""
    
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.llm = OpenAI(temperature=0.7)  # Language model with some creativity
        
        # Custom prompt template for better responses
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""
You are a helpful assistant that answers questions based on the provided document content.
Use the following pieces of context to answer the question at the end.
If you don't know the answer based on the context, just say that you don't know.
Don't make up information that's not in the document.

Context: {context}

Question: {question}

Answer: """
        )
        
        # Create the retrieval QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",  # Stuff all retrieved docs into the prompt
            retriever=self.vector_store.as_retriever(
                search_kwargs={"k": 3}  # Retrieve top 3 most relevant chunks
            ),
            chain_type_kwargs={
                "prompt": self.prompt_template
            },
            return_source_documents=True  # Include source info in response
        )
    
    def get_response(self, question):
        """Get AI response to user question based on document content"""
        try:
            # Query the document using retrieval-augmented generation
            result = self.qa_chain({"query": question})
            
            # Extract the answer
            answer = result["result"]
            
            # Optionally show which parts of the document were used
            source_docs = result.get("source_documents", [])
            
            if source_docs:
                # Add a note about the sources (optional - can be removed)
                answer += f"\n\n*Based on {len(source_docs)} relevant sections from your document.*"
            
            return answer
        
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            st.error(error_msg)
            return "I'm sorry, I encountered an error while processing your question. Please try again."
    
    def get_relevant_chunks(self, question, k=3):
        """Get relevant document chunks for a question (useful for debugging)"""
        try:
            retriever = self.vector_store.as_retriever(search_kwargs={"k": k})
            relevant_docs = retriever.get_relevant_documents(question)
            
            return [doc.page_content for doc in relevant_docs]
        
        except Exception as e:
            st.error(f"Error retrieving relevant chunks: {str(e)}")
            return []