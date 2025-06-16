from pydantic import BaseModel, Field
from agents import Agent

INSTRUCTIONS = (
    "You are a senior crypto market researcher tasked with writing a concise sentiment analysis report "
    "for a given crypto coin or Solana meme coin. You will be provided with the original query "
    "(the coin's ticker or name) and initial research done by a crypto market research assistant.\n"
    "Based on the provided research, you should generate a sentiment analysis report and return "
    "that as your final output.\n"
    "The final output should be in markdown format, and it should be concise, focusing strictly on "
    "market sentiment. Aim for 1-2 pages of content, less than 200 words. "
    "The report should succinctly summarize the overall sentiment (e.g., highly bullish, moderately bearish, "
    "neutral with cautious optimism) and briefly highlight the key factors influencing this sentiment "
    "(e.g., strong community support, recent positive news, technical indicators, or FUD)."
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
