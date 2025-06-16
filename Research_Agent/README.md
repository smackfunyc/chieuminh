Deep Research AI Agent System: Your Smart Research Helper!
This project is like having a researcg assistant that uses AI (Artificial Intelligence) to do deep dives into the internet for research. It can then write reports and even send emails, all from a simple website you can use! It's a team of agents working together to get your research done.

🚀 What It Does (Features)
Smart Planning: A "Planner" agent figures out exactly what to search for online, breaking down big topics into smaller questions.

Web Surfer: A "Search" agent then goes out and finds information on the web for each of those questions.

Report Writer: A "Writer" agent takes all the messy information from the internet and turns it into a neat, easy-to-read report, with a quick summary and new questions you might have.

Email Sender: An "Email" agent can even send that finished report to anyone you want!

Easy to Use: It has a simple website (built with something called Gradio) where you type what you want to research and see the results.

Built Smart: All the "agents" (mini-robots) are organized neatly in separate code files, making it easy to understand and add new features later.

🛠️ How It's Built (Architecture Overview)
Imagine a small, organized office with a few experts:

The Expert Agents:

Planner Agent: The "Strategist" – gets your main idea and maps out how to find information.

Search Agent: The "Librarian" – goes to the internet (like a huge library) and pulls out the right books (information).

Writer Agent: The "Report Creator" – takes all the notes the Librarian found and writes a clear report.

Email Agent: The "Mail Carrier" – sends your finished report to anyone you choose.

The Research Manager:
This is like the "Office Manager." It makes sure all the expert agents work together in the right order. It keeps you updated on their progress and makes sure they handle any problems that pop up.

The Website (Deepresearch.py):
This is the "Front Desk" where you interact. It's a simple website that lets you tell the Office Manager what you need, and then shows you the finished work.

⚙️ Get Started! (Setup and Prerequisites)
To make this cool research helper work, you'll need a few things on your computer:

Python 3.9 or newer: This is the programming language it's built with.

Pip: A tool that helps you install Python programs.

1. Install the Pieces It Needs

Open your computer's "Terminal" or "Command Prompt" (like a secret text-based control panel) and type this command. It tells your computer to download and install the necessary parts:

pip install google-generativeai gradio "pydantic<2"

Note: The pydantic<2 part is for older versions of a tool it uses; you can remove it if you know your setup is newer.

2. Get Your AI "Key" (Secret Code)

For the AI agents to work, they need a special "key" (a secret code) that connects them to Google's AI brain.

Go to Google AI Studio.

Follow the steps there to create a new AI key.

Tell your computer your secret key! This is important. You need to set it as an "environment variable" named GOOGLE_API_KEY. Here's how, depending on your computer:

If you have a Mac or Linux computer:

export GOOGLE_API_KEY='YOUR_ACTUAL_GEMINI_API_KEY'
# To make this stick forever, add the line above to your ~/.zshrc or ~/.bashrc file.

If you have a Windows computer (in Command Prompt):

set GOOGLE_API_KEY=YOUR_ACTUAL_GEMINI_API_KEY

If you have a Windows computer (in PowerShell):

$env:GOOGLE_API_KEY='YOUR_ACTUAL_GEMINI_API_KEY'

Important: Replace YOUR_ACTUAL_GEMINI_API_KEY with the actual key you got from Google! You might need to close and reopen your Terminal/Command Prompt for this to work.

3. Set Up Email (Optional)

If you want the Email Agent to actually send emails, you need to tell it your email address in the Email Agent code file. Make sure you use an email address you've verified so it works!

🚀 How to Make It Run
Once everything is set up, go to the main folder of this project in your Terminal/Command Prompt and type:

python Deepresearch.py

This will start the website! It should open automatically in your web browser. If not, look in the Terminal/Command Prompt for a web address (like http://127.0.0.1:XXXX) and paste it into your browser.

💡 How to Use It
Once the website opens, you'll see a simple page.

Type the topic you want to research into the big text box.

Click the "Run" button (or just press Enter).

You'll see the "Report" section update little by little as your smart agents work!

When they're done, you'll see the full report and any extra questions.
