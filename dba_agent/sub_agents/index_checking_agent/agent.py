"""
DB Lock Information Agent

This agent is responsible for checking database/table locked and generate alert
"""

from google.adk.agents import LlmAgent

from .tools import check_or_create_employees_index

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"


def create_index_checking_agent():
    return LlmAgent(
        name="index_checking_agent",
        model=GEMINI_MODEL,
        instruction="""
            You are a DBA Information Agent.
            You check database health, check index.
        """,
        description="Check employee index",
        tools=[check_or_create_employees_index],
        output_key="index_info",
    )
