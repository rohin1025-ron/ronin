from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import mimetypes

def upload_to_drive(file_path, drive_folder_id=None):
    credentials = service_account.Credentials.from_service_account_file(
        "client_secrets.json",  # 🔐 Put your key file here
        scopes=["https://www.googleapis.com/auth/drive.file"],
    )
    service = build("drive", "v3", credentials=credentials)

    file_metadata = {"name": file_path.split("/")[-1]}
    if drive_folder_id:
        file_metadata["parents"] = [drive_folder_id]

    media = MediaFileUpload(file_path, mimetype=mimetypes.guess_type(file_path)[0])
    file = service.files().create(
        body=file_metadata, media_body=media, fields="id, webViewLink"
    ).execute()

    print("✅ Uploaded to Google Drive:", file.get("webViewLink"))
    return file.get("webViewLink")
