# from langchain_openai import ChatOpenAI
from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserConfig, Controller, BrowserContextConfig
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

config = BrowserContextConfig(
    cookies_file="path/to/cookies.json",
    wait_for_network_idle_page_load_time=3.0,
    window_width=1280,
    window_height=1100,
    locale='en-US',
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    highlight_elements=True,
    viewport_expansion=500,
    allowed_domains=['google.com', 'wikipedia.org'],
)

# Configure the browser to connect to your Chrome instance
browser = Browser(
    config=BrowserConfig(
        browser_binary_path='/usr/bin/google-chrome-stable',
        extra_browser_args=['--user-data-dir=/home/artur/.config/google-chrome']
    )
)

# context = BrowserContext(browser=browser, config=config)

llm = ChatOpenAI(
    model="google/gemini-2.0-flash-exp",
    base_url=requesty_base_url,
    api_key=SecretStr(requesty_api_key) if requesty_api_key else None,
)

async def main():
    initial_actions = [
        {'open_tab': {'url': 'https://x.com'}},
    ]
    agent = Agent(
        task="1. Make post on x.com that says 'hello world' and that this post was made with browser-use",
        llm=llm,
        browser=browser,
        controller=controller,
        initial_actions=initial_actions,
    )
    result = await agent.run()
    print(result)
    await browser.close()

asyncio.run(main())
