import os
from openai import OpenAI
from datetime import datetime

class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def process_query(self, query, jira_service, github_service, calendar_service):
        """Process a natural language query using LLM"""
        # Gather context from different services
        jira_summary = jira_service.get_issue_summary()
        github_summary = github_service.get_activity_summary()
        calendar_summary = calendar_service.get_calendar_summary()

        # Create a prompt with context
        prompt = f"""
        You are a helpful work assistant. Use the following information to answer the user's query:

        Jira Status:
        - Open Issues: {jira_summary['open_issues']}
        - Recent Issues: {jira_summary['recent_issues']}
        - Top Open Issues: {jira_summary['issues']}

        GitHub Activity:
        - Recent Commits: {github_summary['recent_commits']}
        - Open PRs: {github_summary['open_prs']}
        - Recent Commits: {github_summary['commits']}
        - Open PRs: {github_summary['pull_requests']}

        Calendar:
        - Today's Events: {calendar_summary['today_events']}
        - Upcoming Events: {calendar_summary['upcoming_events']}
        - Today's Schedule: {calendar_summary['events']}

        User Query: {query}

        Please provide a helpful response based on this information. Be concise but informative.
        """

        # Get response from OpenAI
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful work assistant that provides concise and informative responses about work-related queries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )

        return response.choices[0].message.content 