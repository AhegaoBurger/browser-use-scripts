# from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from browser_use import Agent, Browser, BrowserConfig, Controller
from pydantic import BaseModel
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

# llm = ChatOpenAI(model="gpt-4o")
llm = ChatGroq(
    # model="llama-3.3-70b-versatile", # Works
    # model="llama3-70b-8192", # Also works but can handle less
    # model="gemma2-9b-it", # Works, but encountered issue while web searching, not sure what happened
    model="llama-3.1-8b-instant", # Can handle the workflow
    temperature=0,
    max_tokens=None,
    timeout=None,
    # other params...
)

async def main():
    initial_actions = [
        {'open_tab': {'url': 'https://lisboa.kdmid.ru/queue'}},
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
