# Google Drive Monitor ![gdrive](https://user-images.githubusercontent.com/45032865/219503816-4833a41b-0ae4-450d-8fd6-d073be4b6039.png)


This is a Python-based project designed to monitor Google Drive. The script is programmed to track the user's drive and, upon detecting the presence of new files, determine whether or not they are publicly accessible. In the event that a new file permissions is publicly accessible, the script will proceed to adjust the file's permission settings to "private". As the script checks each file, it produce an output detailing the sharing status of the file, as well as whether or not it has been altered by the program.

## Setup

There are a few setup steps you need to complete before you can use this library:

1. If you don't already have a Google account, sign up.
2. If you have never created a Google APIs Console project, read the Google Cloud Managing Projects page and create a project in the   Google API Console. https://developers.google.com/drive/api/guides/enable-drive-api
3. Clone the repository.
4. Create a virtual environment.
5. Install the required packages using pip. (pip install -r requirements.txt)
6. Modify the following fields in the script if needed SCOPES, TOKEN_FILE, CREDENTIALS_FILE, FOLDER_ID 

```
# Set the ID of the folder to monitor (Optional)
FOLDER_ID = 'FOLDER_ID_HERE'

# Set the path of the credentials file you downloaded from the Google Cloud Console
CREDENTIALS_FILE = 'credentials.json'

# Set the path of the token file to store your access and refresh tokens
TOKEN_FILE = 'token.json'

# Set the scope of the API request
SCOPES = ['https://www.googleapis.com/auth/drive']

# Set time interval for API calls to check for new files(In Seconds)
TIME = 60
```
6. Run the project.
7. Once executed you will be prompt to allow the program to access your gdrive.
![image](https://user-images.githubusercontent.com/45032865/219655807-9911c44e-995e-4850-b198-b85a2404dcce.png)


Press continue in order to use the program.
 Enjoy!

## Unsupported Python Versions
Python < 3.7

## Usage

To use the project, run the following command:
```
python google_drive_Monitor.py
```

Sample outputs:
```
Default sharing settings: {'id': '*****************', 'type': 'user', 'kind': 'drive#permission', 'role': 'owner'}
2023-02-17T13:13:18.926357Z No new files detected.
2023-02-17T13:14:38.291088Z New file detected: ccc.txt
Filename: ccc.txt (1ZOa5GLfZtWXJl18AyzMRJz5tqbijefpo) permissions is anyone
Filename: ccc.txt (1ZOa5GLfZtWXJl18AyzMRJz5tqbijefpo) permissions changed to private.
2023-02-17T13:14:54.595369Z New file detected: qw.txt
Filename: qw.txt (18kmzEOSh3DfhRSGYm2DNfACTDuIWb_Xx) permissions is user
```

```
2023-02-17T13:37:18.284846Z No new files detected.
Waiting 60 Seconds
2023-02-17T13:38:18.643492Z No new files detected.
Waiting 60 Seconds
2023-02-17T13:39:19.014467Z No new files detected.
Waiting 60 Seconds
```
## Retrieve/Set the general sharing access default option for new items
By default, general access is set to Restricted. This is the recommended setting for most users, so they can share a file only when they’re ready and keep personal files private.
Changing it available only for company editions: Business Standard and Business Plus; Enterprise; Education Standard and Education Plus; G Suite Business; Nonprofits.

## Interesting attack surfaces

While working with the google drive API few attack methods came to my mind:
1. Authentication - The Google Drive API uses OAuth 2.0 for authorization, which allows users to grant third-party applications access to their Google Drive data. If a malicious actor is able to steal a user's access token, they can gain access to the user's Google Drive data and basically use it for any attack (Ransom, Sell PII online, etc).
2. Public File permissions - Anyone with access to the link can view and download the file. If the file contains sensitive information or is not intended for public consumption, it could end up in the wrong hands.




