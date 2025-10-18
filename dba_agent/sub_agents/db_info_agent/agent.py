"""
DB Lock Information Agent

This agent is responsible for checking database/table locked and generate alert
"""

from google.adk.agents import LlmAgent

from .tools import check_database_lock

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# CPU Information Agent
db_info_agent = LlmAgent(
    name="DBInfoAgent",
    model=GEMINI_MODEL,
    instruction="""You are a DBA Information Agent.
    
    When asked for system information, you should:
    1. Use the 'check_database_lock' 
    2.Throw error
    
    The tool will return a dictionary with:
    - result:Database information
    - stats: If the database is locked
    - additional_info: Context about the data collection
    
 
    IMPORTANT: You MUST call the get_cpu_info tool. Do not make up information.
    """,
    description="Gathers database information",
    tools=[check_database_lock],
    output_key="db_lock_info",
)