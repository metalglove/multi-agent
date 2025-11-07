# dev_crew.py (Updated for Streamlit UI)
import os
from dotenv import load_dotenv
from crewai import LLM  # For explicit local LLM config

# Load environment variables for LLM configuration
load_dotenv()

# Patch CrewAI color codes to prevent KeyError in Streamlit environment
try:
    from crewai.utilities import printer
    # Add missing color code for 'orange'
    if hasattr(printer, '_COLOR_CODES'):
        if 'orange' not in printer._COLOR_CODES:
            printer._COLOR_CODES['orange'] = '\033[38;5;208m'  # Orange in ANSI
except Exception:
    pass  # If patching fails, continue anyway

# Explicit LLM setup for local LM Studio integration
local_llm = LLM(
    model="openai/qwen/qwen3-4b-2507",  # Adjusted prefix for compatibility
    base_url=os.getenv("OPENAI_API_BASE", "http://localhost:1234/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "not-needed"),
    temperature=0.7
)

from agents import crew

dev_crew.kickoff(inputs={'project_details': project_details})


