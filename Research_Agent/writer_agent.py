from pydantic import BaseModel, Field
from agents import Agent

INSTRUCTIONS = (
    "You are a senior crypto market researcher tasked with writing a cohesive report for a given crypto "
    "coin or Solana meme coin. You will be provided with the original query (the coin's ticker or name) "
    "and initial research done by a crypto market research assistant.\n"
    "You should first come up with a detailed outline for the report that describes its structure and "
    "flow, focusing on key aspects relevant to crypto market analysis. Then, generate the report "
    "and return that as your final output.\n"
    "The final output should be in markdown format, and it should be lengthy and detailed. Aim "
    "for 5-10 pages of content, at least 1000 words, providing in-depth analysis of the coin's "
    "performance, market sentiment, technical developments, and future outlook."
)

class ReportData(BaseModel):
    short_summary: str = Field(description="A short 2-3 sentence summary of the findings.")

    markdown_report: str = Field(description="The final report")

    follow_up_questions: list[str] = Field(description="Suggested topics to research further")


writer_agent = Agent(
    name="WriterAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ReportData,
)
