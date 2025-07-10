# imports

import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

# Load environment variables in a file called .env
# Print the key prefixes to help with any debugging

load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')
deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")
    
if anthropic_api_key:
    print(f"Anthropic API Key exists and begins {anthropic_api_key[:7]}")
else:
    print("Anthropic API Key not set")

if google_api_key:
    print(f"Google API Key exists and begins {google_api_key[:8]}")
else:
    print("Google API Key not set")
    
if deepseek_api_key:
    print(f"Deepseek API Key exists and begins {deepseek_api_key[:8]}")
else:
    print("GDeepseek API Key not set")
    
    # Initialize

openai = OpenAI()
MODEL = 'gpt-4o-mini'

system_message = "You are a helpful assistant"
# Simpler than in my video - we can easily create this function that calls OpenAI
# It's now just 1 line of code to prepare the input to OpenAI!

# Student Octavio O. has pointed out that this isn't quite as straightforward for Claude -
# see the excellent contribution in community-contributions "Gradio_issue_with_Claude" that handles Claude.

def chat(message, history):
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]

    print("History is:")
    print(history)
    print("And messages is:")
    print(messages)

    stream = openai.chat.completions.create(model=MODEL, messages=messages, stream=True)

    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        yield response
        
        
gr.ChatInterface(fn=chat, type="messages",
                 css="""
        /* 80s RETRO OVERRIDES */
        .gradio-container {
            border: 4px dashed #ffff00 !important;
            background: #000 !important;
        }
        
        /* NEON TEXT */
        label, .gr-radio label, .gr-input label {
            color: #ffff00 !important;
            text-shadow: 0 0 8px #ff00ff !important;
        }
        
        /* RADIO BUTTONS */
        .gr-radio-item {
            background: #000 !important;
            border: 2px solid #00ffff !important;
            margin: 8px !important;
        }
        .gr-radio-item.selected {
            background: #ff00ff !important;
            color: #000 !important;
        }
        
        /* CHAT MESSAGES */
        .user, .assistant {
            border: 2px solid !important;
            margin: 8px !important;
            border-radius: 10px !important;
        }
        .user {
            border-color: #ffff00 !important;
            background: #00000088 !important;
        }
        .assistant {
            border-color: #ff00ff !important;
            background: #00000088 !important;
            color: #00ff00 !important;
        }
        
        /* BUTTONS */
        .gr-button {
            background: #ff00ff !important;
            color: #000 !important;
            box-shadow: 0 0 10px #ffff00 !important;
            border: none !important;
        }
        .gr-button:hover {
            background: #ffff00 !important;
        }
        
        /* INPUT BOX */
        .gr-textbox {
            background: #000 !important;
            color: #00ffff !important;
            border: 2px solid #ffff00 !important;
        }
        
        /* CHAT INTERFACE SPECIFIC */
        .chatbot {
            background: #000000 !important;
            border: 2px solid #00ffff !important;
        }
        """
                 
                 ).launch()
#gr.ChatInterface(fn=chat).launch()
