import os
import json
import boto3
import pymongo
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration from .env
MONGO_USERNAME = os.getenv('MONGO_USERNAME')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')

# Configuration
MONGO_CLUSTER = 'cscalltranscript.w192w6d.mongodb.net'
DATABASE_NAME = 'transcript-json-db'
MONGO_URI = f'mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_CLUSTER}/{DATABASE_NAME}?retryWrites=true&w=majority'
COLLECTION_NAME = 'transcript-collection'
S3_PREFIX_FOLDER = 'transcription-jan-2024' # path to s3 folder
S3_BUCKET = 'cs-calls-transcription'
LOCAL_DOWNLOAD_DIR = 'transcriptions' # folder to temporarily store downloaded files

# Initialize MongoDB client
client = pymongo.MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Initialize S3 client
s3 = boto3.client('s3')

def download_files_from_s3(bucket_name, prefix, local_dir):
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

    for page in pages:
        for obj in page.get('Contents', []):
            key = obj['Key']
            local_file_path = os.path.join(local_dir, os.path.basename(key))

             # Ensure the local file path directory exists
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
            
             # Logging for debugging
            print(f"Attempting to download {key} to {local_file_path}")
            try:
                s3.download_file(bucket_name, key, local_file_path)
                print(f"Downloaded {key} to {local_file_path}")
            except Exception as e:
                print(f"Failed to download {key} to {local_file_path}. Error: {e}")

def upload_files_to_mongodb(local_dir, collection):
    for filename in os.listdir(local_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(local_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                data = file.read()
                json_data = json.loads(data)
                collection.insert_one(json_data)
                print(f'Uploaded {filename} to MongoDB')

# Ensure local directory exists
print("Attempting to make local directory")
os.makedirs(LOCAL_DOWNLOAD_DIR, exist_ok=True)

# Download files from S3
print("Attempting to download S3 files")
download_files_from_s3(S3_BUCKET, S3_PREFIX_FOLDER, LOCAL_DOWNLOAD_DIR)

# Check MongoDB connection
print("Checking MongoDB connection")
try:
    client.admin.command('ping')
    print("MongoDB connection successful")
except pymongo.errors.ServerSelectionTimeoutError as err:
    print(f"MongoDB connection failed: {err}")

# Upload files to MongoDB
print("Attempting to upload to MongoDB")
upload_files_to_mongodb(LOCAL_DOWNLOAD_DIR, collection)

print("All JSON files have been uploaded to MongoDB.")
