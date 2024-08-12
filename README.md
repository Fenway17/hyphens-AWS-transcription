# call-transcription

Transcription of CS calls using AWS Transcribe

## Running transcribe_folder.sh to transcribe audio files

Parameters:

-   Edit `transcribe_folder.sh` script to include correct variables/parameters to the variables needed

Before running script:

-   Ensure AWS is configured with correct logins
    -   Requires AWS CLI
    -   Use Command Prompt to access AWS through AWS CLI and login with `AWS Access Key ID` and `Secret`

Run the Script:

-   Open Git Bash (Requires Git to be installed)
-   Navigate to the directory containing your transcribe_folder.sh script
    -   Alternatively: Navigate to directory, and right click and click `Open Git Bash Here`
-   Make the script executable (if necessary) with `chmod +x transcribe_folder.sh`
-   Run the script with `./transcribe_folder.sh`

## Process the transcription json files into human readable text

-   Partial instructions in `INSTRUCTIONS.txt`
-   Transfer JSON files to `transcriptions` folder
-   Use `python src/process_transcriptions.py transcriptions processed-transcriptions`
    -   Alternatively, `npm run process-transcriptions`
-   Results will be output into `processed-transcriptions` folder

## Upload transcription JSON files to MongoDB

Parameters:

-   Edit `upload_mongodb_direct.py` script to include correct variables/parameters to the variables needed
-   Edit `upload_mongodb.py` script to include correct variables/parameters to the variables needed

Before uploading the JSON files to MongoDB:

-   Requires your IP address to be whitelisted on MongoDB's network access
-   Requires `.env` file to contain MongoDB username and password
    -   Created in MongoDB

Uploading the JSON files to MongoDB:

-   Set up virtual environment with `python -m venv venv`
-   Activate virtual environment with `.\venv\Scripts\activate`
    -   Use `pip freeze > requirements.txt` to update `requirements.txt` if any new libraries are installed
-   Install required libraries with `pip install -r requirements.txt`
-   Run either one of the Python scripts:
    -   Run the script `python src/upload_mongodb_direct.py` to upload from S3 bucket to MongoDB directly
        -   Alternatively, `npm run upload-mongodb-direct`
    -   Run the script `python src/upload_mongodb.py` to download from S3 before uploading to MongoDB
        -   Alternatively, `npm run upload-mongodb`
