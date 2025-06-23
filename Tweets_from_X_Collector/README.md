# 🐦 Web3 Twitter Collector

An interactive Web3-style Gradio app for collecting and analyzing tweets with advanced search filters, built using the `twikit` API client. Login, collect, preview, and export tweets from Twitter (X) in real time.

---

## 🚀 Features

- **Login Support**: Authenticates via email and password using `twikit`.
- **Search Agent**: Collects tweets based on keywords, hashtags, or phrases.
- **Ignore Filter**: Skips tweets containing unwanted keywords.
- **Live Progress**: View and stop tweet collection anytime.
- **Data Export**: Automatically saves tweets to `tweets.csv`.
- **Gradio Web3 UI**: Stylish, themed interface powered by Gradio Blocks.

---

## 🛠 Tech Stack

- Python 3.10+
- [twikit](https://github.com/Xonshiz/twikit) – Twitter API wrapper
- [Gradio](https://gradio.app/) – UI framework
- [httpx](https://www.python-httpx.org/) – async HTTP client
- pandas, asyncio, datetime – data handling and control flow

---

## ⚙️ Setup Instructions

### 1. Install dependencies

pip install -r requirements.txt

---
 RUN THE APP
python your_script_name.py

---
💡 How to Use
---
Enter your Twitter email and password under the "Authentication" tab.
In the "Collect Tweets" tab:
Set a search query
Choose search style (LATEST, TOP, etc.)
Adjust tweet count limit
(Optional) Add ignored words
Click Start Collection to begin.
View tweets live or download as a CSV file.
---
 Credits Built by Chieu Minh Nguyen
---
Design powered by custom Gradio Web3 theme.
```bash

