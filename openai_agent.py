import os
from typing import TypedDict
from agents import Agent, ModelSettings, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled
from openai import AsyncOpenAI
import httpx

@function_tool
async def duckduckgo_search(query: str) -> str:
    """Search the web using DuckDuckGo and return a summary of results.

    Args:
        query: The search query string.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://duckduckgo.com/html/?q={query}")
        if response.status_code == 200:
            return f"Search results found for '{query}' (HTML length: {len(response.text)} characters)."
        return f"Failed to search DuckDuckGo for '{query}'."

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
