
from __future__ import annotations

from typing import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from IPython.display import Image, display
import gradio as gr
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
import random

from typing import Annotated, Iterable
from dotenv import load_dotenv
import gradio as gr
from gradio.themes.base import Base
from gradio.themes.utils import colors, fonts, sizes
from pydantic import BaseModel
import random
import time

# --- 80s Neon Custom Theme ---
class EightiesNeon(Base):
    def __init__(
        self,
        *,
        primary_hue: colors.Color | str = "pink",    # Neon pink
        secondary_hue: colors.Color | str = "cyan",  # Neon teal/cyan
        neutral_hue: colors.Color | str = "yellow",  # Neon yellow
        spacing_size: sizes.Size | str = sizes.spacing_md,
        radius_size: sizes.Size | str = sizes.radius_lg,
        text_size: sizes.Size | str = sizes.text_lg,
        font: fonts.Font | str | Iterable[fonts.Font | str] = (
            fonts.GoogleFont("Press Start 2P"),
            "cursive",
            "sans-serif",
        ),
        font_mono: fonts.Font | str | Iterable[fonts.Font | str] = (
            fonts.GoogleFont("IBM Plex Mono"),
            "ui-monospace",
            "monospace",
        ),
    ):
        super().__init__(
            primary_hue=primary_hue,
            secondary_hue=secondary_hue,
            neutral_hue=neutral_hue,
            spacing_size=spacing_size,
            radius_size=radius_size,
            text_size=text_size,
            font=font,
            font_mono=font_mono,
        )
        super().set(
            body_background_fill="linear-gradient(135deg, yellow 0%, pink 100%)",
            body_background_fill_dark="linear-gradient(135deg, #22223b 0%, pink 100%)",
            button_primary_background_fill="linear-gradient(90deg, cyan 0%, pink 100%)",
            button_primary_background_fill_hover="linear-gradient(90deg, yellow 0%, cyan 100%)",
            button_primary_text_color="#22223b",
            block_shadow="0 0 24px 4px cyan, 0 0 64px 16px pink",
            block_border_width="4px",
            block_title_text_weight="900",
            button_primary_shadow="0 0 12px 2px cyan",
            # radius_size="2rem",  # <-- REMOVE THIS LINE!
        )

eighties_theme = EightiesNeon()

# --- Data & Useful Constants ---
nouns = [
    "Jell-O",
"Dudes",
"Rad BMX",
"Frosted Flakes",
"Back to the Future",
"80s music",
"Bike rides",
"Wide skateboards",
"Cable TV",
"Neon Socks"
]
adjectives = [
    "fantastic",
"awesome",
"mystical",
"lively",
"quirky",
"energetic",
"Big Hair",  
"cheerful",
"zesty",       
"radiant",
"outrageous",  
"refreshing",
"playful",
"existential", 
"chill",
"sparkly",
"trustworthy",
"witty",
"bouncy",
"groovy"
]

# --- Load environment variables, if needed ---
load_dotenv(override=True)

# --- LangGraph/State Definitions ---
try:
    from langgraph.graph import StateGraph, START, END
    from langgraph.graph.message import add_messages
except ImportError:
    # Fallback if langgraph is not installed (for UI testing only)
    StateGraph = None
    START, END = "START", "END"
    def add_messages(x): return x

class State(BaseModel):
    messages: Annotated[list, add_messages]

def our_first_node(old_state: State) -> State:
    reply = f"{random.choice(nouns)} are {random.choice(adjectives)}"
    messages = [{"role": "assistant", "content": reply}]
    new_state = State(messages=messages)
    return new_state

if StateGraph:
    graph_builder = StateGraph(State)
    graph_builder.add_node("first_node", our_first_node)
    graph_builder.add_edge(START, "first_node")
    graph_builder.add_edge("first_node", END)
    graph = graph_builder.compile()
else:
    graph = None

# --- Chat function for Gradio ---
def chat(user_input: str, history):
    if not graph:
        # Fallback for UI testing
        return f"{random.choice(nouns)} are {random.choice(adjectives)}"
    message = {"role": "user", "content": user_input}
    messages = [message]
    state = State(messages=messages)
    result = graph.invoke(state)
    return result["messages"][-1].content

# --- Launch the Gradio Chat Interface ---
gr.ChatInterface(
    chat,
    type="messages",
    theme=eighties_theme,
    title="🌈 Neon Chatbot 🌈",
    description="Talk retro vibes!",
).launch()