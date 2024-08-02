# call-transcription

Transcription of CS calls using AWS Transcribe

## Running transcribe_folder.sh

Parameters:

-   Edit script to include correct parameters to the variables needed

Run the Script:

-   Open Git Bash
-   Navigate to the directory containing your transcribe_folder.sh script
-   Make the script executable (if necessary) with `chmod +x transcribe_folder.sh`
-   Run the script with `./transcribe_folder.sh`

Process the transcription json files:

-   use `python src/process_transcriptions.py transcriptions processed-transcriptions`
-   alternatively, `npm run process-transcriptions`
