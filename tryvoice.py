import argparse
import requests
import json
import os
import sys

# Load the settings JSON file
with open('settings.json', 'r') as file:
    settings = json.load(file)

# API settings from settings.json
voice_api_endpoint = settings['voiceAPI']['endpoint']
voice_api_key = settings['voiceAPI']['apikey']

# Load voice data from the JSON file
def load_voice_data():
    with open("voices.json", "r") as file:
        data = json.load(file)
    return data["data"]

# Find the voice actor by name or ID
def find_voice_actor(data, name=None, actor_id=None):
    for actor in data:
        if name and actor["name"].lower() == name.lower():
            return actor
        elif actor_id and actor["actorId"] == actor_id:
            return actor
    return None

# Download the audio sample or create new sample from API
def download_sample(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"Downloaded sample as {filename}")
    else:
        print(f"Failed to download sample. Status code: {response.status_code}")

# Generate a custom audio file with sample text using the API
def generate_custom_sample(actor_id, sample_text, filename):
    url = voice_api_endpoint
    headers = {
        "APIKey": voice_api_key,
        "Content-Type": "application/json"
    }
    data = {
        "data": [
            {
                "actorId": actor_id,
                "text": sample_text,
                "features": [
                    {"key": "speed", "value": "1.0"}
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Custom sample saved as {filename}")
    else:
        print(f"Failed to generate sample. Status code: {response.status_code}")

# Main function
def main():
    parser = argparse.ArgumentParser(description="Download voice sample by actor name or ID")
    parser.add_argument("--name", type=str, help="Name of the voice actor")
    parser.add_argument("--id", type=int, help="ID of the voice actor")
    parser.add_argument("--sampletext", type=str, help="Text to generate a custom sample with the voice")

    args = parser.parse_args()

    # Load data
    data = load_voice_data()

    # Search for the actor
    actor = None
    if args.name:
        actor = find_voice_actor(data, name=args.name)
    elif args.id:
        actor = find_voice_actor(data, actor_id=args.id)

    # If actor is found, download or generate sample
    if actor:
        if args.sampletext:
            # Generate custom audio sample
            filename = f"{actor['name'] if args.name else actor['actorId']}_sample.mp3"
            generate_custom_sample(actor["actorId"], args.sampletext, filename)
        else:
            # Download pre-defined sample
            sample_url = actor.get("audioSampleLink")
            if sample_url:
                filename = f"{actor['name'] if args.name else actor['actorId']}.mp3"
                download_sample(sample_url, filename)
            else:
                print("Audio sample link not found for this actor.")
    else:
        print("Voice actor not found.")

if __name__ == "__main__":
    main()
