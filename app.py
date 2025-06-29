# # import os
# # import uuid
# # import streamlit as st
# # import requests
# # import pandas as pd
# # from typing import List
# # from datetime import datetime

# # # Configure page
# # st.set_page_config(
# #     page_title="Document Q&A RAG", 
# #     page_icon="📄", 
# #     layout="wide"
# # )

# # # Backend API URL
# # BACKEND_URL = "http://localhost:8000"

# # def upload_document(uploaded_file):
# #     files = {'file': (uploaded_file.name, uploaded_file)}
# #     response = requests.post(f"{BACKEND_URL}/upload", files=files)
    
# #     # If it's an Excel file, also save a copy locally for reference purposes
# #     if uploaded_file.name.endswith(('.xlsx', '.xls')):
# #         # Reset uploaded file pointer to beginning
# #         uploaded_file.seek(0)
# #         # Ensure the tmp directory exists
# #         os.makedirs("tmp", exist_ok=True)
# #         # Save the file locally
# #         file_path = os.path.join("tmp", uploaded_file.name)
# #         with open(file_path, "wb") as f:
# #             f.write(uploaded_file.getbuffer())
    
# #     return response.json()

# # def query_documents(query: str, chat_history: List[dict], chat_id: str = None):
# #     # Regular query
# #     payload = {
# #         "query": query,
# #         "chat_history": chat_history,
# #         "chat_id": chat_id
# #     }
# #     response = requests.post(f"{BACKEND_URL}/query", json=payload)
# #     return response.json()

# # def save_chat_session(chat_history, chat_id):
# #     """Save current chat session to the session state"""
# #     # Check if the chat session already exists
# #     existing_session_index = None
# #     for idx, session in enumerate(st.session_state.chat_sessions):
# #         if session['id'] == chat_id:
# #             existing_session_index = idx
# #             break
    
# #     # Update existing session or create new one
# #     session_data = {
# #         'id': chat_id,
# #         'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
# #         'messages': chat_history.copy(),
# #         'total_messages': len(chat_history),
# #         'last_message': chat_history[-1]['content'] if chat_history else '',
# #         'title': f"Chat {datetime.now().strftime('%m/%d %H:%M')}"
# #     }
    
# #     if existing_session_index is not None:
# #         st.session_state.chat_sessions[existing_session_index] = session_data
# #     else:
# #         st.session_state.chat_sessions.append(session_data)

# # def get_chat_sessions_from_backend():
# #     """Get all chat sessions from the backend API"""
# #     try:
# #         response = requests.get(f"{BACKEND_URL}/chat-history")
# #         return response.json()
# #     except Exception as e:
# #         st.error(f"Error fetching chat history: {str(e)}")
# #         return []

# # def get_specific_chat_history(chat_id):
# #     """Get full chat history for a specific chat ID"""
# #     try:
# #         response = requests.get(f"{BACKEND_URL}/chat-history/{chat_id}")
# #         return response.json().get('messages', [])
# #     except Exception as e:
# #         st.error(f"Error fetching specific chat history: {str(e)}")
# #         return []

# # def delete_chat_history(chat_id):
# #     """Delete chat history for a specific chat ID"""
# #     try:
# #         response = requests.delete(f"{BACKEND_URL}/chat-history/{chat_id}")
# #         return response.json()
# #     except Exception as e:
# #         st.error(f"Error deleting chat history: {str(e)}")
# #         return {"message": f"Failed to delete chat history: {str(e)}"}

# # # Custom CSS for enhanced styling
# # st.markdown("""
# # <style>
# #     .main-container {
# #         max-width: 1200px;
# #         margin: 0 auto;
# #         padding: 20px;
# #     }
# #     .sidebar-content {
# #         background-color: #f0f2f6;
# #         border-radius: 10px;
# #         padding: 15px;
# #         margin-bottom: 15px;
# #     }
# #     .chat-message {
# #         margin-bottom: 15px;
# #         padding: 10px;
# #         border-radius: 10px;
# #     }
# #     .user-message {
# #         background-color: #e6f2ff;
# #     }
# #     .assistant-message {
# #         background-color: #f0f0f0;
# #     }
# #     .sources-expander {
# #         background-color: #f9f9f9;
# #         border-radius: 8px;
# #     }
# #     .chat-title {
# #         font-weight: bold;
# #         margin-bottom: 5px;
# #     }
# #     .chat-preview {
# #         color: #666;
# #         font-size: 0.9em;
# #         white-space: nowrap;
# #         overflow: hidden;
# #         text-overflow: ellipsis;
# #         max-width: 200px;
# #     }
# #     .chat-item {
# #         display: flex;
# #         align-items: center;
# #         margin-bottom: 10px;
# #         padding: 8px;
# #         border-radius: 5px;
# #         cursor: pointer;
# #     }
# #     .chat-item:hover {
# #         background-color: #e6e6e6;
# #     }
# #     .chat-item.active {
# #         background-color: #d1e7ff;
# #     }
# # </style>
# # """, unsafe_allow_html=True)

# # # Initialize session state variables
# # if 'chat_sessions' not in st.session_state:
# #     st.session_state.chat_sessions = []

# # if 'chat_history' not in st.session_state:
# #     st.session_state.chat_history = []

# # if 'uploaded_documents' not in st.session_state:
# #     st.session_state.uploaded_documents = []

# # if 'open_chat_index' not in st.session_state:
# #     st.session_state.open_chat_index = None

# # # Previous question tracking
# # if 'previous_user_question' not in st.session_state:
# #     st.session_state.previous_user_question = None

# # if 'last_user_question' not in st.session_state:
# #     st.session_state.last_user_question = None

# # # Generate unique chat ID
# # if 'current_chat_id' not in st.session_state:
# #     st.session_state.current_chat_id = str(uuid.uuid4())

# # # Sync with backend chat history
# # if st.session_state.chat_sessions == []:
# #     backend_chats = get_chat_sessions_from_backend()
# #     if backend_chats:
# #         for chat in backend_chats:
# #             st.session_state.chat_sessions.append({
# #                 'id': chat.get('chat_id'),
# #                 'timestamp': datetime.fromisoformat(chat.get('timestamp')).strftime("%Y-%m-%d %H:%M:%S"),
# #                 'messages': get_specific_chat_history(chat.get('chat_id')),
# #                 'total_messages': len(get_specific_chat_history(chat.get('chat_id'))),
# #                 'last_message': get_specific_chat_history(chat.get('chat_id'))[-1]['content'] if get_specific_chat_history(chat.get('chat_id')) else '',
# #                 'title': chat.get('title', f"Chat {datetime.fromisoformat(chat.get('timestamp')).strftime('%m/%d %H:%M')}")
# #             })

# # # Main layout
# # st.markdown('<div class="main-container">', unsafe_allow_html=True)
# # st.title("📄 Document Q&A with RAG")

# # # Sidebar Layout
# # with st.sidebar:
# #     st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
# #     st.header("📋 Document Management")
    
# #     # Document Upload Section
# #     st.subheader("Upload Documents")
# #     uploaded_files = st.file_uploader(
# #         "Choose PDF, PPTX, or Excel files", 
# #         type=['pdf', 'pptx', 'xlsx', 'xls'], 
# #         accept_multiple_files=True,
# #         help="Upload documents to query against"
# #     )

# #     if uploaded_files:
# #         with st.spinner("Processing documents..."):
# #             for uploaded_file in uploaded_files:
# #                 result = upload_document(uploaded_file)
                
# #                 # Display chunk count
# #                 chunk_count = result.get('chunk_count', 0)
# #                 st.success(f"{uploaded_file.name} processed successfully!")
# #                 st.info(f"📊 Document chunked into {chunk_count} semantic chunks")
                
# #                 # Track uploaded documents uniquely
# #                 if uploaded_file.name not in st.session_state.uploaded_documents:
# #                     st.session_state.uploaded_documents.append(uploaded_file.name)

# #     # Current Documents Display
# #     if st.session_state.uploaded_documents:
# #         st.subheader("Current Documents")
# #         for doc in st.session_state.uploaded_documents:
# #             col1, col2 = st.columns([3,1])
# #             with col1:
# #                 st.write(f"📄 {doc}")
# #             with col2:
# #                 if st.button("❌", key=f"remove_{doc}"):
# #                     st.session_state.uploaded_documents.remove(doc)
# #                     # Also remove from tmp directory if it's an Excel file
# #                     if doc.endswith(('.xlsx', '.xls')):
# #                         file_path = os.path.join("tmp", doc)
# #                         if os.path.exists(file_path):
# #                             os.remove(file_path)

# #     st.markdown('</div>', unsafe_allow_html=True)
    
# #     # Enhanced Chat History Section
# #     st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
# #     st.header("🕒 Chat History")
    
# #     # New Chat Button with improved styling
# #     if st.button("🆕 Start New Chat", use_container_width=True, key="new_chat_button"):
# #         # Check if the current chat has messages
# #         if st.session_state.chat_history:
# #             # Save current chat to chat sessions
# #             save_chat_session(st.session_state.chat_history, st.session_state.current_chat_id)
        
# #         # Reset chat history and related variables
# #         st.session_state.chat_history = []
# #         st.session_state.last_user_question = None
# #         st.session_state.previous_user_question = None
# #         st.session_state.open_chat_index = None
        
# #         # Generate new unique chat ID
# #         st.session_state.current_chat_id = str(uuid.uuid4())
    
# #     # Display Chat Sessions with improved UI
# #     st.subheader("Your Conversations")
    
# #     if not st.session_state.chat_sessions:
# #         st.info("No saved conversations yet. Start a new chat!")
    
# #     # Sort chat sessions by timestamp (newest first)
# #     sorted_sessions = sorted(
# #         st.session_state.chat_sessions, 
# #         key=lambda x: datetime.strptime(x['timestamp'], "%Y-%m-%d %H:%M:%S"),
# #         reverse=True
# #     )
    
# #     for idx, chat_session in enumerate(sorted_sessions):
# #         # Determine if this is the active chat
# #         is_active = (st.session_state.current_chat_id == chat_session['id'] or 
# #                     (st.session_state.open_chat_index is not None and 
# #                     idx == st.session_state.open_chat_index))
        
# #         # Create an interactive chat item
# #         chat_class = "chat-item active" if is_active else "chat-item"
        
# #         st.markdown(f'<div class="{chat_class}" id="chat_{idx}">', unsafe_allow_html=True)
        
# #         col1, col2 = st.columns([4,1])
        
# #         # Get a preview of the last message (first 50 chars)
# #         last_msg = chat_session.get('last_message', '')
# #         preview = last_msg[:50] + '...' if len(last_msg) > 50 else last_msg
        
# #         with col1:
# #             # Chat title and preview with clickable behavior
# #             if st.button(
# #                 f"📝 {chat_session.get('title', f'Chat {idx+1}')}",
# #                 key=f"open_chat_{idx}",
# #                 help="Click to open this conversation"
# #             ):
# #                 # Load this chat history
# #                 st.session_state.open_chat_index = idx
# #                 st.session_state.chat_history = chat_session['messages']
# #                 st.session_state.current_chat_id = chat_session['id']
# #                 st.session_state.last_user_question = None
# #                 st.session_state.previous_user_question = None
            
# #             # Show message preview
# #             st.markdown(f'<div class="chat-preview">{preview}</div>', unsafe_allow_html=True)
            
# #             # Show timestamp and message count
# #             st.caption(f"{chat_session['timestamp']} | {chat_session['total_messages']} messages")
        
# #         with col2:
# #             # Delete button
# #             if st.button("❌", key=f"delete_chat_{idx}", help="Delete this conversation"):
# #                 # Delete from backend first
# #                 if delete_chat_history(chat_session['id']).get('message'):
# #                     st.session_state.chat_sessions.pop(idx)
# #                     # If we deleted the active chat, reset current chat
# #                     if is_active:
# #                         st.session_state.chat_history = []
# #                         st.session_state.current_chat_id = str(uuid.uuid4())
# #                         st.session_state.open_chat_index = None
        
# #         st.markdown('</div>', unsafe_allow_html=True)
    
# #     st.markdown('</div>', unsafe_allow_html=True)

# # # Chat Interface - Always Visible
# # st.header("Ask Questions about Your Documents")

# # # Display chat history with sources
# # for message in st.session_state.chat_history:
# #     with st.chat_message(message['role']):
# #         st.markdown(message['content'])
        
# #         # Show sources if available (for assistant messages)
# #         if message['role'] == 'assistant' and message.get('sources'):
# #             with st.expander("Sources"):
# #                 for source in message['sources']:
# #                     st.write(source)

# # # User input
# # if prompt := st.chat_input("Ask a question about your documents"):
# #     # Store the current question as previous question before updating
# #     st.session_state.previous_user_question = st.session_state.get('last_user_question', None)
# #     st.session_state.last_user_question = prompt

# #     # Process the query
# #     try:
# #         # User message
# #         st.chat_message("user").markdown(prompt)
# #         st.session_state.chat_history.append({"role": "user", "content": prompt})

# #         # Get response from backend
# #         with st.spinner("Generating response..."):
# #             response = query_documents(
# #                 prompt, 
# #                 st.session_state.chat_history,
# #                 st.session_state.current_chat_id
# #             )
        
# #         # Display AI response
# #         with st.chat_message("assistant"):
# #             st.markdown(response['answer'])
            
# #             # Show sources if available
# #             if response.get('sources'):
# #                 with st.expander("Sources"):
# #                     for source in response['sources']:
# #                         st.write(source)
        
# #         # Update chat history
# #         st.session_state.chat_history.append({
# #             "role": "assistant", 
# #             "content": response['answer'],
# #             "sources": response.get('sources', [])
# #         })
        
# #         # Save updated chat session
# #         save_chat_session(st.session_state.chat_history, st.session_state.current_chat_id)
        
# #     except Exception as e:
# #         st.error(f"An error occurred: {str(e)}")

# # st.markdown('</div>', unsafe_allow_html=True)



# ### app.py (Frontend with memory + conditional source display) ###
# import os
# import uuid
# import streamlit as st
# import requests
# import pandas as pd
# from typing import List
# from datetime import datetime

# st.set_page_config(page_title="Document Q&A RAG", page_icon="📄", layout="wide")
# BACKEND_URL = "http://localhost:8000"

# def upload_document(uploaded_file):
#     files = {'file': (uploaded_file.name, uploaded_file)}
#     response = requests.post(f"{BACKEND_URL}/upload", files=files)
#     if uploaded_file.name.endswith(('.xlsx', '.xls')):
#         uploaded_file.seek(0)
#         os.makedirs("tmp", exist_ok=True)
#         file_path = os.path.join("tmp", uploaded_file.name)
#         with open(file_path, "wb") as f:
#             f.write(uploaded_file.getbuffer())
#     return response.json()

# def query_documents(query: str, chat_history: List[dict], chat_id: str = None):
#     payload = {"query": query, "chat_history": chat_history, "chat_id": chat_id}
#     response = requests.post(f"{BACKEND_URL}/query", json=payload)
#     return response.json()

# def save_chat_session(chat_history, chat_id):
#     existing_session_index = None
#     for idx, session in enumerate(st.session_state.chat_sessions):
#         if session['id'] == chat_id:
#             existing_session_index = idx
#             break

#     session_data = {
#         'id': chat_id,
#         'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         'messages': chat_history.copy(),
#         'total_messages': len(chat_history),
#         'last_message': chat_history[-1]['content'] if chat_history else '',
#         'title': f"Chat {datetime.now().strftime('%m/%d %H:%M')}"
#     }
#     if existing_session_index is not None:
#         st.session_state.chat_sessions[existing_session_index] = session_data
#     else:
#         st.session_state.chat_sessions.append(session_data)

# if 'chat_sessions' not in st.session_state:
#     st.session_state.chat_sessions = []
# if 'chat_history' not in st.session_state:
#     st.session_state.chat_history = []
# if 'uploaded_documents' not in st.session_state:
#     st.session_state.uploaded_documents = []
# if 'current_chat_id' not in st.session_state:
#     st.session_state.current_chat_id = str(uuid.uuid4())

# st.title("📄 Document Q&A with RAG")

# with st.sidebar:
#     st.header("📋 Upload Documents")
#     uploaded_files = st.file_uploader("Upload PDFs, PPTXs or Excels", type=['pdf', 'pptx', 'xlsx', 'xls'], accept_multiple_files=True)
#     if uploaded_files:
#         for uploaded_file in uploaded_files:
#             result = upload_document(uploaded_file)
#             st.success(f"{uploaded_file.name} processed! Chunks: {result.get('chunk_count')}")
#             if uploaded_file.name not in st.session_state.uploaded_documents:
#                 st.session_state.uploaded_documents.append(uploaded_file.name)

# st.header("Ask Questions about Your Documents")
# for message in st.session_state.chat_history:
#     with st.chat_message(message['role']):
#         st.markdown(message['content'])
#         if message['role'] == 'assistant' and message.get('sources'):
#             if any('page' in s.lower() or '.pdf' in s.lower() or '.pptx' in s.lower() or '.xlsx' in s.lower() for s in message['sources']):
#                 with st.expander("Sources"):
#                     for source in message['sources']:
#                         st.write(source)

# if prompt := st.chat_input("Ask a question about your documents"):
#     st.chat_message("user").markdown(prompt)
#     st.session_state.chat_history.append({"role": "user", "content": prompt})
#     with st.spinner("Generating response..."):
#         response = query_documents(prompt, st.session_state.chat_history, st.session_state.current_chat_id)
#     with st.chat_message("assistant"):
#         st.markdown(response['answer'])
#         if response.get('sources'):
#             if any('page' in s.lower() or '.pdf' in s.lower() or '.pptx' in s.lower() or '.xlsx' in s.lower() for s in response['sources']):
#                 with st.expander("Sources"):
#                     for source in response['sources']:
#                         st.write(source)
#     st.session_state.chat_history.append({"role": "assistant", "content": response['answer'], "sources": response.get('sources', [])})
#     save_chat_session(st.session_state.chat_history, st.session_state.current_chat_id)





import os
import uuid
import streamlit as st
import requests
import pandas as pd
import json  # Added import for json
from typing import List
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Document Q&A RAG", 
    page_icon="📄", 
    layout="wide"
)

# Backend API URL
BACKEND_URL = "http://localhost:8000"

def upload_document(uploaded_file):
    files = {'file': (uploaded_file.name, uploaded_file)}
    response = requests.post(f"{BACKEND_URL}/upload", files=files)
    
    # If it's an Excel file, also save a copy locally for reference purposes
    if uploaded_file.name.endswith(('.xlsx', '.xls')):
        # Reset uploaded file pointer to beginning
        uploaded_file.seek(0)
        # Ensure the tmp directory exists
        os.makedirs("tmp", exist_ok=True)
        # Save the file locally
        file_path = os.path.join("tmp", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    
    return response.json()

def query_documents(query: str, chat_history: List[dict], chat_id: str = None):
    # Regular query
    payload = {
        "query": query,
        "chat_history": chat_history,
        "chat_id": chat_id
    }
    response = requests.post(f"{BACKEND_URL}/query", json=payload)
    return response.json()

def save_chat_session(chat_history, chat_id):
    """Save current chat session to the session state"""
    # Check if the chat session already exists
    existing_session_index = None
    for idx, session in enumerate(st.session_state.chat_sessions):
        if session['id'] == chat_id:
            existing_session_index = idx
            break
    
    # Update existing session or create new one
    session_data = {
        'id': chat_id,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'messages': chat_history.copy(),
        'total_messages': len(chat_history),
        'last_message': chat_history[-1]['content'] if chat_history else '',
        'title': f"Chat {datetime.now().strftime('%m/%d %H:%M')}"
    }
    
    if existing_session_index is not None:
        st.session_state.chat_sessions[existing_session_index] = session_data
    else:
        st.session_state.chat_sessions.append(session_data)

def get_chat_sessions_from_backend():
    """Get all chat sessions from the backend API"""
    try:
        response = requests.get(f"{BACKEND_URL}/chat-history")
        return response.json()
    except Exception as e:
        st.error(f"Error fetching chat history: {str(e)}")
        return []

def get_specific_chat_history(chat_id):
    """Get full chat history for a specific chat ID"""
    try:
        response = requests.get(f"{BACKEND_URL}/chat-history/{chat_id}")
        return response.json().get('messages', [])
    except Exception as e:
        st.error(f"Error fetching specific chat history: {str(e)}")
        return []

def delete_chat_history(chat_id):
    """Delete chat history for a specific chat ID"""
    try:
        response = requests.delete(f"{BACKEND_URL}/chat-history/{chat_id}")
        return response.json()
    except Exception as e:
        st.error(f"Error deleting chat history: {str(e)}")
        return {"message": f"Failed to delete chat history: {str(e)}"}

# Custom CSS for enhanced styling
st.markdown("""
<style>
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }
    .sidebar-content {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
    }
    .chat-message {
        margin-bottom: 15px;
        padding: 10px;
        border-radius: 10px;
    }
    .user-message {
        background-color: #e6f2ff;
    }
    .assistant-message {
        background-color: #f0f0f0;
    }
    .sources-expander {
        background-color: #f9f9f9;
        border-radius: 8px;
    }
    .chat-title {
        font-weight: bold;
        margin-bottom: 5px;
    }
    .chat-preview {
        color: #666;
        font-size: 0.9em;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 200px;
    }
    .chat-item {
        display: flex;
        align-items: center;
        margin-bottom: 10px;
        padding: 8px;
        border-radius: 5px;
        cursor: pointer;
    }
    .chat-item:hover {
        background-color: #e6e6e6;
    }
    .chat-item.active {
        background-color: #d1e7ff;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'chat_sessions' not in st.session_state:
    st.session_state.chat_sessions = []

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'uploaded_documents' not in st.session_state:
    st.session_state.uploaded_documents = []

if 'open_chat_index' not in st.session_state:
    st.session_state.open_chat_index = None

# Previous question tracking
if 'previous_user_question' not in st.session_state:
    st.session_state.previous_user_question = None

if 'last_user_question' not in st.session_state:
    st.session_state.last_user_question = None

# Generate unique chat ID
if 'current_chat_id' not in st.session_state:
    st.session_state.current_chat_id = str(uuid.uuid4())

# Sync with backend chat history
if st.session_state.chat_sessions == []:
    backend_chats = get_chat_sessions_from_backend()
    if backend_chats:
        for chat in backend_chats:
            if isinstance(chat, str):
                try:
                    chat = json.loads(chat)
                except Exception as e:
                    print(f"Error parsing chat as JSON: {e}, value: {chat}")
                    continue  # skip this chat if it can't be parsed
            st.session_state.chat_sessions.append({
                'id': chat.get('chat_id'),
                'timestamp': datetime.fromisoformat(chat.get('timestamp')).strftime("%Y-%m-%d %H:%M:%S"),
                'messages': get_specific_chat_history(chat.get('chat_id')),
                'total_messages': len(get_specific_chat_history(chat.get('chat_id'))),
                'last_message': get_specific_chat_history(chat.get('chat_id'))[-1]['content'] if get_specific_chat_history(chat.get('chat_id')) else '',
                'title': chat.get('title', f"Chat {datetime.fromisoformat(chat.get('timestamp')).strftime('%m/%d %H:%M')}")
            })

# Main layout
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.title("📄 Document Q&A with RAG")

# Sidebar Layout
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.header("📋 Document Management")
    
    # Document Upload Section
    st.subheader("Upload Documents")
    uploaded_files = st.file_uploader(
        "Choose PDF, PPTX, or Excel files", 
        type=['pdf', 'pptx', 'xlsx', 'xls'], 
        accept_multiple_files=True,
        help="Upload documents to query against"
    )

    if uploaded_files:
        with st.spinner("Processing documents..."):
            for uploaded_file in uploaded_files:
                result = upload_document(uploaded_file)
                
                # Display chunk count
                chunk_count = result.get('chunk_count', 0)
                st.success(f"{uploaded_file.name} processed successfully!")
                st.info(f"📊 Document chunked into {chunk_count} semantic chunks")
                
                # Track uploaded documents uniquely
                if uploaded_file.name not in st.session_state.uploaded_documents:
                    st.session_state.uploaded_documents.append(uploaded_file.name)

    # Current Documents Display
    if st.session_state.uploaded_documents:
        st.subheader("Current Documents")
        for doc in st.session_state.uploaded_documents:
            col1, col2 = st.columns([3,1])
            with col1:
                st.write(f"📄 {doc}")
            with col2:
                if st.button("❌", key=f"remove_{doc}"):
                    st.session_state.uploaded_documents.remove(doc)
                    # Also remove from tmp directory if it's an Excel file
                    if doc.endswith(('.xlsx', '.xls')):
                        file_path = os.path.join("tmp", doc)
                        if os.path.exists(file_path):
                            os.remove(file_path)

    st.markdown('</div>', unsafe_allow_html=True)
    
    # Enhanced Chat History Section
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.header("🕒 Chat History")
    
    # New Chat Button with improved styling
    if st.button("🆕 Start New Chat", use_container_width=True, key="new_chat_button"):
        # Check if the current chat has messages
        if st.session_state.chat_history:
            # Save current chat to chat sessions
            save_chat_session(st.session_state.chat_history, st.session_state.current_chat_id)
        
        # Reset chat history and related variables
        st.session_state.chat_history = []
        st.session_state.last_user_question = None
        st.session_state.previous_user_question = None
        st.session_state.open_chat_index = None
        
        # Generate new unique chat ID
        st.session_state.current_chat_id = str(uuid.uuid4())
    
    # Display Chat Sessions with improved UI
    st.subheader("Your Conversations")
    
    if not st.session_state.chat_sessions:
        st.info("No saved conversations yet. Start a new chat!")
    
    # Sort chat sessions by timestamp (newest first)
    sorted_sessions = sorted(
        st.session_state.chat_sessions, 
        key=lambda x: datetime.strptime(x['timestamp'], "%Y-%m-%d %H:%M:%S"),
        reverse=True
    )
    
    for idx, chat_session in enumerate(sorted_sessions):
        # Determine if this is the active chat
        is_active = (st.session_state.current_chat_id == chat_session['id'] or 
                    (st.session_state.open_chat_index is not None and 
                    idx == st.session_state.open_chat_index))
        
        # Create an interactive chat item
        chat_class = "chat-item active" if is_active else "chat-item"
        
        st.markdown(f'<div class="{chat_class}" id="chat_{idx}">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([4,1])
        
        # Get a preview of the last message (first 50 chars)
        last_msg = chat_session.get('last_message', '')
        preview = last_msg[:50] + '...' if len(last_msg) > 50 else last_msg
        
        with col1:
            # Chat title and preview with clickable behavior
            if st.button(
                f"📝 {chat_session.get('title', f'Chat {idx+1}')}",
                key=f"open_chat_{idx}",
                help="Click to open this conversation"
            ):
                # Load this chat history
                st.session_state.open_chat_index = idx
                st.session_state.chat_history = chat_session['messages']
                st.session_state.current_chat_id = chat_session['id']
                st.session_state.last_user_question = None
                st.session_state.previous_user_question = None
            
            # Show message preview
            st.markdown(f'<div class="chat-preview">{preview}</div>', unsafe_allow_html=True)
            
            # Show timestamp and message count
            st.caption(f"{chat_session['timestamp']} | {chat_session['total_messages']} messages")
        
        with col2:
            # Delete button
            if st.button("❌", key=f"delete_chat_{idx}", help="Delete this conversation"):
                # Delete from backend first
                if delete_chat_history(chat_session['id']).get('message'):
                    st.session_state.chat_sessions.pop(idx)
                    # If we deleted the active chat, reset current chat
                    if is_active:
                        st.session_state.chat_history = []
                        st.session_state.current_chat_id = str(uuid.uuid4())
                        st.session_state.open_chat_index = None
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Chat Interface - Always Visible
st.header("Ask Questions about Your Documents")

# Display chat history with sources
for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
        st.markdown(message['content'])
        
        # Show sources if available (for assistant messages)
        if message['role'] == 'assistant' and message.get('sources'):
            with st.expander("Sources"):
                for source in message['sources']:
                    st.write(source)

# User input
if prompt := st.chat_input("Ask a question about your documents"):
    # Store the current question as previous question before updating
    st.session_state.previous_user_question = st.session_state.get('last_user_question', None)
    st.session_state.last_user_question = prompt

    # Process the query
    try:
        # User message
        st.chat_message("user").markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        # Get response from backend
        with st.spinner("Generating response..."):
            response = query_documents(
                prompt, 
                st.session_state.chat_history,
                st.session_state.current_chat_id
            )
            print("DEBUG: Backend response:", response)
        
        # Display AI response
        if isinstance(response, dict) and 'answer' in response:
            with st.chat_message("assistant"):
                st.markdown(response['answer'])
                
                # Show sources if available
                if response.get('sources'):
                    with st.expander("Sources"):
                        for source in response['sources']:
                            st.write(source)
            
            # Update chat history
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": response['answer'],
                "sources": response.get('sources', [])
            })
        else:
            st.error(f"Backend did not return an answer. Response: {response}")
        
        # Save updated chat session
        save_chat_session(st.session_state.chat_history, st.session_state.current_chat_id)
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)