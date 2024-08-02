#!/bin/bash

# Configuration
BUCKET_NAME="cs-calls-audio"
OUTPUT_BUCKET="cs-calls-transcription"
LANGUAGE_CODE="en-US"
JOB_NAME_PREFIX="call-transcription-job-"
AUDIO_FOLDER="test-calls"
CUSTOM_VOCABULARY_NAME="PharmaceuticalTerms"
SPEAKER_SEPARATION=true
MAX_SPEAKERS=2  # Set the number of speakers

# List all audio files in the S3 bucket folder
FILES=$(aws s3 ls s3://$BUCKET_NAME/$AUDIO_FOLDER/ | awk '{print $4}')

# Iterate over each file and start a transcription job
for FILE in $FILES; do
  JOB_NAME="${JOB_NAME_PREFIX}$(basename $FILE .wav)"
  MEDIA_FILE_URI="s3://$BUCKET_NAME/$AUDIO_FOLDER/$FILE"
  
  echo "Starting transcription job for $FILE"

  aws transcribe start-transcription-job \
    --transcription-job-name "$JOB_NAME" \
    --language-code "$LANGUAGE_CODE" \
    --media MediaFileUri="$MEDIA_FILE_URI" \
    --output-bucket-name "$OUTPUT_BUCKET" \
    --settings "VocabularyName=$CUSTOM_VOCABULARY_NAME,ShowSpeakerLabels=$SPEAKER_SEPARATION,MaxSpeakerLabels=$MAX_SPEAKERS"

  echo "Started transcription job $JOB_NAME"
done
