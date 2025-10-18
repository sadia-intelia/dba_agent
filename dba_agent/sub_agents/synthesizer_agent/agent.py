"""
Database Health Agent

This agent is responsible for synthesizing information from other agents
to create a comprehensive system health report.
"""

from google.adk.agents import LlmAgent

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

def create_system_report_synthesizer():
    return LlmAgent(
         name="DatabaseReportSynthesizer",
    model=GEMINI_MODEL,
    instruction="""You are a Database Report Synthesizer.
    
    Your task is to create a comprehensive system health report by combining information from:
    - index check agent information : {index_info}
    - db_info_agent information: {db_lock_info}
    
    generate report from both output {index_info} and {db_lock_info}
    
   
    Use markdown formatting to make the report readable and professional.
    Highlight any concerning values and provide practical recommendations.
    """,
    description="Synthesizes all system information into a comprehensive report",
    )
# System Report Synthesizer Agent
# system_report_synthesizer = LlmAgent(
#     name="DatabaseReportSynthesizer",
#     model=GEMINI_MODEL,
#     instruction="""You are a Database Report Synthesizer.
    
#     Your task is to create a comprehensive system health report by combining information from:
#     - index check agent information : {index_info}
#     - db_info_agent information: {db_lock_info}
    
#     generate report from both output {index_info} and {db_lock_info}
    
   
#     Use markdown formatting to make the report readable and professional.
#     Highlight any concerning values and provide practical recommendations.
#     """,
#     description="Synthesizes all system information into a comprehensive report",
# )