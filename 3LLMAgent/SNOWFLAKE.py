from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables (API key)
load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')

if not openai_api_key:
    raise ValueError("OpenAI API Key not set in .env file!")

client = OpenAI(api_key=openai_api_key)

# --- STEP 1: Pick a business area for Agentic AI ---
business_area_prompt = """  
What is a promising but underserved business area with Snowflake where **Agentic AI**  
(autonomous, goal-driven AI agents) could create significant value?  
Pick two problems that Snowflake is facing and explain why it's a good fit in 1-2 sentences.  
"""  

response = client.chat.completions.create(  
    model="gpt-4-turbo",  
    messages=[{"role": "user", "content": business_area_prompt}]  
)  

business_area = response.choices[0].message.content  
print("🚀 **Selected Business Area:**\n", business_area)  

# --- STEP 2: Identify a key pain point in that industry ---  
pain_point_prompt = f"""  
In the business areayou just mentioned: **{business_area}**,  
what is a major operational or customer-related pain point that is:  
1. Costly or inefficient today  
2. Could benefit from autonomous AI agents?  
Explain in 1-2 sentences.  
"""  

response = client.chat.completions.create(  
    model="gpt-4-turbo",  
    messages=[{"role": "user", "content": pain_point_prompt}]  
)  

pain_point = response.choices[0].message.content  
print("\n🔴 **Key Pain Point:**\n", pain_point)  

# --- STEP 3: Propose an Agentic AI solution ---  
solution_prompt = f"""  
Given the pain point: **{pain_point}**,  
design an **Agentic AI solution** (autonomous AI agents) that could solve it.  
Structure your answer as:  
1. **Solution Name** (e.g., "SnowflakeAgent")  
2. **How it works** (1-2 sentences)  
3. **Key benefits** (bullet points)  
"""  

response = client.chat.completions.create(  
    model="gpt-4-turbo",  
    messages=[{"role": "user", "content": solution_prompt}]  
)  

agentic_solution = response.choices[0].message.content  
print("\n🤖 **Agentic AI Solution Proposal:**\n", agentic_solution)  