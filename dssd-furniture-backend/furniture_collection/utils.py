from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io
import base64

# Path to the service account credentials JSON file
SERVICE_ACCOUNT_FILE = '/opt/dazzling-matrix-394013-047c78eb7abe.json'

# Define the necessary scopes
SCOPES = ['https://www.googleapis.com/auth/drive']

def upload_file_to_drive(file_data, file_name):
    try:
        creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=creds)
        
        file_metadata = {'name': file_name}
        media = MediaIoBaseUpload(io.BytesIO(file_data), mimetype='application/octet-stream', resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return file.get('id')
    except Exception as e:
        return None  # or handle the error as needed

def get_image_from_drive(file_id):
    # Authenticate with the service account credentials
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # Build the Google Drive v3 API service
    service = build('drive', 'v3', credentials=creds)

    try:
        # Fetch the image content from Google Drive
        image_content = service.files().get_media(fileId=file_id).execute()

        # Convert the binary image content to base64 string
        base64_image = base64.b64encode(image_content).decode('utf-8')

        return base64_image  # Return the base64 encoded image content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None  # Error occurred during image retrieval