# call-transcription

Transcription of CS calls using AWS Transcribe

## Running transcribe_folder.sh

Parameters:

-   Edit `transcribe_folder.sh` script to include correct variables/parameters to the variables needed

Run the Script:

-   Open Git Bash (Requires Git to be installed)
-   Navigate to the directory containing your transcribe_folder.sh script
    -   Alternatively: Navigate to directory, and right click and click `Open Git Bash Here`
-   Make the script executable (if necessary) with `chmod +x transcribe_folder.sh`
-   Run the script with `./transcribe_folder.sh`

Process the transcription json files into human readable text:

-   Transfer JSON files to `transcriptions` folder
-   Use `python src/process_transcriptions.py transcriptions processed-transcriptions`
    -   Alternatively, `npm run process-transcriptions`
-   Results will be output into `processed-transcriptions` folder
