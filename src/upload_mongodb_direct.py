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
S3_PREFIX_FOLDER = 'transcription-feb-2024' # path to s3 folder
S3_BUCKET = 'cs-calls-transcription'

# Initialize MongoDB client
client = pymongo.MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Initialize S3 client
s3 = boto3.client('s3')

def upload_files_from_s3_to_mongodb(bucket_name, prefix, collection):
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

    for page in pages:
        for obj in page.get('Contents', []):
            key = obj['Key']
            if key.endswith('.json'):
                # Logging for debugging
                print(f"Attempting to read {key} from S3")
                try:
                    obj = s3.get_object(Bucket=bucket_name, Key=key)
                    data = obj['Body'].read().decode('utf-8')
                    json_data = json.loads(data)
                    collection.insert_one(json_data)
                    print(f"Uploaded {key} to MongoDB")
                except Exception as e:
                    print(f"Failed to read {key} from S3 or upload to MongoDB. Error: {e}")

# Check MongoDB connection
print("Checking MongoDB connection")
try:
    client.admin.command('ping')
    print("MongoDB connection successful")
except pymongo.errors.ServerSelectionTimeoutError as err:
    print(f"MongoDB connection failed: {err}")

# Upload files from S3 to MongoDB
print("Attempting to upload to MongoDB directly from S3")
upload_files_from_s3_to_mongodb(S3_BUCKET, S3_PREFIX_FOLDER, collection)

print("All JSON files have been uploaded to MongoDB.")
