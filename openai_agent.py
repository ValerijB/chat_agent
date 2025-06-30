import os
import streamlit as st
from typing import TypedDict
from agents import Agent, ModelSettings, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled
from openai import AsyncOpenAI
from duckduckgo_search import DDGS

@function_tool
async def duckduckgo_search(query: str) -> str:
    """Search the web using DuckDuckGo and return a summary of results.

    Args:
        query: The search query string.
    """
    try:
        # Initialize DuckDuckGo search
        ddg = DDGS()
        
        # Get search results (limited to 5 for better performance)
        results = ddg.text(query, max_results=5)
        
        if not results:
            return f"No search results found for '{query}'."
        
        # Format the results
        formatted_results = []
        for i, result in enumerate(results, 1):
            title = result.get('title', 'No title')
            snippet = result.get('body', 'No description available')
            url = result.get('href', '')
            
            formatted_results.append(f"{i}. **{title}**\n   {snippet}\n   URL: {url}\n")
        
        search_summary = f"DuckDuckGo search results for '{query}':\n\n" + "\n".join(formatted_results)
        return search_summary
        
    except Exception as e:
        return f"Error searching DuckDuckGo for '{query}': {str(e)}"

# Settings
token = os.getenv('SECRET')
endpoint = 'https://models.github.ai/inference'
model = 'openai/gpt-4.1-nano'

client = AsyncOpenAI(
    base_url=endpoint,
    api_key=token
)
set_tracing_disabled(True)

model_instance = OpenAIChatCompletionsModel(
    model=model,
    openai_client=client
)

agent = Agent(
    name="SearchAgent",
    instructions="""
    You are an intelligent assistant. 
    When you are unsure about something or lack context, 
    use the `duckduckgo_search` tool to look up accurate and current information.

    Always prioritize accuracy. 
    If a question relates to recent events, current news, or factual lookups, 
    perform a `duckduckgo_search` first unless you're confident in your answer.
    """,
    model=model_instance,
    model_settings=ModelSettings(
        temperature=0.1
    ),
    tools=[duckduckgo_search]
)

st.title("🔍 AI Chatbot with Web Search Agent")

# --- Chat state ---
if "chat" not in st.session_state:
    st.session_state.chat = []

for entry in st.session_state.chat:
    st.chat_message(entry["role"]).markdown(entry["content"])

query = st.chat_input("Ask me anything...")

async def main():
    if query:
        st.chat_message("user").markdown(query)
        st.session_state.chat.append({"role": "user", "content": query})

        # --- Run the agent ---
        response = await Runner.run(agent, query)
    
        st.chat_message("assistant").markdown(response.final_output)
        st.session_state.chat.append({"role": "assistant", "content": response.final_output})


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
