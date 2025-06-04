import streamlit as st
import os
from dotenv import load_dotenv
from services.jira_service import JiraService
from services.github_service import GitHubService
from services.calendar_service import CalendarService
from services.llm_service import LLMService
from utils.helpers import format_response

# Load environment variables
load_dotenv()

# Initialize services
jira_service = JiraService()
github_service = GitHubService()
calendar_service = CalendarService()
llm_service = LLMService()

# Set page config
st.set_page_config(
    page_title="Work Assistant",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

def main():
    st.title("🤖 Work Assistant")
    st.markdown("""
    Your AI-powered work assistant that helps you manage your tasks across Jira, GitHub, and Google Calendar.
    Ask me anything about your work!
    """)

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Process the query using LLM
                response = llm_service.process_query(
                    prompt,
                    jira_service,
                    github_service,
                    calendar_service
                )
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main() 