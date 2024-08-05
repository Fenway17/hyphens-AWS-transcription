#!/bin/bash

# Configuration
BUCKET_NAME="cs-calls-audio"
OUTPUT_BUCKET="cs-calls-transcription"
LANGUAGE_OPTIONS=("en-US" "zh-CN" "ms-MY")
JOB_NAME_PREFIX="call-transcription-job-"
AUDIO_FOLDER="rawcalls-jan2024"
# Currently unable to use this custom vocab as it is tied to english only
CUSTOM_VOCABULARY_NAME="PharmaceuticalTerms"
SPEAKER_SEPARATION=true
MAX_SPEAKERS=2  # Set the number of speakers

# List all audio files in the S3 bucket folder
FILES=$(aws s3 ls s3://$BUCKET_NAME/$AUDIO_FOLDER/ --recursive | awk '{print $4}')

# Iterate over each file and start a transcription job
for FILE in $FILES; do
  if [[ $FILE == *.wav || $FILE == *.mp3 || $FILE == *.flac ]]; then
    JOB_NAME="${JOB_NAME_PREFIX}$(basename "$FILE" .audio)"
    MEDIA_FILE_URI="s3://$BUCKET_NAME/$FILE"
    
    echo "Starting transcription job for $FILE"

    aws transcribe start-transcription-job \
      --transcription-job-name "$JOB_NAME" \
      --media MediaFileUri="$MEDIA_FILE_URI" \
      --output-bucket-name "$OUTPUT_BUCKET" \
      --identify-language \
      --language-options $LANGUAGE_OPTIONS \
      --settings "ShowSpeakerLabels=$SPEAKER_SEPARATION,MaxSpeakerLabels=$MAX_SPEAKERS"

    echo "Started transcription job $JOB_NAME"
  fi
done
