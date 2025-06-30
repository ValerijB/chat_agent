# AI Chatbot with DuckDuckGo Web Search Agent

This project is a Streamlit-based AI chatbot that uses an OpenAI-compatible model and integrates a DuckDuckGo web search tool for up-to-date information retrieval.

## Features

- Chat with an AI assistant powered by OpenAI-compatible models.
- If the assistant is unsure or needs current information, it uses DuckDuckGo search.
- Results are summarized and presented in the chat.
- Simple Streamlit web interface.

## Requirements

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [openai](https://pypi.org/project/openai/)
- [duckduckgo-search](https://pypi.org/project/duckduckgo-search/)
- Your own OpenAI-compatible API endpoint and key

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/yourusername/chat_agent.git
   cd chat_agent
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

   Or install individually:

   ```
   pip install streamlit openai duckduckgo-search
   ```

3. Set your API key as an environment variable:

   ```
   set SECRET=your_openai_api_key
   ```

   *(On Linux/macOS use `export SECRET=your_openai_api_key`)*

## Usage

Run the Streamlit app:

```
streamlit run openai_agent.py
```

Open the provided local URL in your browser. Type your questions in the chat input. The assistant will answer and, if needed, search the web for current information.

## File Overview

- `openai_agent.py` — Main Streamlit app and agent logic.

## Notes

- Make sure your OpenAI-compatible endpoint is accessible and supports the model you specify.
- The DuckDuckGo search tool is used as a function tool for the agent.
- Chat history is managed in Streamlit's session state.

## License

MIT License