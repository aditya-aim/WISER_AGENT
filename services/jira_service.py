import os
from jira import JIRA
from datetime import datetime, timedelta

class JiraService:
    def __init__(self):
        self.jira = JIRA(
            server=os.getenv('JIRA_URL'),
            basic_auth=(os.getenv('JIRA_EMAIL'), os.getenv('JIRA_API_TOKEN'))
        )

    def get_my_issues(self):
        """Get all issues assigned to the current user"""
        jql = f'assignee = currentUser() ORDER BY updated DESC'
        return self.jira.search_issues(jql)

    def get_recent_issues(self, days=7):
        """Get issues updated in the last n days"""
        jql = f'updated >= -{days}d ORDER BY updated DESC'
        return self.jira.search_issues(jql)

    def get_issue_details(self, issue_key):
        """Get detailed information about a specific issue"""
        return self.jira.issue(issue_key)

    def get_my_open_issues(self):
        """Get all open issues assigned to the current user"""
        jql = 'assignee = currentUser() AND status != Done ORDER BY updated DESC'
        return self.jira.search_issues(jql)

    def get_issue_summary(self):
        """Get a summary of issues"""
        open_issues = self.get_my_open_issues()
        recent_issues = self.get_recent_issues()
        
        return {
            'open_issues': len(open_issues),
            'recent_issues': len(recent_issues),
            'issues': [{
                'key': issue.key,
                'summary': issue.fields.summary,
                'status': issue.fields.status.name,
                'updated': issue.fields.updated
            } for issue in open_issues[:5]]  # Return top 5 open issues
        } 