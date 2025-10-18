# from google.adk.agents import Agent
# from datetime import datetime
from dba_agent.tools import check_or_create_employees_index
# import sqlite3
# from google.adk.tools import FunctionTool


import os 

from contextlib import aclosing
import asyncio

from google.adk.runners import Runner

from google.adk.sessions import InMemorySessionService


from google.genai import types
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.agents import ParallelAgent, SequentialAgent
from google.adk.tools import FunctionTool
from google.genai import Client
from dotenv import load_dotenv
import os


from dba_agent.sub_agents.synthesizer_agent import create_system_report_synthesizer
# Correct imports in your main file (like dba_agent.py)

from dba_agent.sub_agents.index_checking_agent.agent import create_index_checking_agent
from dba_agent.sub_agents.db_info_agent.agent import create_db_info_agent


# This loads the .env file into environment variables
load_dotenv()



GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")
GOOGLE_GENAI_USE_VERTEXAI = os.getenv("GOOGLE_GENAI_USE_VERTEXAI")
MODEL = os.getenv("MODEL")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


genaiclient = Client(vertexai=True, project="sadia-sandpit", location="us-central1")




#run_sql_tool = FunctionTool(check_or_create_employees_index)

db_info_gatherer = ParallelAgent(
    name="db_info_gatherer",
    sub_agents=[ create_index_checking_agent(),
        create_db_info_agent(),])

# --- 2. Create Sequential Pipeline to gather info in parallel, then synthesize ---
root_agent = SequentialAgent(
    name="system_monitor_agent",
    sub_agents=[db_info_gatherer, create_system_report_synthesizer()],
)
# root_agent = Agent(
#         name="dba_agent",
#         instruction=(
#             "You are a database monitoring assistant. "
#             "You check database health, check index."
#         ),
#         model="gemini-2.0-flash",  # Light LLM
#         tools=[run_sql_tool] # Optional custom tools
#     )

print(type(root_agent))  # <class 'google.adk.agents.llm_agent.LlmAgent'> — expected



# --- Main function ---



async def call_agent_query(user_input):
    # Setup session and runner
    session_service = InMemorySessionService()
    await session_service.create_session(app_name="my_app", user_id="user123", session_id="123")

    runner = Runner(agent=root_agent, app_name="my_app", session_service=session_service)

    content = types.Content(role="user", parts=[types.Part(text=user_input)])
    full_response = {}

    try:
        async with aclosing(runner.run_async(user_id="user123", session_id="123", new_message=content)) as agen:
            async for event in agen:
                if event.content and event.content.parts:
                        for part in event.content.parts:
                            if hasattr(part, "function_response") and part.function_response:
                                fr = part.function_response
                                print(f"Function `{fr.name}` responded with: {fr.response}")
                                full_response[fr.name] = fr.response
                            elif hasattr(part, "text"):
                                print("Text output:", part.text)
                                #full_response.setdefault("text_parts", []).append(part.text)

            
        
                if getattr(event, "is_final_response", None) and event.is_final_response():                  
                    break
        
    except GeneratorExit:
        # Suppress GeneratorExit from TaskGroup cleanup
        pass

    except Exception as e:
        print("Error running agent:", e)

    finally:
        return full_response



async def scheduled_job():
    try:
        output = await call_agent_query("Show employees indexes")
        print("Agent output:", output)
    except Exception as e:
        print("Scheduled job error:", repr(e))


async def start_scheduler():
    """
    Initializes and starts the scheduler to run the agent_task at 9:00 PM daily.
    """
    scheduler = AsyncIOScheduler()
    # Standard way of setting CronTrigger(hour=14, minute=45), for testing - keeping it for one minute
    cron_trigger = CronTrigger(minute='*/1')  
    scheduler.add_job(scheduled_job, trigger=cron_trigger, id="nightly_agent_check", max_instances=1)
    scheduler.start()
    print("Scheduler started. Agent task will run daily at 2:00 PM.")

   # Keep the scheduler running
    await asyncio.Event().wait()

if __name__ == "__main__":

    asyncio.run(start_scheduler())
 

 


 

