from flask import Blueprint, render_template, request, jsonify
import json
import os
from PyPDF2 import PdfReader
from .utils import format_response
from .chat import ChatManager

# Create a Blueprint for the main application
main = Blueprint('main', __name__)

# Initialize the ChatManager
chat_manager = ChatManager()

# ==============================
# Storage Files
# ==============================

HISTORY_FILE = "chat_history.json"
DOCUMENT_FILE = "uploaded_document.txt"


# ==============================
# Chat History Storage
# ==============================

def save_message(user_msg, ai_msg):
    # Create history file if not exists
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

    # Read history
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        history = json.load(f)

    # Append new message
    history.append({
        "user": user_msg,
        "ai": ai_msg
    })

    # Save back to file
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


# ==============================
# Routes
# ==============================

@main.route('/')
def index():
    """Render the chat interface."""
    return render_template('chat.html')
from flask import render_template, redirect, url_for

@main.route("/login")
def login():
    return render_template("login.html")


# ---------- CHAT API ----------
@main.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    use_document = False

    # ✅ Enable document mode only if user types /doc
    if user_message.lower().startswith("/doc"):
        use_document = True
        user_message = user_message.replace("/doc", "").strip()

    # ✅ Load document only when requested
    if use_document and os.path.exists(DOCUMENT_FILE):
        with open(DOCUMENT_FILE, "r", encoding="utf-8") as f:
            doc_text = f.read().strip()

        if doc_text:
            user_message = f"""
Use the following document as reference:

{doc_text}

User Question:
{user_message}
"""

    # Get AI response
    ai_response = chat_manager.get_response(user_message)
    formatted_response = format_response(ai_response)

    # Save chat history
    save_message(user_message, formatted_response)

    return jsonify({"response": formatted_response})


# ---------- FILE UPLOAD API ----------
@main.route('/api/upload', methods=['POST'])
def upload_file():

    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    text = ""

    # Extract PDF text
    if file.filename.lower().endswith(".pdf"):
        reader = PdfReader(file)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()

    # Extract TXT text
    elif file.filename.lower().endswith(".txt"):
        text = file.read().decode("utf-8")

    else:
        return jsonify({"error": "Unsupported file type"}), 400

    # Save extracted text into file
    with open(DOCUMENT_FILE, "w", encoding="utf-8") as f:
        f.write(text)

    return jsonify({"message": "Document uploaded successfully"})
