import argparse
import requests
import json
import os

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

# Download the audio sample
def download_sample(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"Downloaded sample as {filename}")
    else:
        print(f"Failed to download sample. Status code: {response.status_code}")

# Main function
def main():
    parser = argparse.ArgumentParser(description="Download voice sample by actor name or ID")
    parser.add_argument("--name", type=str, help="Name of the voice actor")
    parser.add_argument("--id", type=int, help="ID of the voice actor")
    
    args = parser.parse_args()
    
    # Load data
    data = load_voice_data()
    
    # Search for the actor
    actor = None
    if args.name:
        actor = find_voice_actor(data, name=args.name)
    elif args.id:
        actor = find_voice_actor(data, actor_id=args.id)
    
    # If actor is found, download sample
    if actor:
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
