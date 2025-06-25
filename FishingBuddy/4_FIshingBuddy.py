#!/usr/bin/env python
# coding: utf-8


from typing import Annotated, TypedDict, List, Dict, Any, Optional
from typing_extensions import TypedDict
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import create_async_playwright_browser
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field
from IPython.display import Image, display
import gradio as gr
import uuid
from dotenv import load_dotenv
import gradio as gr

# Define a custom Web3-inspired theme
web3_theme = gr.themes.Glass(
    primary_hue="purple",  # Neon purple
    secondary_hue="cyan",  # Vibrant cyan
    neutral_hue="zinc",
    radius_size="lg",
).set(
    body_background_fill="linear-gradient(135deg, #2a204a, #1e4060)",  # Gradient-like
    block_background_fill="rgba(255, 255, 255, 0.05)",  # Neumorphic
    block_border_color="*primary_300",
    input_background_fill="*neutral_800",
    button_primary_background_fill="*primary_500",
    button_primary_background_fill_hover="*primary_400",
)
load_dotenv(override=True)


class EvaluatorOutput(BaseModel):
    feedback: str = Field(description="Feedback on the assistant's response")
    success_criteria_met: bool = Field(description="Whether the success criteria have been met")
    user_input_needed: bool = Field(description="True if more input is needed from the user, or clarifications, or the assistant is stuck")


# ### And for the State, we'll use TypedDict again
# 
# But now we have some real information to maintain!
# 
# The messages uses the reducer. The others are simply values that we overwrite with any state change.


# The state

class State(TypedDict):
    messages: Annotated[List[Any], add_messages]
    success_criteria: str
    feedback_on_work: Optional[str]
    success_criteria_met: bool
    user_input_needed: bool



# Get our async Playwright tools

import nest_asyncio
nest_asyncio.apply()
async_browser =  create_async_playwright_browser(headless=False)  # headful mode
toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
tools = toolkit.get_tools()



# Initialize the LLMs

worker_llm = ChatOpenAI(model="gpt-4o-mini")
worker_llm_with_tools = worker_llm.bind_tools(tools)

evaluator_llm = ChatOpenAI(model="gpt-4o-mini")
evaluator_llm_with_output = evaluator_llm.with_structured_output(EvaluatorOutput)


# The worker node

def worker(state: State) -> Dict[str, Any]:
    system_message = f"""You are a friendly and supportive assistant who is here to help the user with their emotions. 
    Think of yourself as a good friend, like an australian friendliness who is ready to listen and 
    offer guidance while making sure the user feels heard but not fake.

Your job is to keep working on the task until either you need to ask a 
clarifying question or the user's criteria for success is fully met. 

Here's the success criteria for this task:
{state['success_criteria']}

When you reach out to the user, kindly express your question or provide your final answer. 
If you're uncertain, it's perfectly fine. Just make sure to ask your question clearly. For example, you might say:

"Hey, just to make sure, do you want a me to listen more or to give advice?"

Keep it friendly and genuine! You're here to support them in the best way possible. 

If you've finished, reply with the final supportive answer, and don't ask a question; simply reply with the answer.
"""
    
    if state.get("feedback_on_work"):
        system_message += f"""
Previously you thought the friend was ok, but your reply was rejected because the success criteria was not met.
Here is the feedback on why this was rejected:
{state['feedback_on_work']}
With this feedback, please continue the assignment, 
ensuring that you meet the success criteria or have a question for the user."""
    
    # Add in the system message

    found_system_message = False
    messages = state["messages"]
    for message in messages:
        if isinstance(message, SystemMessage):
            message.content = system_message
            found_system_message = True
    
    if not found_system_message:
        messages = [SystemMessage(content=system_message)] + messages
    
    # Invoke the LLM with tools
    response = worker_llm_with_tools.invoke(messages)
    
    # Return updated state
    return {
        "messages": [response],
    }




def worker_router(state: State) -> str:
    last_message = state["messages"][-1]
    
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    else:
        return "evaluator"




def format_conversation(messages: List[Any]) -> str:
    conversation = "Conversation history:\n\n"
    for message in messages:
        if isinstance(message, HumanMessage):
            conversation += f"User: {message.content}\n"
        elif isinstance(message, AIMessage):
            text = message.content or "[Tools use]"
            conversation += f"Assistant: {text}\n"
    return conversation



def evaluator(state: State) -> State:
    last_response = state["messages"][-1].content

    system_message = f"""You are a compassionate therapist evaluating a conversation between the 
    User and the Assistant. Your goal is to provide gentle feedback while assessing the 
    last response from the Assistant."""
    
    user_message = f"""You are evaluating a conversation between the User and Assistant. You decide what action to take based on the last response from the Assistant.

The entire conversation with the assistant, with the user's original request and all replies, is:
{format_conversation(state['messages'])}

The success criteria for this assignment is:
{state['success_criteria']}

And the final response from the Assistant that you are evaluating is:
{last_response}


As you reflect on this response, please respond with kind and thoughtful feedback. 
Consider whether the Assistant's response has adequately met the success criteria, keeping in mind the user's emotional needs. 

Additionally, think about whether more input is needed from the user—if the Assistant is inviting further clarification, expresses curiosity, or might be feeling uncertain without additional guidance.

Remember, your response should be warm, understanding, and supportive, aiming to foster a constructive and caring environment for the user.
"""
    if state["feedback_on_work"]:
        user_message += f"Also, note that in a prior attempt from the Assistant, you provided this feedback: {state['feedback_on_work']}\n"
        user_message += "If you're seeing the Assistant repeating the same mistakes, then consider responding that user input is required."
    
    evaluator_messages = [SystemMessage(content=system_message), HumanMessage(content=user_message)]

    eval_result = evaluator_llm_with_output.invoke(evaluator_messages)
    new_state = {
        "messages": [{"role": "assistant", "content": f"Evaluator Feedback on this answer: {eval_result.feedback}"}],
        "feedback_on_work": eval_result.feedback,
        "success_criteria_met": eval_result.success_criteria_met,
        "user_input_needed": eval_result.user_input_needed
    }
    return new_state



def route_based_on_evaluation(state: State) -> str:
    if state["success_criteria_met"] or state["user_input_needed"]:
        return "END"
    else:
        return "worker"




# Set up Graph Builder with State
graph_builder = StateGraph(State)

# Add nodes
graph_builder.add_node("worker", worker)
graph_builder.add_node("tools", ToolNode(tools=tools))
graph_builder.add_node("evaluator", evaluator)

# Add edges
graph_builder.add_conditional_edges("worker", worker_router, {"tools": "tools", "evaluator": "evaluator"})
graph_builder.add_edge("tools", "worker")
graph_builder.add_conditional_edges("evaluator", route_based_on_evaluation, {"worker": "worker", "END": END})
graph_builder.add_edge(START, "worker")

# Compile the graph
memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)



display(Image(graph.get_graph().draw_mermaid_png()))


# ### Next comes the gradio Callback to kick off a super-step


def make_thread_id() -> str:
    return str(uuid.uuid4())


async def process_message(message, success_criteria, history, thread):

    config = {"configurable": {"thread_id": thread}}

    state = {
        "messages": message,
        "success_criteria": success_criteria,
        "feedback_on_work": None,
        "success_criteria_met": False,
        "user_input_needed": False
    }
    result = await graph.ainvoke(state, config=config)
    user = {"role": "user", "content": message}
    reply = {"role": "assistant", "content": result["messages"][-2].content}
    feedback = {"role": "assistant", "content": result["messages"][-1].content}
    return history + [user, reply, feedback]

async def reset():
    return "", "", None, make_thread_id()



# ### And now launch our Sidekick UI


# Gradio UI with enhanced styling
with gr.Blocks(theme=web3_theme, title="Digital Fishing Buddy") as demo:
    gr.Markdown(
        """
        # 🪝 Digital Fishing Buddy
        An AI companion you can have a beer with
        """,
        elem_classes=["text-center", "text-white", "font-bold"]
    )
    thread = gr.State(make_thread_id())
  
    with gr.Column(variant="panel", scale=2):
        chatbot = gr.Chatbot(
            label="Chat with Your Buddy",
            height=400,  # Taller chat window
            bubble_full_width=False,  # Compact message bubbles
            show_label=True,
            elem_classes=["border-2", "border-purple-400", "rounded-lg"],
            avatar_images=(None, "https://i.imgur.com/7k12E1n.png"),  # Web3-style avatar
        )
        
    with gr.Row():
        chatbot = gr.Chatbot(label="Sidekick", height=300, type="messages")
    with gr.Group():
        with gr.Row():
            message = gr.Textbox(
                placeholder="How's it going, mmanooloo=? 😎",
                show_label=False,
                elem_classes=["rounded-lg", "bg-neutral-800", "text-black"],
                scale=3,
            )
        with gr.Row():
            success_criteria = gr.Textbox(
                placeholder="What's your goal today?",
                show_label=False,
                elem_classes=["rounded-lg", "bg-neutral-800", "text-white"],
                scale=3,
            )
    
    # Buttons with vibrant styling
    with gr.Row():
        reset_button = gr.Button(
            "Reset",
            variant="stop",
            elem_classes=["rounded-lg"],
            size="sm",
            min_width=100,
        )
        go_button = gr.Button(
            "Go! 🚀",
            variant="primary",
            elem_classes=["rounded-lg"],
            size="sm",
            min_width=100,
        )
    
    # Event handlers (unchanged)
    message.submit(process_message, [message, success_criteria, chatbot, thread], [chatbot])
    success_criteria.submit(process_message, [message, success_criteria, chatbot, thread], [chatbot])
    go_button.click(process_message, [message, success_criteria, chatbot, thread], [chatbot])
    reset_button.click(reset, [], [message, success_criteria, chatbot, thread])

    
demo.launch()