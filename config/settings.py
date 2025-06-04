import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys and Credentials
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
JIRA_URL = os.getenv('JIRA_URL')
JIRA_EMAIL = os.getenv('JIRA_EMAIL')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
GOOGLE_CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS_FILE')

# Application Settings
APP_NAME = "Work Assistant"
APP_VERSION = "1.0.0"
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# LLM Settings
LLM_MODEL = "gpt-3.5-turbo"
MAX_TOKENS = 500
TEMPERATURE = 0.7

# Time Settings
DEFAULT_DAYS_LOOKBACK = 7 