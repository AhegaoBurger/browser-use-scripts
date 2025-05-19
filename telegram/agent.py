# from langchain_openai import ChatOpenAI
from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserConfig, Controller
from pydantic import BaseModel, SecretStr
from os import getenv, environ
# from dotenv import load_dotenv
# load_dotenv()

import asyncio

# Set the OpenAI API key and base URL environment variables
requesty_api_key = getenv("REQUESTY_API_KEY")
requesty_base_url = getenv("REQUESTY_BASE_URL")

if requesty_api_key is not None:
    environ["OPENAI_API_KEY"] = requesty_api_key
    print(f"Using OpenAI API key from environment variable: {requesty_api_key}")


if requesty_base_url is not None:
    environ["OPENAI_BASE_URL"] = requesty_base_url
    print(f"Using OpenAI API base URL from environment variable: {requesty_base_url}")

class QueueInfo(BaseModel):
    queue_number: str
    available: bool

controller = Controller(output_model=QueueInfo)

# Configure the browser to connect to your Chrome instance
browser = Browser(
    config=BrowserConfig(
        browser_binary_path='/usr/bin/google-chrome-stable',
    )
)

llm = ChatOpenAI(
    model="google/gemini-2.5-pro-preview-03-25",
    base_url=requesty_base_url,
    api_key=SecretStr(requesty_api_key) if requesty_api_key else None,
)

async def main():
    initial_actions = [
        {'open_tab': {'url': 'https://web.telegram.org/a'}},
    ]
    agent = Agent(
        task="1. Search for AI, whatever (its the name of the group/chat). 2. Enter the group/chat. 3. Send a message in the group saying you are an AI agent built by Artur and add a funny AI related joke at the end.",
        llm=llm,
        browser=browser,
        controller=controller,
        initial_actions=initial_actions,
    )
    result = await agent.run()
    print(result)
    # await browser.close()

asyncio.run(main())
