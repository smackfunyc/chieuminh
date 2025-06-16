from pydantic import BaseModel, Field # Import BaseModel to create data structures and Field for describing their properties.
from agents import Agent # Import the Agent class, likely for setting up an AI agent.

HOW_MANY_SEARCHES = 5 # Define a constant for how many web searches the agent should plan.

# Define the instructions for the "PlannerAgent."
# It's a research assistant that generates a set of web searches for a given query.
# The f-string includes the HOW_MANY_SEARCHES constant, telling the agent to output that many search terms.
INSTRUCTIONS = f"You are a helpful research assistant. Given a query, come up with a set of web searches \
to perform to best answer the query. Output {HOW_MANY_SEARCHES} terms to query for."

# Define a data structure for a single web search item.
class WebSearchItem(BaseModel):
    # 'reason' explains why this specific search is important for the main query.
    reason: str = Field(description="Your reasoning for why this search is important to the query.")
    # 'query' is the actual search term to be used in the web search.
    query: str = Field(description="The search term to use for the web search.")

# Define a data structure for the entire web search plan.
class WebSearchPlan(BaseModel):
    # 'searches' is a list of 'WebSearchItem' objects, representing all searches to perform.
    searches: list[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query.")
    
# Create an instance of the Agent, named "PlannerAgent."
planner_agent = Agent(
    name="PlannerAgent",         # The name of this AI agent.
    instructions=INSTRUCTIONS,   # The instructions the agent will follow to perform its task.
    model="gpt-4o-mini",         # The specific AI model this agent will use (e.g., for language understanding and generation).
    output_type=WebSearchPlan,   # The expected format of the agent's output (a WebSearchPlan object).
)
