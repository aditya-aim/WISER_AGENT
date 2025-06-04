import os
from github import Github
from datetime import datetime, timedelta

class GitHubService:
    def __init__(self):
        self.github = Github(os.getenv('GITHUB_TOKEN'))
        self.user = self.github.get_user()

    def get_my_repositories(self):
        """Get all repositories for the current user"""
        return self.user.get_repos()

    def get_recent_commits(self, days=7):
        """Get recent commits across all repositories"""
        since = datetime.now() - timedelta(days=days)
        commits = []
        
        for repo in self.get_my_repositories():
            try:
                for commit in repo.get_commits(since=since):
                    if commit.author and commit.author.login == self.user.login:
                        commits.append({
                            'repo': repo.name,
                            'sha': commit.sha,
                            'message': commit.commit.message,
                            'date': commit.commit.author.date
                        })
            except Exception:
                continue
                
        return sorted(commits, key=lambda x: x['date'], reverse=True)

    def get_open_pull_requests(self):
        """Get open pull requests across all repositories"""
        prs = []
        for repo in self.get_my_repositories():
            try:
                for pr in repo.get_pulls(state='open'):
                    if pr.user.login == self.user.login:
                        prs.append({
                            'repo': repo.name,
                            'number': pr.number,
                            'title': pr.title,
                            'state': pr.state,
                            'created_at': pr.created_at
                        })
            except Exception:
                continue
        return prs

    def get_activity_summary(self):
        """Get a summary of GitHub activity"""
        recent_commits = self.get_recent_commits()
        open_prs = self.get_open_pull_requests()
        
        return {
            'recent_commits': len(recent_commits),
            'open_prs': len(open_prs),
            'commits': recent_commits[:5],  # Return top 5 recent commits
            'pull_requests': open_prs[:5]   # Return top 5 open PRs
        } 