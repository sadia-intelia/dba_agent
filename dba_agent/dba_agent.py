# from google.adk.agents import Agent
# from datetime import datetime
from tools import check_or_create_employees_index
# import sqlite3
# from google.adk.tools import FunctionTool

from google.genai import Client
import os 


import asyncio

from google.adk.runners import Runner

from google.adk.sessions import InMemorySessionService


from google.genai import types
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.tools import FunctionTool



# This loads the .env file into environment variables
load_dotenv()



# os.environ["GOOGLE_CLOUD_PROJECT"] ="sadia-sandpit"
# os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"
# os.environ["GOOGLE_GENAI_USE_VERTEXAI"]="FALSE"
# os.environ["MODEL"]= "gemini-2.0-flash"
# os.environ["GOOGLE_API_KEY"] = "AIzaSyB290r-QUhzRxanESuVud3I-z2PWyTqB8w"







run_sql_tool = FunctionTool(check_or_create_employees_index)

root_agent = Agent(
        name="dba_agent",
        instruction=(
            "You are a database monitoring assistant. "
            "You check database health, check index."
        ),
        model="gemini-2.0-flash",  # Light LLM
        tools=[run_sql_tool] # Optional custom tools
    )

print(type(root_agent))  # <class 'google.adk.agents.llm_agent.LlmAgent'> — expected



# --- Main function ---




async def call_agent_query():
    sql_query="SELECT * from employees"
    # Set up session service & runner
    session_service = InMemorySessionService()
    # Create session (so session “123” is valid)
    await session_service.create_session(app_name="my_app", user_id="user123", session_id="123")

    runner = Runner(agent=root_agent, app_name="my_app", session_service=session_service)

    content = types.Content(role="user", parts=[types.Part(text=sql_query)])
    async for event in runner.run_async(user_id="user123", session_id="123", new_message=content):
        # Wait for final response
        if getattr(event, "is_final_response", None) and event.is_final_response():
            if event.content and event.content.parts:
                print("Agent final output:", event.content.parts[0].text)
            break



async def start_scheduler():
    """
    Initializes and starts the scheduler to run the agent_task at 9:00 PM daily.
    """
    scheduler = AsyncIOScheduler()
    # Standard way of setting CronTrigger(hour=14, minute=45), for testing - keeping it for one minute
    cron_trigger = CronTrigger(minute='*/1')  
    scheduler.add_job(call_agent_query, trigger=cron_trigger, id="nightly_agent_check", max_instances=1)
    scheduler.start()
    print("Scheduler started. Agent task will run daily at 9:00 PM.")

   # Keep the scheduler running
    await asyncio.Event().wait()

if __name__ == "__main__":

    asyncio.run(start_scheduler())
 

 


 

