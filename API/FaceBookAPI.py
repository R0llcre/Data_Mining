import os
import requests
import json

def fetch_facebook_data(link):
    url = "https://facebook-profil-scraper.p.rapidapi.com/pub"
    payload = { "link": link }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "facebook-profil-scraper.p.rapidapi.com"
    }

    try:
        # Send API request
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()  # Check if the request was successful

        # Parse the response JSON
        data = response.json()
        # Extract the actual data part
        if 'data' in data:
            return data['data']
        else:
            print("The expected 'data' part was not found in the response")
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred with the request: {e}")
        return None
    except json.JSONDecodeError:
        print("The response is not valid JSON format")
        return None

def save_to_file(data, filename="facebook_data.json"):
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Data has been saved to the file: {filename}")
    except IOError as e:
        print(f"File writing error: {e}")

def main():
    link = "https://www.facebook.com/100088300905263/posts/pfbid02wAZTvMJ8AHoHZcCYvCjvK9Eo7yd7MZHHnUqnYQT1UETFPjYTCPhHbwNoheBS8k9Tl/?app=fbl"
    data = fetch_facebook_data(link)
    if data:
        print(json.dumps(data, indent=4))  # Pretty print JSON data
        save_to_file(data)

if __name__ == "__main__":
    main()
