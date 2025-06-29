# ### main.py (Backend with memory, conditional sources, and LLM prompt) ###
# import os
# import json
# from fastapi import FastAPI, File, UploadFile, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import List, Dict, Any
# from datetime import datetime
# from document_processor import DocumentProcessor
# from pinecone_vectorstore import PineconeVectorStore
# from groq import Groq

# app = FastAPI()
# app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# vector_store = PineconeVectorStore(api_key=os.getenv('PINECONE_API_KEY'), index_name=os.getenv('INDEX_NAME'))
# groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))
# CHAT_HISTORY_DIR = "temp/chat_history"
# os.makedirs(CHAT_HISTORY_DIR, exist_ok=True)

# class QueryRequest(BaseModel):
#     query: str
#     chat_history: List[dict] = []
#     chat_id: str = None

# def save_chat_history(chat_id: str, messages: List[Dict[str, Any]]):
#     title = "New Chat"
#     for m in messages:
#         if m['role'] == 'user':
#             title = m['content'][:30] + ("..." if len(m['content']) > 30 else "")
#             break
#     data = {"chat_id": chat_id, "title": title, "timestamp": datetime.now().isoformat(), "messages": messages}
#     with open(os.path.join(CHAT_HISTORY_DIR, f"{chat_id}.json"), "w") as f:
#         json.dump(data, f, indent=2)

# def load_chat_history(chat_id: str) -> List[Dict[str, Any]]:
#     path = os.path.join(CHAT_HISTORY_DIR, f"{chat_id}.json")
#     if os.path.exists(path):
#         with open(path, "r") as f:
#             return json.load(f).get("messages", [])
#     return []

# def format_chat_history_for_llm(chat_history: List[Dict[str, Any]]) -> str:
#     pairs = []
#     for i in range(0, len(chat_history) - 1, 2):
#         if chat_history[i]['role'] == 'user' and chat_history[i+1]['role'] == 'assistant':
#             pairs.append((chat_history[i], chat_history[i+1]))
#     recent = pairs[-5:]
#     return "\n\n".join([f"User: {u['content']}\nAssistant: {a['content']}" for u, a in recent])

# @app.post("/upload")
# async def upload_document(file: UploadFile = File(...)):
#     path = f"temp/{file.filename}"
#     with open(path, "wb") as f:
#         f.write(await file.read())
#     if file.filename.endswith('.pdf'):
#         chunks = DocumentProcessor.read_pdf(path)
#     elif file.filename.endswith('.pptx'):
#         chunks = DocumentProcessor.read_pptx(path)
#     elif file.filename.endswith(('.xlsx', '.xls')):
#         chunks = DocumentProcessor.read_excel(path)
#     else:
#         os.remove(path)
#         raise HTTPException(400, "Unsupported file type")
#     vector_store.upsert_documents(chunks)
#     os.remove(path)
#     return {"message": "Success", "chunk_count": len(chunks)}

# @app.post("/query")
# async def query_documents(request: QueryRequest):
#     chat_id = request.chat_id or f"chat_{datetime.now().strftime('%Y%m%d%H%M%S')}_{os.urandom(4).hex()}"
#     chat_history = load_chat_history(chat_id)
#     query_results = vector_store.query(request.query)

#     if not query_results['matches']:
#         response = "I couldn't find relevant info in your documents. Please rephrase or upload more."
#         chat_history += [{"role": "user", "content": request.query}, {"role": "assistant", "content": response}]
#         save_chat_history(chat_id, chat_history)
#         return {"answer": response, "sources": [], "chat_id": chat_id}

#     context = "\n\n".join([m['metadata']['text'] for m in query_results['matches']])
#     memory = format_chat_history_for_llm(chat_history)
#     system_prompt = """
# You are a helpful document assistant. Follow these rules:
# - Use ONLY the document context for factual answers.
# - Use chat history to interpret pronouns or references.
# - Show sources (like page/file name) ONLY when the answer uses document information.
# - DO NOT show sources for greetings or general chit-chat.
# """

#     user_prompt = f"""Document Context:\n{context}\n\n"
#     if memory:
#         user_prompt += f"Previous Conversation:\n{memory}\n\n"
#     user_prompt += f"User Message: {request.query}"

#     result = groq_client.chat.completions.create(
#         messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
#         model="llama-3.3-70b-versatile",
#         temperature=0
#     )

#     response = result.choices[0].message.content
#     chat_history += [{"role": "user", "content": request.query}, {"role": "assistant", "content": response}]
#     save_chat_history(chat_id, chat_history)

#     return {
#         "answer": response,
#         "sources": [m['metadata']['source'] for m in query_results['matches']],
#         "chat_id": chat_id
#     }

# @app.get("/chat-history")
# async def get_chat_history():
#     chats = []
#     for fname in os.listdir(CHAT_HISTORY_DIR):
#         if fname.endswith(".json"):
#             with open(os.path.join(CHAT_HISTORY_DIR, fname)) as f:
#                 data = json.load(f)
#                 chats.append({"chat_id": data['chat_id'], "title": data['title'], "timestamp": data['timestamp']})
#     chats.sort(key=lambda x: x['timestamp'], reverse=True)
#     return chats

# @app.get("/chat-history/{chat_id}")
# async def get_specific_chat_history(chat_id: str):
#     messages = load_chat_history(chat_id)
#     if messages:
#         return {"messages": messages}
#     raise HTTPException(404, "Chat history not found")

# @app.delete("/chat-history/{chat_id}")
# async def delete_chat_history(chat_id: str):
#     path = os.path.join(CHAT_HISTORY_DIR, f"{chat_id}.json")
#     if os.path.exists(path):
#         os.remove(path)
#         return {"message": f"Chat history {chat_id} deleted successfully"}
#     raise HTTPException(404, "Chat history not found")





# # import os
# # import json
# # from fastapi import FastAPI, File, UploadFile, HTTPException
# # from fastapi.middleware.cors import CORSMiddleware
# # from pydantic import BaseModel
# # from typing import List, Dict, Any
# # from datetime import datetime

# # from document_processor import DocumentProcessor
# # from pinecone_vectorstore import PineconeVectorStore
# # from groq import Groq

# # app = FastAPI()

# # # CORS Middleware
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # # Initialize Pinecone Vector Store
# # vector_store = PineconeVectorStore(
# #     api_key=os.getenv('PINECONE_API_KEY'), 
# #     index_name=os.getenv('INDEX_NAME')
# # )

# # # Initialize Groq Client for Llama3
# # groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# # # Create temp directory for file storage if it doesn't exist
# # CHAT_HISTORY_DIR = "temp/chat_history"
# # os.makedirs(CHAT_HISTORY_DIR, exist_ok=True)

# # class QueryRequest(BaseModel):
# #     query: str
# #     chat_history: List[dict] = []
# #     chat_id: str = None

# # class DocumentUpload(BaseModel):
# #     file_name: str

# # class ChatInfo(BaseModel):
# #     chat_id: str
# #     title: str
# #     timestamp: str
    
# # def save_chat_history(chat_id: str, messages: List[Dict[str, Any]]) -> None:
# #     """Save chat history to a JSON file."""
# #     # Extract the first user message to use as title (limited to 30 chars)
# #     title = "New Chat"
# #     for message in messages:
# #         if message["role"] == "user":
# #             title = message["content"][:30] + ("..." if len(message["content"]) > 30 else "")
# #             break
            
# #     chat_data = {
# #         "chat_id": chat_id,
# #         "title": title,
# #         "timestamp": datetime.now().isoformat(),
# #         "messages": messages
# #     }
    
# #     file_path = os.path.join(CHAT_HISTORY_DIR, f"{chat_id}.json")
# #     with open(file_path, "w") as f:
# #         json.dump(chat_data, f, indent=2)

# # def load_chat_history(chat_id: str) -> List[Dict[str, Any]]:
# #     """Load chat history from a JSON file."""
# #     file_path = os.path.join(CHAT_HISTORY_DIR, f"{chat_id}.json")
# #     if os.path.exists(file_path):
# #         with open(file_path, "r") as f:
# #             chat_data = json.load(f)
# #             return chat_data.get("messages", [])
# #     return []

# # def get_all_chat_histories() -> List[Dict[str, Any]]:
# #     """Get a list of all available chat histories."""
# #     chat_histories = []
# #     for filename in os.listdir(CHAT_HISTORY_DIR):
# #         if filename.endswith(".json"):
# #             file_path = os.path.join(CHAT_HISTORY_DIR, filename)
# #             with open(file_path, "r") as f:
# #                 chat_data = json.load(f)
# #                 chat_histories.append({
# #                     "chat_id": chat_data.get("chat_id"),
# #                     "title": chat_data.get("title", "Untitled Chat"),
# #                     "timestamp": chat_data.get("timestamp")
# #                 })
# #     # Sort by timestamp, newest first
# #     chat_histories.sort(key=lambda x: x["timestamp"], reverse=True)
# #     return chat_histories

# # @app.post("/upload")
# # async def upload_document(file: UploadFile = File(...)):
# #     # Temporary file storage
# #     file_location = f"temp/{file.filename}"
# #     os.makedirs("temp", exist_ok=True)
    
# #     with open(file_location, "wb+") as file_object:
# #         file_object.write(await file.read())
    
# #     # Process document based on file extension
# #     if file.filename.endswith('.pdf'):
# #         chunks = DocumentProcessor.read_pdf(file_location)
# #     elif file.filename.endswith('.pptx'):
# #         chunks = DocumentProcessor.read_pptx(file_location)
# #     elif file.filename.endswith(('.xlsx', '.xls')):
# #         chunks = DocumentProcessor.read_excel(file_location)
# #     else:
# #         os.remove(file_location)
# #         raise HTTPException(status_code=400, detail="Unsupported file type")
    
# #     # Upsert document chunks to Pinecone
# #     vector_store.upsert_documents(chunks)
    
# #     os.remove(file_location)
# #     return {
# #         "message": "Document processed successfully", 
# #         "chunk_count": len(chunks)  # Return the number of chunks created
# #     }

# # @app.post("/query")
# # async def query_documents(request: QueryRequest):
# #     query = request.query
# #     chat_id = request.chat_id
    
# #     # If no chat_id is provided, generate a new one
# #     if not chat_id:
# #         chat_id = f"chat_{datetime.now().strftime('%Y%m%d%H%M%S')}_{os.urandom(4).hex()}"
    
# #     # Load existing chat history
# #     chat_history = load_chat_history(chat_id)
    
# #     # Retrieve relevant documents for the question
# #     query_results = vector_store.query(query)
    
# #     # If no relevant documents found, explicitly state that no information is available
# #     if not query_results['matches']:
# #         response = "I apologize, but I cannot find any relevant information from the documents to answer this question. Please ensure you have uploaded the appropriate documents or rephrase your query."
        
# #         # Add to chat history
# #         chat_history.append({"role": "user", "content": query})
# #         chat_history.append({"role": "assistant", "content": response})
        
# #         # Save chat history
# #         save_chat_history(chat_id, chat_history)
        
# #         return {
# #             "answer": response,
# #             "sources": [],
# #             "chat_id": chat_id
# #         }
    
# #     # Construct context from retrieved documents
# #     document_context = "\n\n".join([
# #         result['metadata']['text'] 
# #         for result in query_results['matches']
# #     ])
    
# #     # Enhanced system prompt with calculation capabilities
# #     system_prompt = """
# #     You are a document assistant that answers questions based ONLY on the provided context.
# # IMPORTANT INSTRUCTIONS:
# # 1. Only use information that is explicitly present in the context provided below.
# # 2. Pay special attention to the document type (PDF, EXCEL, PPT, etc.) and respond with content from the specific document type the user is asking about.
# # 3. If the user explicitly mentions or asks about PowerPoint, Excel, or PDF, prioritize information from that document type.
# # 4. If information from multiple document types is available and relevant, explicitly mention which information comes from which document type.
# # 5. If the answer isn't in the provided context, say "I don't have information about this in the uploaded documents." Don't make up answers.
# # 6. Provide document names, types, and page numbers as sources for your information ONLY when answering substantive queries about document content. DO NOT provide source citations when:
# #    - Responding to greetings (hello, hi, good morning, etc.)
# #    - Engaging in simple conversation that doesn't require document information
# #    - Answering follow-up questions that don't request new document information
# #    - Responding to questions about yourself or your capabilities
# #    - Acknowledging user messages that don't require document references
# # 7. If the user mentions "slides" or "presentation," look specifically for PPT/PPTX content in the context.
# # 8. If the user mentions "spreadsheet," "cells," or similar, look specifically for Excel/XLS/XLSX content.
# # 9. Maintain accuracy - don't confuse information between different documents.
# #     """
    
# #     # Generate response using Llama3 with enhanced prompt
# #     chat_completion = groq_client.chat.completions.create(
# #         messages=[
# #             {
# #                 "role": "system", 
# #                 "content": system_prompt
# #             },
# #             {
# #                 "role": "user", 
# #                 "content": f"Document Context:\n{document_context}\n\nUser Message: {query}\n\nImportant: Unless this is just a greeting, your response MUST be solely based on the provided context. If you cannot confidently answer from this context, state that you cannot answer."
# #             }
# #         ],
# #         model="llama-3.3-70b-versatile",
# #         temperature=0  # Lowest temperature for most precise responses
# #     )
    
# #     # Get the response
# #     response = chat_completion.choices[0].message.content
    
# #     # Add to chat history
# #     chat_history.append({"role": "user", "content": query})
# #     chat_history.append({"role": "assistant", "content": response})
    
# #     # Save chat history
# #     save_chat_history(chat_id, chat_history)
    
# #     return {
# #         "answer": response,
# #         "sources": [
# #             result['metadata']['source'] 
# #             for result in query_results['matches']
# #         ],
# #         "chat_id": chat_id
# #     }

# # @app.get("/chat-history")
# # async def get_chat_history():
# #     # Return list of chat IDs with timestamps and titles
# #     return get_all_chat_histories()

# # @app.get("/chat-history/{chat_id}")
# # async def get_specific_chat_history(chat_id: str):
# #     # Retrieve chat history for specific chat_id
# #     chat_history = load_chat_history(chat_id)
# #     if chat_history:
# #         return {"messages": chat_history}
# #     else:
# #         raise HTTPException(status_code=404, detail="Chat history not found")

# # @app.delete("/chat-history/{chat_id}")
# # async def delete_chat_history(chat_id: str):
# #     # Delete a specific chat history
# #     file_path = os.path.join(CHAT_HISTORY_DIR, f"{chat_id}.json")
# #     if os.path.exists(file_path):
# #         os.remove(file_path)
# #         return {"message": f"Chat history {chat_id} deleted successfully"}
# #     else:
# #         raise HTTPException(status_code=404, detail="Chat history not found")

# # if __name__ == "__main__":
# #     import uvicorn
# #     uvicorn.run(app, host="0.0.0.0", port=8000)






# # ADDING PREVIOUSE QUESTION FUNCTIONALITY

# # import os
# # import json
# # from fastapi import FastAPI, File, UploadFile, HTTPException
# # from fastapi.middleware.cors import CORSMiddleware
# # from pydantic import BaseModel
# # from typing import List, Dict, Any
# # from datetime import datetime

# # from document_processor import DocumentProcessor
# # from pinecone_vectorstore import PineconeVectorStore
# # from groq import Groq

# # app = FastAPI()

# # # CORS Middleware
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # # Initialize Pinecone Vector Store
# # vector_store = PineconeVectorStore(
# #     api_key=os.getenv('PINECONE_API_KEY'), 
# #     index_name=os.getenv('INDEX_NAME')
# # )

# # # Initialize Groq Client for Llama3
# # groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# # # Create temp directory for file storage if it doesn't exist
# # CHAT_HISTORY_DIR = "temp/chat_history"
# # os.makedirs(CHAT_HISTORY_DIR, exist_ok=True)

# # # Maximum number of message pairs to include in context
# # MAX_HISTORY_MESSAGES = 5  # Will include 5 Q&A pairs (10 messages total)

# # class QueryRequest(BaseModel):
# #     query: str
# #     chat_history: List[dict] = []
# #     chat_id: str = None

# # class DocumentUpload(BaseModel):
# #     file_name: str

# # class ChatInfo(BaseModel):
# #     chat_id: str
# #     title: str
# #     timestamp: str
    
# # def save_chat_history(chat_id: str, messages: List[Dict[str, Any]]) -> None:
# #     """Save chat history to a JSON file."""
# #     # Extract the first user message to use as title (limited to 30 chars)
# #     title = "New Chat"
# #     for message in messages:
# #         if message["role"] == "user":
# #             title = message["content"][:30] + ("..." if len(message["content"]) > 30 else "")
# #             break
            
# #     chat_data = {
# #         "chat_id": chat_id,
# #         "title": title,
# #         "timestamp": datetime.now().isoformat(),
# #         "messages": messages
# #     }
    
# #     file_path = os.path.join(CHAT_HISTORY_DIR, f"{chat_id}.json")
# #     with open(file_path, "w") as f:
# #         json.dump(chat_data, f, indent=2)

# # def load_chat_history(chat_id: str) -> List[Dict[str, Any]]:
# #     """Load chat history from a JSON file."""
# #     file_path = os.path.join(CHAT_HISTORY_DIR, f"{chat_id}.json")
# #     if os.path.exists(file_path):
# #         with open(file_path, "r") as f:
# #             chat_data = json.load(f)
# #             return chat_data.get("messages", [])
# #     return []

# # def get_all_chat_histories() -> List[Dict[str, Any]]:
# #     """Get a list of all available chat histories."""
# #     chat_histories = []
# #     for filename in os.listdir(CHAT_HISTORY_DIR):
# #         if filename.endswith(".json"):
# #             file_path = os.path.join(CHAT_HISTORY_DIR, filename)
# #             with open(file_path, "r") as f:
# #                 chat_data = json.load(f)
# #                 chat_histories.append({
# #                     "chat_id": chat_data.get("chat_id"),
# #                     "title": chat_data.get("title", "Untitled Chat"),
# #                     "timestamp": chat_data.get("timestamp")
# #                 })
# #     # Sort by timestamp, newest first
# #     chat_histories.sort(key=lambda x: x["timestamp"], reverse=True)
# #     return chat_histories

# # def format_chat_history_for_llm(chat_history: List[Dict[str, Any]]) -> str:
# #     """Format chat history into a string for the LLM context"""
# #     # Only take the most recent MAX_HISTORY_MESSAGES pairs (user + assistant)
# #     # We process in pairs to keep context coherent
# #     formatted_history = []
    
# #     # Only include actual message pairs (user + assistant)
# #     messages = []
# #     for i in range(0, len(chat_history) - 1, 2):
# #         if i+1 < len(chat_history):
# #             if chat_history[i]["role"] == "user" and chat_history[i+1]["role"] == "assistant":
# #                 messages.append((chat_history[i], chat_history[i+1]))
    
# #     # Take only the most recent MAX_HISTORY_MESSAGES
# #     recent_messages = messages[-MAX_HISTORY_MESSAGES:]
    
# #     # Format messages
# #     for user_msg, assistant_msg in recent_messages:
# #         formatted_history.append(f"User: {user_msg['content']}")
# #         formatted_history.append(f"Assistant: {assistant_msg['content']}")
    
# #     return "\n\n".join(formatted_history)

# # @app.post("/upload")
# # async def upload_document(file: UploadFile = File(...)):
# #     # Temporary file storage
# #     file_location = f"temp/{file.filename}"
# #     os.makedirs("temp", exist_ok=True)
    
# #     with open(file_location, "wb+") as file_object:
# #         file_object.write(await file.read())
    
# #     # Process document based on file extension
# #     if file.filename.endswith('.pdf'):
# #         chunks = DocumentProcessor.read_pdf(file_location)
# #     elif file.filename.endswith('.pptx'):
# #         chunks = DocumentProcessor.read_pptx(file_location)
# #     elif file.filename.endswith(('.xlsx', '.xls')):
# #         chunks = DocumentProcessor.read_excel(file_location)
# #     else:
# #         os.remove(file_location)
# #         raise HTTPException(status_code=400, detail="Unsupported file type")
    
# #     # Upsert document chunks to Pinecone
# #     vector_store.upsert_documents(chunks)
    
# #     os.remove(file_location)
# #     return {
# #         "message": "Document processed successfully", 
# #         "chunk_count": len(chunks)  # Return the number of chunks created
# #     }

# # @app.post("/query")
# # async def query_documents(request: QueryRequest):
# #     query = request.query
# #     chat_id = request.chat_id
    
# #     # If no chat_id is provided, generate a new one
# #     if not chat_id:
# #         chat_id = f"chat_{datetime.now().strftime('%Y%m%d%H%M%S')}_{os.urandom(4).hex()}"
    
# #     # Load existing chat history
# #     chat_history = load_chat_history(chat_id)
    
# #     # Retrieve relevant documents for the question
# #     query_results = vector_store.query(query)
    
# #     # If no relevant documents found, explicitly state that no information is available
# #     if not query_results['matches']:
# #         response = "I apologize, but I cannot find any relevant information from the documents to answer this question. Please ensure you have uploaded the appropriate documents or rephrase your query."
        
# #         # Add to chat history
# #         chat_history.append({"role": "user", "content": query})
# #         chat_history.append({"role": "assistant", "content": response})
        
# #         # Save chat history
# #         save_chat_history(chat_id, chat_history)
        
# #         return {
# #             "answer": response,
# #             "sources": [],
# #             "chat_id": chat_id
# #         }
    
# #     # Construct context from retrieved documents
# #     document_context = "\n\n".join([
# #         result['metadata']['text'] 
# #         for result in query_results['matches']
# #     ])
    
# #     # Format previous chat history for context
# #     previous_conversation = format_chat_history_for_llm(chat_history)
    
# #     # Enhanced system prompt with calculation capabilities and conversation memory
# #     system_prompt = """
# #     You are a strictly context-bound document assistant with calculation capabilities and conversation memory. You have these functions:

# #     1. If a user sends a simple greeting (like "hello", "hi", "hey", etc.) without a specific question, 
# #        respond with a friendly greeting and introduce yourself as a document assistant.

# #     2. If the user asks about documents, ONLY answer based on the provided document context.
# #        If the context does not contain sufficient information to answer the question, respond that
# #        you cannot answer based on the given documents.

# #     3. If the user asks for calculations or data analysis on numerical data in the documents, you can:
# #        - Calculate sums, averages, max/min values from tabular data mentioned in the context
# #        - Filter calculations by categories if specified (e.g., "total profit for New York" or "average sales in France")
# #        - Extract numerical trends or patterns if present in the data
# #        - Format numbers appropriately with commas and decimal places
# #        - Provide location information when identifying maximum or minimum values
       
# #     4. When the user refers to previous questions or uses pronouns like "it", "that", etc., use the conversation
# #        history to understand the context and provide an appropriate response.
       
# #     Always maintain a professional, helpful tone and DO NOT generate information not present in the provided context.
# #     """
    
# #     # Generate response using Llama3 with enhanced prompt and conversation history
# #     user_prompt = f"Document Context:\n{document_context}\n\n"
    
# #     # Add previous conversation if it exists
# #     if previous_conversation:
# #         user_prompt += f"Previous Conversation:\n{previous_conversation}\n\n"
    
# #     user_prompt += f"User Message: {query}\n\n"
# #     user_prompt += "Important: Unless this is just a greeting, your response MUST be solely based on the provided context. If you cannot confidently answer from this context, state that you cannot answer."
    
# #     chat_completion = groq_client.chat.completions.create(
# #         messages=[
# #             {
# #                 "role": "system", 
# #                 "content": system_prompt
# #             },
# #             {
# #                 "role": "user", 
# #                 "content": user_prompt
# #             }
# #         ],
# #         model="llama-3.3-70b-versatile",
# #         temperature=0  # Lowest temperature for most precise responses
# #     )
    
# #     # Get the response
# #     response = chat_completion.choices[0].message.content
    
# #     # Add to chat history
# #     chat_history.append({"role": "user", "content": query})
# #     chat_history.append({"role": "assistant", "content": response})
    
# #     # Save chat history
# #     save_chat_history(chat_id, chat_history)
    
# #     return {
# #         "answer": response,
# #         "sources": [
# #             result['metadata']['source'] 
# #             for result in query_results['matches']
# #         ],
# #         "chat_id": chat_id
# #     }

# # @app.get("/chat-history")
# # async def get_chat_history():
# #     # Return list of chat IDs with timestamps and titles
# #     return get_all_chat_histories()

# # @app.get("/chat-history/{chat_id}")
# # async def get_specific_chat_history(chat_id: str):
# #     # Retrieve chat history for specific chat_id
# #     chat_history = load_chat_history(chat_id)
# #     if chat_history:
# #         return {"messages": chat_history}
# #     else:
# #         raise HTTPException(status_code=404, detail="Chat history not found")

# # @app.delete("/chat-history/{chat_id}")
# # async def delete_chat_history(chat_id: str):
# #     # Delete a specific chat history
# #     file_path = os.path.join(CHAT_HISTORY_DIR, f"{chat_id}.json")
# #     if os.path.exists(file_path):
# #         os.remove(file_path)
# #         return {"message": f"Chat history {chat_id} deleted successfully"}
# #     else:
# #         raise HTTPException(status_code=404, detail="Chat history not found")

# # if __name__ == "__main__":
# #     import uvicorn
# #     uvicorn.run(app, host="0.0.0.0", port=8000)



import os
import json
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime

from document_processor import DocumentProcessor
from pinecone_vectorstore import PineconeVectorStore
from groq import Groq

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Pinecone Vector Store
vector_store = PineconeVectorStore(
    api_key=os.getenv('PINECONE_API_KEY'), 
    index_name=os.getenv('INDEX_NAME')
)

# Initialize Groq Client for Llama3
groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# Create temp directory for file storage if it doesn't exist
CHAT_HISTORY_DIR = "temp/chat_history"
os.makedirs(CHAT_HISTORY_DIR, exist_ok=True)

# Maximum number of message pairs to include in context
MAX_HISTORY_MESSAGES = 5  # Will include 5 Q&A pairs (10 messages total)

class QueryRequest(BaseModel):
    query: str
    chat_history: List[dict] = []
    chat_id: str = None

class DocumentUpload(BaseModel):
    file_name: str

class ChatInfo(BaseModel):
    chat_id: str
    title: str
    timestamp: str
    
def save_chat_history(chat_id: str, messages: List[Dict[str, Any]]) -> None:
    """Save chat history to a JSON file."""
    # Extract the first user message to use as title (limited to 30 chars)
    title = "New Chat"
    for message in messages:
        if message["role"] == "user":
            title = message["content"][:30] + ("..." if len(message["content"]) > 30 else "")
            break
            
    chat_data = {
        "chat_id": chat_id,
        "title": title,
        "timestamp": datetime.now().isoformat(),
        "messages": messages
    }
    
    file_path = os.path.join(CHAT_HISTORY_DIR, f"{chat_id}.json")
    with open(file_path, "w") as f:
        json.dump(chat_data, f, indent=2)

def load_chat_history(chat_id: str) -> List[Dict[str, Any]]:
    """Load chat history from a JSON file."""
    file_path = os.path.join(CHAT_HISTORY_DIR, f"{chat_id}.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            chat_data = json.load(f)
            return chat_data.get("messages", [])
    return []

def get_all_chat_histories() -> List[Dict[str, Any]]:
    """Get a list of all available chat histories."""
    chat_histories = []
    for filename in os.listdir(CHAT_HISTORY_DIR):
        if filename.endswith(".json"):
            file_path = os.path.join(CHAT_HISTORY_DIR, filename)
            with open(file_path, "r") as f:
                chat_data = json.load(f)
                chat_histories.append({
                    "chat_id": chat_data.get("chat_id"),
                    "title": chat_data.get("title", "Untitled Chat"),
                    "timestamp": chat_data.get("timestamp")
                })
    # Sort by timestamp, newest first
    chat_histories.sort(key=lambda x: x["timestamp"], reverse=True)
    return chat_histories

def format_chat_history_for_llm(chat_history: List[Dict[str, Any]]) -> str:
    """Format chat history into a string for the LLM context"""
    # Only take the most recent MAX_HISTORY_MESSAGES pairs (user + assistant)
    # We process in pairs to keep context coherent
    formatted_history = []
    
    # Only include actual message pairs (user + assistant)
    messages = []
    for i in range(0, len(chat_history) - 1, 2):
        if i+1 < len(chat_history):
            if chat_history[i]["role"] == "user" and chat_history[i+1]["role"] == "assistant":
                messages.append((chat_history[i], chat_history[i+1]))
    
    # Take only the most recent MAX_HISTORY_MESSAGES
    recent_messages = messages[-MAX_HISTORY_MESSAGES:]
    
    # Format messages
    for user_msg, assistant_msg in recent_messages:
        formatted_history.append(f"User: {user_msg['content']}")
        formatted_history.append(f"Assistant: {assistant_msg['content']}")
    
    return "\n\n".join(formatted_history)

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    # Temporary file storage
    file_location = f"temp/{file.filename}"
    os.makedirs("temp", exist_ok=True)
    
    with open(file_location, "wb+") as file_object:
        file_object.write(await file.read())
    
    # Process document based on file extension
    if file.filename.endswith('.pdf'):
        chunks = DocumentProcessor.read_pdf(file_location)
    elif file.filename.endswith('.pptx'):
        chunks = DocumentProcessor.read_pptx(file_location)
    elif file.filename.endswith(('.xlsx', '.xls')):
        chunks = DocumentProcessor.read_excel(file_location)
    else:
        os.remove(file_location)
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    # Upsert document chunks to Pinecone
    vector_store.upsert_documents(chunks)
    
    os.remove(file_location)
    return {
        "message": "Document processed successfully", 
        "chunk_count": len(chunks)  # Return the number of chunks created
    }

@app.post("/query")
async def query_documents(request: QueryRequest):
    query = request.query
    chat_id = request.chat_id
    
    # If no chat_id is provided, generate a new one
    if not chat_id:
        chat_id = f"chat_{datetime.now().strftime('%Y%m%d%H%M%S')}_{os.urandom(4).hex()}"
    
    # Load existing chat history
    chat_history = load_chat_history(chat_id)
    
    # Retrieve relevant documents for the question
    query_results = vector_store.query(query)
    
    # If no relevant documents found, explicitly state that no information is available
    if not query_results['matches']:
        response = "I apologize, but I cannot find any relevant information from the documents to answer this question. Please ensure you have uploaded the appropriate documents or rephrase your query."
        
        # Add to chat history
        chat_history.append({"role": "user", "content": query})
        chat_history.append({"role": "assistant", "content": response})
        
        # Save chat history
        save_chat_history(chat_id, chat_history)
        
        return {
            "answer": response,
            "sources": [],
            "chat_id": chat_id
        }
    
    # Construct context from retrieved documents
    document_context = "\n\n".join([
        result['metadata']['text'] 
        for result in query_results['matches']
    ])
    
    # Format previous chat history for context
    previous_conversation = format_chat_history_for_llm(chat_history)
    
    # Enhanced system prompt with calculation capabilities and conversation memory
    system_prompt = """
    You are a strictly context-bound document assistant with calculation capabilities and conversation memory. You have these functions:

    1. If a user sends a simple greeting (like "hello", "hi", "hey", etc.) without a specific question, 
       respond with a friendly greeting and introduce yourself as a document assistant.

    2. If the user asks about documents, ONLY answer based on the provided document context.
       If the context does not contain sufficient information to answer the question, respond that
       you cannot answer based on the given documents.

    3. If the user asks for calculations or data analysis on numerical data in the documents, you can:
       - Calculate sums, averages, max/min values from tabular data mentioned in the context
       - Filter calculations by categories if specified (e.g., "total profit for New York" or "average sales in France")
       - Extract numerical trends or patterns if present in the data
       - Format numbers appropriately with commas and decimal places
       - Provide location information when identifying maximum or minimum values
       
    4. When the user refers to previous questions or uses pronouns like "it", "that", etc., use the conversation
       history to understand the context and provide an appropriate response.
       
    Always maintain a professional, helpful tone and DO NOT generate information not present in the provided context.
    """
    
    # Generate response using Llama3 with enhanced prompt and conversation history
    user_prompt = f"Document Context:\n{document_context}\n\n"
    
    # Add previous conversation if it exists
    if previous_conversation:
        user_prompt += f"Previous Conversation:\n{previous_conversation}\n\n"
    
    user_prompt += f"User Message: {query}\n\n"
    user_prompt += "Important: Unless this is just a greeting, your response MUST be solely based on the provided context. If you cannot confidently answer from this context, state that you cannot answer."
    
    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "system", 
                "content": system_prompt
            },
            {
                "role": "user", 
                "content": user_prompt
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=0  # Lowest temperature for most precise responses
    )
    
    # Get the response
    response = chat_completion.choices[0].message.content
    
    # Add to chat history
    chat_history.append({"role": "user", "content": query})
    chat_history.append({"role": "assistant", "content": response})
    
    # Save chat history
    save_chat_history(chat_id, chat_history)
    
    return {
        "answer": response,
        "sources": [
            result['metadata']['source'] 
            for result in query_results['matches']
        ],
        "chat_id": chat_id
    }

@app.get("/chat-history")
async def get_chat_history():
    # Return list of chat IDs with timestamps and titles
    return get_all_chat_histories()

@app.get("/chat-history/{chat_id}")
async def get_specific_chat_history(chat_id: str):
    # Retrieve chat history for specific chat_id
    chat_history = load_chat_history(chat_id)
    if chat_history:
        return {"messages": chat_history}
    else:
        raise HTTPException(status_code=404, detail="Chat history not found")

# NEW: List all chat sessions
@app.get("/chat-history")
async def get_chat_history():
    chats = []
    for fname in os.listdir(CHAT_HISTORY_DIR):
        if fname.endswith(".json"):
            with open(os.path.join(CHAT_HISTORY_DIR, fname), "r") as f:
                chat_data = json.load(f)
                chats.append({
                    "chat_id": chat_data.get("chat_id"),
                    "title": chat_data.get("title", "Untitled Chat"),
                    "timestamp": chat_data.get("timestamp")
                })
    # Sort by timestamp, newest first
    chats.sort(key=lambda x: x["timestamp"], reverse=True)
    return chats


@app.delete("/chat-history/{chat_id}")
async def delete_chat_history(chat_id: str):
    # Delete a specific chat history
    file_path = os.path.join(CHAT_HISTORY_DIR, f"{chat_id}.json")
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"message": f"Chat history {chat_id} deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Chat history not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)