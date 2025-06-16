import os  # Used to get environment variables, like your SendGrid API key.
from typing import Dict  # Used to tell Python that a function will return a dictionary.

import sendgrid  # The library that helps send emails using SendGrid.
from sendgrid.helpers.mail import Email, Mail, Content, To # Specific parts of the SendGrid library to build an email.
from agents import Agent, function_tool # 'Agent' is likely for creating an AI agent, and 'function_tool' marks a function for the agent to use.

@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """
    Sends an email with a subject and content that can include HTML.
    This function is marked as a tool, meaning an AI agent can use it.
    """
    # Connect to SendGrid using your special key (from environment variables).
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    
    # Set who the email is from. **Remember to change "youremail@domain.com" to your actual verified sender email.**
    from_email = Email("youremail@domain.com") 
    
    # Set who the email is going to. **Remember to change "anotheremail@domain.com" to the actual recipient.**
    to_email = To("anotheremail@domain.com") 
    
    # Create the email content, specifying it's HTML.
    content = Content("text/html", html_body)
    
    # Put all the email parts together (sender, recipient, subject, content).
    mail = Mail(from_email, to_email, subject, content).get()
    
    # Send the email through SendGrid.
    response = sg.client.mail.send.post(request_body=mail)
    
    # Print the status code from SendGrid (e.g., 202 means success).
    print("Email response", response.status_code)
    
    # Return a status message indicating success.
    return {"status": "success"}

# These are the instructions for the AI "Email agent."
INSTRUCTIONS = """You're an expert at sending well-formatted HTML emails from detailed reports.
You'll get a detailed report. Your job is to use your email tool to send just one email.
Make sure the report is converted into clean, good-looking HTML with a suitable subject line."""

# Create the Email agent.
email_agent = Agent(
    name="Email agent",          # Give the agent a name.
    instructions=INSTRUCTIONS,   # Tell the agent what it needs to do.
    tools=[send_email],          # Give the agent the 'send_email' function to use.
    model="gpt-4o-mini",         # Specify which AI model the agent should use.
)
