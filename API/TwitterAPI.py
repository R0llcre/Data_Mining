import os
import requests
import json


def fetch_twitter_data(query, limit=5, section="top", language="en", min_likes=20, min_retweets=20,
                       start_date="2022-01-01"):
    url = "https://twitter154.p.rapidapi.com/search/search"
    payload = {
        "query": query,
        "limit": limit,
        "section": section,
        "language": language,
        "min_likes": min_likes,
        "min_retweets": min_retweets,
        "start_date": start_date
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "twitter154.p.rapidapi.com"
    }

    try:
        # Send API request
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Check if the request was successful

        # Parsing Response JSON
        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        print(f"An error occurred in the request: {e}")
        return None
    except json.JSONDecodeError:
        print("Response is not in valid JSON format")
        return None


def save_to_file(data, filename="twitter_data.json"):
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to file: {filename}")
    except IOError as e:
        print(f"File Write Error: {e}")


def main():
    query = "#python"  # Search Content
    data = fetch_twitter_data(query)
    if data:
        print(json.dumps(data, indent=4))  # Beautify output JSON data
        save_to_file(data)


if __name__ == "__main__":
    main()
