#!/bin/bash

# Configuration
BUCKET_NAME="cs-calls-audio"
AUDIO_FOLDER="rawcalls-feb2024/2024-08-06T03_30_10.877Z"
OUTPUT_BUCKET="cs-calls-transcription"
OUTPUT_FOLDER="transcription-feb-2024"
LANGUAGE_OPTIONS=("en-US" "zh-CN" "ms-MY")
JOB_NAME_PREFIX="call-transcription-job-"
# Currently unable to use this custom vocab as it is tied to english only
CUSTOM_VOCABULARY_NAME="PharmaceuticalTerms"
SPEAKER_SEPARATION=true
MAX_SPEAKERS=2  # Set the number of speakers

# List all audio files in the S3 bucket folder
FILES=$(aws s3 ls s3://$BUCKET_NAME/$AUDIO_FOLDER/ --recursive | awk '{print $4}')

# Function to check if the corresponding output file already exists
function output_file_exists {
  local file_path=$1
  local output_file_path=""
  local base_file_name="${JOB_NAME_PREFIX}$(basename "${file_path}")"

  if [[ $base_file_name == *.wav || $base_file_name == *.mp3 || $base_file_name == *.flac ]]; then
    output_file_path=${base_file_name}.json
  else
    echo "Unsupported file extension for file $base_file_name."
    return 1 # Unsupported file extension
  fi

  output_file_path="$OUTPUT_FOLDER/$output_file_path"
  local existing_output=$(aws s3 ls s3://$OUTPUT_BUCKET/$output_file_path)
  echo "Searching for file at: $output_file_path"
  
  if [ -n "$existing_output" ]; then
    return 0 # Output file exists
  else
    return 1 # Output file does not exist
  fi
}

# Iterate over each file and start a transcription job
for FILE in $FILES; do
  if [[ $FILE == *.wav || $FILE == *.mp3 || $FILE == *.flac ]]; then
    JOB_NAME="${JOB_NAME_PREFIX}$(basename "$FILE")"
    MEDIA_FILE_URI="s3://$BUCKET_NAME/$FILE"
    
    if output_file_exists "$FILE"; then
      echo "Output file for $FILE already exists. Skipping transcription job."
    else
      echo "Starting transcription job for $FILE"

      aws transcribe start-transcription-job \
        --transcription-job-name "$JOB_NAME" \
        --media MediaFileUri="$MEDIA_FILE_URI" \
        --output-bucket-name "$OUTPUT_BUCKET" \
        --output-key "$OUTPUT_FOLDER/$JOB_NAME.json" \
        --identify-language \
        --language-options "${LANGUAGE_OPTIONS[@]}" \
        --settings "ShowSpeakerLabels=$SPEAKER_SEPARATION,MaxSpeakerLabels=$MAX_SPEAKERS"

      echo "Started transcription job $JOB_NAME"
    fi
  fi
done
