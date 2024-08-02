import json
import os
import sys

def load_json(file_path):
    """Load JSON file from a given file path."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def process_transcription(json_data):
    """Process the transcription JSON data and format it into a readable format."""
    items = json_data['results']['items']
    speaker_labels = json_data['results'].get('speaker_labels', {}).get('segments', [])
    
    formatted_text = []
    current_speaker = None
    for item in items:
        if item['type'] == 'pronunciation':
            if 'speaker_label' in item:
                speaker_label = item['speaker_label']
                if speaker_label != current_speaker:
                    formatted_text.append(f'\n{speaker_label}: ')
                    current_speaker = speaker_label
            word = item['alternatives'][0]['content']
            formatted_text.append(word + ' ')
        elif item['type'] == 'punctuation':
            punctuation = item['alternatives'][0]['content']
            formatted_text.append(punctuation)

    return ''.join(formatted_text)

def save_to_file(content, output_file):
    """Save the processed content to a text file."""
    with open(output_file, 'w') as file:
        file.write(content)

def process_folder(input_folder, output_folder):
    """Process all JSON files in the specified folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            json_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, filename.replace('.json', '.txt'))
            
            print(f'Processing {filename}')
            json_data = load_json(json_file_path)
            formatted_text = process_transcription(json_data)
            save_to_file(formatted_text, output_file_path)
            print(f'Saved transcription to {output_file_path}')

def main(input_folder, output_folder):
    """Main function to process a folder of JSON transcription files."""
    process_folder(input_folder, output_folder)
    print(f'Processed all files in {input_folder} and saved results to {output_folder}')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python process_transcriptions.py <input_folder> <output_folder>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]

    main(input_folder, output_folder)
