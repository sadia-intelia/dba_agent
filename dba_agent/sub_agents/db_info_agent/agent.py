from google.adk.agents import LlmAgent
from .tools import check_database_lock

GEMINI_MODEL = "gemini-2.0-flash"

def create_db_info_agent():
    return LlmAgent(
        name="DBInfoAgent",
        model=GEMINI_MODEL,
        instruction="""
        You are a DBA Information Agent.

        When asked for system information, you should:
        1. Use the 'check_database_lock' tool.
        2. Throw an error if needed.

        The tool will return a dictionary with:
        - result: Database information
        - stats: If the database is locked
        - additional_info: Context about the data collection

        IMPORTANT: You MUST call the check_database_lock tool. Do not make up information.
        """,
        description="Gathers database information",
        tools=[check_database_lock],
        output_key="db_lock_info",
    )
