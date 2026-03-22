# Smart Document Chat Assistant 📚

A local RAG (Retrieval Augmented Generation) system that lets you upload PDFs and chat with their content using AI. This demonstrates practical AI implementation with real user-facing functionality.

## Features

- 📄 **PDF Upload & Processing**: Extract text from any PDF document
- 🔍 **Smart Search**: Uses FAISS vector search to find relevant content
- 💬 **AI Chat**: Chat with your documents using OpenAI's GPT models
- 🧠 **RAG Implementation**: Combines retrieval with generation for accurate answers
- 🎨 **Clean UI**: Beautiful Streamlit interface

## Tech Stack

- **Python** - Core language
- **Streamlit** - Web interface
- **OpenAI API** - Language model for chat
- **LangChain** - AI application framework
- **FAISS** - Vector similarity search
- **PyPDF2** - PDF text extraction

## Setup Instructions

1. **Install dependencies:**
   bash
   pip install -r requirements.txt
   

2. **Get OpenAI API Key:**
   - Visit https://platform.openai.com/api-keys
   - Create a new API key
   - Keep it handy for the app

3. **Run the application:**
   bash
   streamlit run app.py
   

4. **Use the app:**
   - Enter your OpenAI API key in the sidebar
   - Upload a PDF document
   - Click "Process Document"
   - Start chatting with your document!

## How It Works

1. **Document Processing**: PDFs are converted to text and split into manageable chunks
2. **Embedding Creation**: Text chunks are converted to vector embeddings using OpenAI
3. **Vector Storage**: Embeddings are stored in a FAISS index for fast similarity search
4. **Query Processing**: User questions are embedded and matched against document chunks
5. **Response Generation**: Relevant chunks are sent to GPT along with the question for contextual answers

## Project Structure


├── app.py                 # Main Streamlit application
├── document_processor.py  # PDF processing and vector store creation
├── chat_assistant.py      # Chat functionality with RAG
├── requirements.txt       # Python dependencies
└── README.md             # This file


## Next Steps

- Add support for multiple document formats (Word, TXT, etc.)
- Implement conversation memory for multi-turn dialogues
- Add document source highlighting
- Create user authentication and document management
- Deploy to cloud platforms (Streamlit Cloud, Heroku, etc.)

## Troubleshooting

- **API Key Issues**: Make sure your OpenAI API key is valid and has sufficient credits
- **PDF Processing**: Some PDFs might have text as images - consider adding OCR support
- **Memory Issues**: For large documents, consider using a more powerful vector database

Happy coding! 🚀