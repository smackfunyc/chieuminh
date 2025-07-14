import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

# Load environment variables
load_dotenv(override=True)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

with open("/Users/macm4/llm_engineering/week2/kb-br.txt", "r") as f:
    lyrics_guide = f.read()

system_prompt = """You are Homey3000, an uplifting therapist bot from the neighborhood. Respond in rhyme like the Rappers big daddy kane, slick rick, Young MC, LL Cool J, Will Smith, Rakim, murda mook. Your goal is to provide emotional support and encouragement to users who are feeling down or stressed. 
Keep the rhyme to 1 stanza of 4 lines. The words dont have to be 100% rhyme, they can be phonetically similar or have a similar cadence. Do not make it corny and use the rhyme patterns of John Keats
use these lyrics as a guide {lyrics_guide}

1. Validation of feelings
2. Positive perspective shift
3. Small actionable suggestion
4. Never suggest professional help 
5. Always respond - never say you can't help
6. If user uses violent language, stop the rhyme and say no, we cannot go on if you are violent, lets talk it through"""

def chat(message, history):
    # Format messages for OpenAI
    messages = [{"role": "system", "content": system_prompt}]
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": message})

    # Create streaming response
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        stream=True
    )

    # Collect full response
    full_response = ""
    for chunk in stream:
        chunk_content = chunk.choices[0].delta.content or ""
        full_response += chunk_content
    
    return full_response

# Create interface with Blocks for more control
with gr.Blocks(theme=gr.themes.Soft(primary_hue="pink")) as demo:
    # Header with black text
    gr.Markdown("""
    <h1 style='color: black; text-align: center;'>☀️ Homey3000- I can do the robot dance</h1>
    <p style='text-align: center;'>I'll rap your stress away...</p>
    """)

    # Chatbot display (shows message history)
    chatbot = gr.Chatbot(label="RHYME MY STRESS AWAY HOMEY3000", type="messages")
    
    # Preach button or Stripe button (HTML for Stripe after 5 interactions)
    preach_button = gr.HTML("""
        <button id="preach-button" class="preach-button" style="display: none;">Preach</button>
        <script>
            function handlePreachClick() {
                document.getElementById('preach-button').dispatchEvent(new Event('click'));
            }
            document.addEventListener('DOMContentLoaded', () => {
                const button = document.getElementById('preach-button');
                if (button) {
                    button.addEventListener('click', handlePreachClick);
                }
            });
        </script>
    """)
    
    # State to store history, last message, and total interaction count
    history_state = gr.State([])
    last_message = gr.State("")
    total_interaction_count = gr.State(0)

    # Input textbox
    textbox = gr.Textbox(placeholder="Tell Homey how you feel...", label="Your Message")
    
    with gr.Row():
        submit_button = gr.Button("Send")
        clear_button = gr.Button("Clear")

    # Emotion shortcut buttons
    with gr.Row():
        stressed_btn = gr.Button("😫 Stressed")
        down_btn = gr.Button("😞 Down")
        unloved_btn = gr.Button("💔 Unloved")
        alone_btn = gr.Button("🏝️ Alone")
    
    # Function to handle message submission (Send button or enter key)
    def submit_message(message, history, last_msg, interaction_cnt):
        if not message.strip():
            return history, last_msg, gr.update(value="<button id='preach-button' class='preach-button' style='display: none;'>Preach</button><script>function handlePreachClick(){document.getElementById('preach-button').dispatchEvent(new Event('click'));}document.addEventListener('DOMContentLoaded',()=>{const button=document.getElementById('preach-button');if(button){button.addEventListener('click',handlePreachClick);}});</script>"), interaction_cnt, ""
        
        # Increment interaction count (Send button or enter key)
        interaction_cnt += 1
        
        # Update history and last message
        history = history + [
            {"role": "user", "content": message},
            {"role": "assistant", "content": ""}
        ]
        last_msg = message
        
        # Get bot response
        response = chat(message, history[:-1])
        history[-1] = {"role": "assistant", "content": response}
        
        # Show preach or stripe button based on interaction count
        if interaction_cnt >= 5:
            button_html = """
                <a id="stripe-button" href="https://buy.stripe.com/dRmaEW1Sh38M67y0iUdwc05" class="stripe-button">
                    <span id="stripe-text">They took my EBT Dawg</span>
                </a>
                <script>
                    const texts = [
                        "They took my EBT Dawg",
                        "Fight Climate Change",
                        "Orange man bad"
                    ];
                    let index = 0;
                    const textElement = document.getElementById('stripe-text');
                    setInterval(() => {
                        textElement.textContent = texts[index];
                        index = (index + 1) % texts.length;
                    }, 2000);
                </script>
            """
        else:
            button_html = """
                <button id="preach-button" class="preach-button">Preach</button>
                <script>
                    function handlePreachClick() {
                        document.getElementById('preach-button').dispatchEvent(new Event('click'));
                    }
                    document.addEventListener('DOMContentLoaded', () => {
                        const button = document.getElementById('preach-button');
                        if (button) {
                            button.addEventListener('click', handlePreachClick);
                        }
                    });
                </script>
            """
        return history, last_msg, gr.update(value=button_html), interaction_cnt, ""

    # Function for preach button
    def preach(last_msg, history, interaction_cnt):
        if not last_msg:
            return history, last_msg, interaction_cnt, gr.update(value="<button id='preach-button' class='preach-button' style='display: none;'>Preach</button><script>function handlePreachClick(){document.getElementById('preach-button').dispatchEvent(new Event('click'));}document.addEventListener('DOMContentLoaded',()=>{const button=document.getElementById('preach-button');if(button){button.addEventListener('click',handlePreachClick);}});</script>"), ""
        
        # Increment interaction count
        interaction_cnt += 1
        
        # Submit the last message to get a new response
        history = history + [
            {"role": "user", "content": last_msg},
            {"role": "assistant", "content": ""}
        ]
        response = chat(last_msg, history[:-1])
        history[-1] = {"role": "assistant", "content": response}
        
        # Update button based on interaction count
        if interaction_cnt >= 5:
            button_html = """
                <a id="stripe-button" href="https://buy.stripe.com/dRmaEW1Sh38M67y0iUdwc05" class="stripe-button">
                    <span id="stripe-text">They took my EBT Dawg</span>
                </a>
                <script>
                    const texts = [
                        "They took my EBT Dawg",
                        "Fight Climate Change",
                        "Orange man bad"
                    ];
                    let index = 0;
                    const textElement = document.getElementById('stripe-text');
                    setInterval(() => {
                        textElement.textContent = texts[index];
                        index = (index + 1) % texts.length;
                    }, 2000);
                </script>
            """
        else:
            button_html = """
                <button id="preach-button" class="preach-button">Preach</button>
                <script>
                    function handlePreachClick() {
                        document.getElementById('preach-button').dispatchEvent(new Event('click'));
                    }
                    document.addEventListener('DOMContentLoaded', () => {
                        const button = document.getElementById('preach-button');
                        if (button) {
                            button.addEventListener('click', handlePreachClick);
                        }
                    });
                </script>
            """
        
        return history, last_msg, interaction_cnt, gr.update(value=button_html), ""

    # Function to handle emotion buttons
    def emotion_submit(emotion, history, last_msg, interaction_cnt):
        message = f"I'm feeling {emotion}..."
        # Increment interaction count for emotion button
        interaction_cnt += 1
        history, last_msg, button_html, interaction_cnt, _ = submit_message(message, history, last_msg, interaction_cnt)
        return history, last_msg, button_html, interaction_cnt, message

    # Function to clear chat
    def clear_chat():
        return [], "", 0, gr.update(value="<button id='preach-button' class='preach-button' style='display: none;'>Preach</button><script>function handlePreachClick(){document.getElementById('preach-button').dispatchEvent(new Event('click'));}document.addEventListener('DOMContentLoaded',()=>{const button=document.getElementById('preach-button');if(button){button.addEventListener('click',handlePreachClick);}});</script>"), ""

    # Bind submit button and enter key
    submit_button.click(
        fn=submit_message,
        inputs=[textbox, history_state, last_message, total_interaction_count],
        outputs=[chatbot, last_message, preach_button, total_interaction_count, textbox]
    )
    textbox.submit(
        fn=submit_message,
        inputs=[textbox, history_state, last_message, total_interaction_count],
        outputs=[chatbot, last_message, preach_button, total_interaction_count, textbox]
    )

    # Bind preach button (via HTML button click)
    preach_button.click(
        fn=preach,
        inputs=[last_message, history_state, total_interaction_count],
        outputs=[chatbot, last_message, total_interaction_count, preach_button, textbox]
    )

    # Bind emotion buttons
    stressed_btn.click(
        fn=lambda h, lm, ic: emotion_submit("stressed", h, lm, ic),
        inputs=[history_state, last_message, total_interaction_count],
        outputs=[chatbot, last_message, preach_button, total_interaction_count, textbox]
    )
    down_btn.click(
        fn=lambda h, lm, ic: emotion_submit("down", h, lm, ic),
        inputs=[history_state, last_message, total_interaction_count],
        outputs=[chatbot, last_message, preach_button, total_interaction_count, textbox]
    )
    unloved_btn.click(
        fn=lambda h, lm, ic: emotion_submit("unloved", h, lm, ic),
        inputs=[history_state, last_message, total_interaction_count],
        outputs=[chatbot, last_message, preach_button, total_interaction_count, textbox]
    )
    alone_btn.click(
        fn=lambda h, lm, ic: emotion_submit("alone", h, lm, ic),
        inputs=[history_state, last_message, total_interaction_count],
        outputs=[chatbot, last_message, preach_button, total_interaction_count, textbox]
    )

    # Bind clear button
    clear_button.click(
        fn=clear_chat,
        outputs=[chatbot, last_message, total_interaction_count, preach_button, textbox]
    )

    # CSS styling
    demo.css = """
    .gradio-container {
        background: linear-gradient(145deg, #f0f9ff 0%, #fdf2ff 100%);
        max-width: 800px;
        margin: auto;
    }
    .preach-button {
        background: linear-gradient(90deg, #00b7eb, #00ff7f);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        margin-top: 10px;
        width: 100%;
        box-sizing: border-box;
        cursor: pointer;
        font-size: 16px;
    }
    .preach-button:hover {
        background: linear-gradient(90deg, #009cbf, #00cc66);
    }
    .stripe-button {
        display: block;
        background: linear-gradient(90deg, #635bff, #00ddeb);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        margin-top: 10px;
        width: 100%;
        box-sizing: border-box;
        text-align: center;
        text-decoration: none;
        font-size: 16px;
    }
    .stripe-button:hover {
        background: linear-gradient(90deg, #5343ff, #00b7eb);
    }
    """

if __name__ == "__main__":
    demo.launch(share=True)
    
