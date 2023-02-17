#!/usr/bin/env python
"""
Author: Bar Franko
Email: barfranko2@gmail.com
Date: Feb 16. 2023
"""

import os
import time
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set the ID of the folder to monitor (Optional), Default - all files and folders
FOLDER_ID = 'FOLDER_ID_HERE'

# Set the path of the credentials file you downloaded from the Google Cloud Console
CREDENTIALS_FILE = 'credentials.json'

# Set the path of the token file to store your access and refresh tokens
TOKEN_FILE = 'token.json'

# Set the scope of the API request
SCOPES = ['https://www.googleapis.com/auth/drive']

# Set time interval for API calls to check for new files(In Seconds)
TIME = 60

def get_service():
    """
    Set up the credentials object and authenticate to the drive api service
    """
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Refresh an expired access token
            creds.refresh(Request())
        else:
            # Authenticate the user with OAuth 2.0
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

def get_new_files(service):
    """
    Check Google drive for newly created files and collect them
    """
    try:
        minutes_back = 120+(TIME/60) # Set how many minutes to trace back depends on the main function sleep (default time zone is UTC)
        delta = datetime.datetime.now() - datetime.timedelta(minutes=minutes_back)
        delta_str = delta.isoformat() + 'Z'
        # Query the drive api for new created files for the past X minutes set
        results = service.files().list(q=f"createdTime > '{delta_str}'", fields='files(id, name)').execute()
        items = results.get('files', [])
        return items
    except HttpError as error:
        print('An error occurred: %s' % error)
        return None

def retrieve_default_sharing(service):
    """
    Get the default sharing settings of files in the google account and print it
    """
    try:
        # Call the about.get method to get information about the user's Google Drive account
        about = service.about().get(fields='user').execute()
        permission_id = about['user']['permissionId']
        # Get the permissions for the default role
        permissions = service.permissions().list(fileId='root',).execute()
        default_permission = None
        for permission in permissions['permissions']:
            if permission['id'] == permission_id:
                default_permission = permission
                break
        if default_permission:
            print('Default sharing settings:', default_permission)
        else:
            print('No default sharing settings found.')
    except HttpError as error:
        print(f'An error occurred: {error}')

def check_public_file(file_id, service):
    """
    Check if a file is publicly accessible, if so print it and change the permissions to private
    """
    try:
        file = service.files().get(fileId=file_id, fields='permissions(kind, id, emailAddress, role, type),id, name, webViewLink').execute()
        sharing_settings = file['permissions'][0]['type']
        print(f'Filename: {file["name"]} ({file["id"]}) permissions is {sharing_settings}')
        if sharing_settings == 'anyone':
            # Change file permissions to private
            try:
                permission_id = file['permissions'][0]['id']
                service.permissions().delete(fileId=file_id, permissionId=permission_id).execute()
                print(f'Filename: {file["name"]} ({file["id"]}) permissions changed to private.')
            except HttpError as error:
                print(f'An error occurred: {error}')
    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    service = get_service()
    retrieve_default_sharing(service)
    while True:
        new_files = get_new_files(service)
        if new_files:
            for file in new_files:
                tnow = datetime.datetime.now()
                tnow_str = tnow.isoformat() + 'Z'
                print(f'{tnow_str} New file detected: {file["name"]}')
                check_public_file(file['id'], service)
        else:
            tnow = datetime.datetime.now()
            tnow_str = tnow.isoformat() + 'Z'
            print(f"{tnow_str} No new files detected.")
        # Wait for 60 seconds before checking for new files again
        print(f'Waiting {TIME} Seconds')
        time.sleep(TIME)