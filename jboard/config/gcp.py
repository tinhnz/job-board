import io
import os

from dotenv import load_dotenv
from google.cloud import secretmanager

# Pull secrets from Secret Manager
project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
settings_name = os.environ.get("SETTINGS_NAME", "jb_settings")
name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
client = secretmanager.SecretManagerServiceClient()
payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")

load_dotenv(stream=io.StringIO(payload))

SECRET_KEY = os.getenv('SECRET_KEY')

DATABASE_URI = 'dbname={dbname} user={dbuser} password={dbpass} host={dbhost}'.format(
    dbname=os.environ.get('DBNAME'),
    dbuser=os.environ.get('DBUSER'),
    dbpass=os.environ.get('DBPASS'),
    dbhost=os.environ.get('DBHOST'),
)