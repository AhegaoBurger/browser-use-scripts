# from langchain_openai import ChatOpenAI
from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserConfig, Controller
from pydantic import BaseModel
from os import getenv
from dotenv import load_dotenv
load_dotenv()

import asyncio

class QueueInfo(BaseModel):
    queue_number: str
    available: bool

controller = Controller(output_model=QueueInfo)

# Configure the browser to connect to your Chrome instance
browser = Browser(
    config=BrowserConfig(
        # Specify the path to your Chrome executable
        browser_binary_path='/usr/bin/google-chrome',
        # For Windows, typically: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
        # For Linux, typically: '/usr/bin/google-chrome'
    )
)

llm = ChatOpenAI(
    openai_api_key=getenv("REQUESTY_API_KEY"),
    openai_api_base=getenv("REQUESTY_BASE_URL"),
    model_name="openai/gpt-4o",
)

async def main():
    initial_actions = [
        {'open_tab': {'url': 'https://lisboa.kdmid.ru/queue/orderinfo.aspx?id=79571&cd=19a9bb7a&ems=9A884FFA'}},
    ]
    agent = Agent(
        task="1. Perform the capthca. 2. Press the Sign up for an appointment button. 3. Get my queue number.",
        llm=llm,
        browser=browser,
        controller=controller,
        initial_actions=initial_actions,
    )
    result = await agent.run()
    print(result)
    await browser.close()

asyncio.run(main())
