import requests
import json
import sys
import os
from pydub import AudioSegment

# Check if at least a file argument is provided
if len(sys.argv) < 2:
    print("Usage: python dialoger.py <dialog.json> [output_filename]")
    sys.exit(1)

# Load the JSON file from the command-line argument
json_file = sys.argv[1]
output_filename = sys.argv[2] if len(sys.argv) > 2 else "combined_output.mp3"

with open(json_file, 'r') as f:
    dialog_data = json.load(f)

url = "https://synthesys.live/api/actor/generateVoice"
headers = {
    "APIKey": "5b429969-ef59-4a74-b1af-bcf0301e7f3e",  # Replace with your actual API key
    "Content-Type": "application/json"
}

audio_segments = []

# Iterate through each dialog entry in the JSON
for i, entry in enumerate(dialog_data["dialog"]):
    data = {
        "data": [
            {
                "actorId": entry["actorId"],
                "text": entry["text"],
                "features": [
                    {
                        "key": "speed",
                        "value": "1.0"
                    }
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        filename = f"output_{i}.mp3"
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"MP3 file saved as '{filename}'")

        # Load the audio file into pydub
        audio_segment = AudioSegment.from_mp3(filename)
        audio_segments.append(audio_segment)
    else:
        print(f"Failed with status code {response.status_code}")
        print(response.text)

# Concatenate all audio segments
combined_audio = AudioSegment.empty()
for segment in audio_segments:
    combined_audio += segment

# Export the combined audio file
combined_audio.export(output_filename, format="mp3")
print(f"Combined MP3 file saved as '{output_filename}'")

# Delete intermediate files
for i in range(len(audio_segments)):
    filename = f"output_{i}.mp3"
    if os.path.exists(filename):
        os.remove(filename)
        print(f"Deleted intermediate file '{filename}'")
