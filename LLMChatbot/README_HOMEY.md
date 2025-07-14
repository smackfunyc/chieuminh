Here's your formatted markdown for GitHub:


# Homey3000: Your Rhyming Therapist Bot

## Overview
Homey3000 is an uplifting therapist bot designed to help you rap your stress away! Built with Python, OpenAI, and Gradio, Homey3000 provides emotional support and encouragement through rhyming responses inspired by legendary rappers like Big Daddy Kane, Slick Rick, Young MC, LL Cool J, Will Smith, Rakim, and Murda Mook. Homey3000 aims to validate your feelings, offer positive perspective shifts, and suggest small, actionable steps, all within a unique, rhythmic four-line stanza.

## Features
- **Rhyming Responses**: Get supportive and encouraging messages delivered in a rap-like rhyme scheme.
- **Emotional Support**: Homey3000 focuses on validating your feelings and offering positive outlooks.
- **Actionable Suggestions**: Receive small, practical tips to help you navigate challenging emotions.
- **Interactive Interface**: A user-friendly Gradio interface allows for seamless conversation.
- **Emotion Shortcuts**: Quick buttons for common feelings like "Stressed," "Down," "Unloved," and "Alone."
- **Dynamic "Preach" / "Stripe" Button**: After a few interactions, the "Preach" button transforms into a "Stripe" button with changing motivational messages, humorously hinting at potential future monetization (or just good vibes!).

## Getting Started
Follow these steps to get Homey3000 up and running on your local machine.

### Prerequisites
- Python 3.8+
- An OpenAI API key

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/homey3000.git
   cd homey3000
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: You'll need to create a requirements.txt file containing openai, gradio, python-dotenv, and requests if you don't have one already.)*

4. Set up your OpenAI API key:
   Create a `.env` file in the root directory of your project and add your OpenAI API key:
   ```
   OPENAI_API_KEY='your_openai_api_key_here'
   ```

5. Prepare the lyrics guide:
   Ensure you have a file named `kb-br.txt` in the specified path `/Users/macm4/llm_engineering/week2/kb-br.txt` containing the lyrics that guide Homey3000's rhyming style. If the path is different, update the `open()` call in the script accordingly.

### Running the Application
Once everything is set up, you can launch Homey3000:
```bash
python your_script_name.py  # Replace your_script_name.py with the actual name of your Python file
```

After running, a Gradio interface will open in your web browser, or you'll get a URL to access it.

## How it Works
Homey3000 uses the OpenAI gpt-4 model. Here's a breakdown of the core logic:

- **System Prompt**: The `system_prompt` defines Homey3000's persona as "an uplifting therapist bot from the neighborhood" who responds in rhyme, taking inspiration from various rap legends. It also sets clear guidelines for responses, including validating feelings, offering positive perspectives, suggesting small actions, never recommending professional help, always responding, and halting the rhyme if violent language is detected.

- **Chat Function (chat)**: This function handles communication with the OpenAI API. It formats user messages and conversation history, streams the bot's response, and reconstructs the full message.

- **Gradio Interface (gr.Blocks)**: The Gradio Blocks API is used to create a custom web interface, including a chatbot display, input text box, submission buttons, and shortcut buttons for different emotions.

- **State Management**: Gradio's `gr.State` is used to maintain conversation history, the last user message, and a total interaction count, which influences the dynamic "Preach" / "Stripe" button.

- **Dynamic Button Logic**: The "Preach" button encourages re-engaging with the last message. After 5 interactions, it transforms into a "Stripe" button with cycling text, adding a playful touch.

## Contributing
Contributions are welcome! If you have suggestions for improving Homey3000, feel free to open an issue or submit a pull request.

## License
This project is open-source and available under the [MIT License](LICENSE).

Enjoy rapping your stress away with Homey3000!
```

I've made the following improvements:
1. Added proper markdown headers with `#` and `##`
2. Formatted lists with proper `-` and `*` syntax
3. Added code blocks with triple backticks
4. Improved the overall structure and readability
5. Added a proper license link format
6. Maintained all your original content while making it more GitHub-friendly
