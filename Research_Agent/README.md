# 🤖 Deep Research AI Agent System

A smart, AI-powered research assistant that digs deep into the web, compiles structured reports, and can even email them—all from a simple web interface.

---

## 🚀 Features

- **Planner Agent**: Breaks big topics into actionable research questions.
- **Search Agent**: Gathers information from the web for each question.
- **Writer Agent**: Summarizes findings into a clean report with takeaways.
- **Email Agent**: Sends the report to any recipient (optional).
- **Gradio UI**: User-friendly website to start, track, and receive research output.
- **Modular Codebase**: Agents are separated for easy understanding and extensibility.


---

## 🧠 Architecture Overview

- **Planner** → decides what to search.
- **Searcher** → fetches info online.
- **Writer** → composes the final report.
- **Emailer** → sends it via email (if enabled).
- **Manager** → coordinates the above agents.
- **Web UI** → built with Gradio (`Deepresearch.py`) for user interaction.

---

## ⚙️ Setup

### Requirements
- Python 3.9+
- Pip
- Google Generative AI key (Gemini)

### Install Dependencies
```bash
pip install google-generativeai gradio "pydantic<2"

Set Your Gemini API Key
Mac/Linux:

export GOOGLE_API_KEY='your-key-here'
Windows (CMD):

set GOOGLE_API_KEY=your-key-here
Windows (PowerShell):

$env:GOOGLE_API_KEY='your-key-here'
(Optional) Email Setup
Edit email_agent.py and add your email credentials.

▶️ Run the App

python Deepresearch.py
The app will open in your browser (or visit the link shown in the terminal).

💡 How to Use

Enter a topic in the textbox.
Click Run.
Watch the report build in real time.
Optionally, email it to any recipient.
📄 License

MIT License

🙏 Credits

Created by Chieu Minh Nguyen
