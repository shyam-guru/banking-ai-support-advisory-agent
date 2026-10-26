"""
Application configuration.

This module loads environment variables and provides
central configuration for the Banking AI Agent.
"""

import os
from dotenv import load_dotenv


# Load variables from .env
load_dotenv()


# ---------------------------------------------------------
# OpenAI configuration
# ---------------------------------------------------------

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Controls whether the application actually calls OpenAI.
# false = use Mock LLM during development
# true  = use OpenAI when API credits are available
OPENAI_ENABLED = os.getenv("OPENAI_ENABLED", "false").lower() == "true"


# OpenAI model to be used later.
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


# ---------------------------------------------------------
# Application configuration
# ---------------------------------------------------------

APP_NAME = "Banking AI Support & Advisory Agent"

APP_VERSION = "0.1.0"


# ---------------------------------------------------------
# Validation
# ---------------------------------------------------------

def validate_openai_configuration():
    """
    Validate OpenAI configuration only when OpenAI
    integration is enabled.

    This allows the project to run in Mock mode without
    requiring an active OpenAI API connection.
    """

    if OPENAI_ENABLED and not OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_ENABLED=true but OPENAI_API_KEY was not found."
        )