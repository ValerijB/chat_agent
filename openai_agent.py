import os
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
    instructions="You are a helpful assistant that can search the web using DuckDuckGo.",
    model=model_instance,
    model_settings=ModelSettings(
        temperature=0.1
    ),
    tools=[duckduckgo_search]
)

async def main():
    result = await Runner.run(agent, "How many churches in Vilnius? Please search DuckDuckGo.")
    print(result.final_output)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
