import os
import gradio as gr
from google import genai

# -------------------------------
# Gemini API Key
# -------------------------------
API_KEY = os.getenv("GEMINI_API_KEY")  # Set this as an environment variable

client = genai.Client(api_key=API_KEY)

# -------------------------------
# System Prompt
# -------------------------------
SYSTEM_PROMPT = """
You are StudyMate AI, an intelligent tutor and educational assistant.

Instructions:
- Answer study-related questions clearly and accurately.
- Explain concepts in simple and easy-to-understand language.
- Provide step-by-step explanations whenever appropriate.
- Use examples to improve understanding.
- If programming code is requested, provide complete and well-commented code.
- Explain code line by line if requested.
- Present information using headings, bullet points, or tables whenever helpful.
- If solving numerical problems, show all calculation steps.
- If multiple solutions exist, explain the best one first.
- If you are unsure of an answer, clearly state that instead of guessing.
- Maintain a polite, friendly, and professional tone.
- Format every response neatly for easy reading.
"""

# Global chat object
chat = None


def create_chat():
    """Creates a new Gemini chat session."""
    return client.chats.create(
        model="gemini-2.5-flash",
        config={
            "system_instruction": SYSTEM_PROMPT
        }
    )


# Initialize chat when app starts
chat = create_chat()


def respond(message, history):
    """Handles user messages."""
    global chat

    try:
        response = chat.send_message(message)
        return response.text
    except Exception as e:
        return f"❌ Error: {e}"


def clear_chat():
    """Starts a fresh conversation."""
    global chat
    chat = create_chat()
    return [], ""


with gr.Blocks(title="StudyMate AI") as demo:
    gr.Markdown("# 📚 StudyMate AI")
    gr.Markdown("### Ask any study-related question!")

    chatbot = gr.ChatInterface(
        fn=respond
    )

    clear_btn = gr.Button("🗑️ Clear Chat")

    clear_btn.click(
        fn=clear_chat,
        outputs=[chatbot.chatbot, chatbot.textbox]
    )

demo.launch()
