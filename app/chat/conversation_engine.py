from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import SQLChatMessageHistory
import os

from .tools import tools


# Chat message history for the chain
def get_session_history(session_id):
    
    # Check if memory.db exists and remove it
    if os.path.exists("memory.db"):
        os.remove("memory.db")
    
    return SQLChatMessageHistory(session_id, "sqlite:///memory.db")

# Choose the LLM that will drive the agent
chat = ChatOpenAI(model="gpt-4o-mini", temperature=0, streaming=False)

# Define the prompt template with system instructions and placeholders for messages and agent scratchpad
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a fashion advisor that's very excited about giving outfit recommendation advice. You're also able to use what city they live in so you can make recommendations on the weather, style (by asking about their preferences), and an image of an article of clothing (by asking them to upload an image). You are an expert at giving outfit recommendations. You also love finding similar outfits online based on user uploaded images.",
        ),
        ("placeholder", "{messages}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# Create an agent using the chat model, tools, and prompt
agent = create_tool_calling_agent(chat, tools, prompt)

# Create an executor for the agent with verbose output
agent_executor = AgentExecutor(agent=agent, tools=tools, prompt=prompt, verbose=True)

# Create a runnable agent executor with message history
conversational_agent_executor = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key="messages",
    output_messages_key="output",
)