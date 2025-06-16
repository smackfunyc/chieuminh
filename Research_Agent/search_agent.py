from agents import Agent, WebSearchTool, ModelSettings # Import necessary classes: Agent for creating AI agents, WebSearchTool to enable web searching, and ModelSettings for configuring the AI model's behavior.

# Define the instructions for the "Search agent."
# These instructions guide the AI on how to perform its research task specifically for crypto coins.
INSTRUCTIONS = (
    "You are a crypto market research assistant. Given a specific crypto coin or Solana meme coin "
    "(by ticker or full name), you search recent market data, news, and community discussions. "
    "Produce a concise summary of your findings. The summary must be 2-3 paragraphs and less than 300 "
    "words. Capture the main points: recent price action, significant whale movements or exchange listings, "
    "key development updates or partnerships, and overall market sentiment (e.g., bullish, bearish, "
    "consolidating). Write succinctly; no need for complete sentences or perfect grammar. "
    "This information will be consumed by someone synthesizing a crypto market report, so it's vital "
    "you capture the essence and ignore any fluff or speculative commentary. Do not include any "
    "additional commentary or disclaimers other than the summary itself. Focus on actionable insights "
    "relevant to the coin's current market standing and potential near-term trajectory."
)

# Create an instance of the Agent, named "Search agent."
search_agent = Agent(
    name="Search agent",           # The name of this AI agent.
    instructions=INSTRUCTIONS,     # The detailed instructions the agent will follow for crypto research.
    tools=[WebSearchTool(search_context_size="low")], # Provide the agent with a WebSearchTool.
                                # 'search_context_size="low"' suggests a concise search approach.
    model="gpt-4o-mini",           # The specific AI model this agent will use for processing instructions and generating summaries.
    model_settings=ModelSettings(tool_choice="required"), # Configure the model settings to ensure it always uses a tool (in this case, the WebSearchTool).
)
