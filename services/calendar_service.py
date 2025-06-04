import os
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import streamlit as st

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class CalendarService:
    def __init__(self):
        self.creds = None
        self.service = None
        self._authenticate()

    def _authenticate(self):
        """Handle Google Calendar authentication"""
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        os.getenv('GOOGLE_CREDENTIALS_FILE'), SCOPES)
                    # Use Streamlit's built-in OAuth flow
                    self.creds = flow.run_local_server(
                        port=0,
                        prompt='consent',
                        authorization_prompt_message='Please authorize the application to access your Google Calendar.'
                    )
                except Exception as e:
                    st.error(f"Authentication failed: {str(e)}")
                    st.info("Please make sure you have added the correct redirect URIs in Google Cloud Console:")
                    st.code("""
                    http://localhost:8501
                    http://localhost:52376
                    http://127.0.0.1:8501
                    http://127.0.0.1:52376
                    """)
                    return
            
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        if self.creds:
            self.service = build('calendar', 'v3', credentials=self.creds)

    def get_upcoming_events(self, days=7):
        """Get upcoming events for the next n days"""
        if not self.service:
            return []
            
        now = datetime.utcnow().isoformat() + 'Z'
        end = (datetime.utcnow() + timedelta(days=days)).isoformat() + 'Z'
        
        try:
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=now,
                timeMax=end,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            return events_result.get('items', [])
        except Exception as e:
            st.error(f"Failed to fetch calendar events: {str(e)}")
            return []

    def get_today_events(self):
        """Get events for today"""
        if not self.service:
            return []
            
        now = datetime.utcnow()
        start_of_day = datetime(now.year, now.month, now.day).isoformat() + 'Z'
        end_of_day = (datetime(now.year, now.month, now.day) + timedelta(days=1)).isoformat() + 'Z'
        
        try:
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=start_of_day,
                timeMax=end_of_day,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            return events_result.get('items', [])
        except Exception as e:
            st.error(f"Failed to fetch today's events: {str(e)}")
            return []

    def get_calendar_summary(self):
        """Get a summary of calendar events"""
        if not self.service:
            return {
                'today_events': 0,
                'upcoming_events': 0,
                'events': []
            }
            
        today_events = self.get_today_events()
        upcoming_events = self.get_upcoming_events()
        
        return {
            'today_events': len(today_events),
            'upcoming_events': len(upcoming_events),
            'events': [{
                'summary': event['summary'],
                'start': event['start'].get('dateTime', event['start'].get('date')),
                'end': event['end'].get('dateTime', event['end'].get('date'))
            } for event in today_events]
        } 