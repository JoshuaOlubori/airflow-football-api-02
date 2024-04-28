import requests
API_KEY = "8feeed635dmshbab9080dc4f248bp112d75jsn9661eab3597b"
API_HOST = "api-football-v1.p.rapidapi.com"


API_ENDPOINT = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST
}
league_id=71
chosen_season=2023
querystring = {"league": str(league_id), "season": chosen_season}

response = requests.get(API_ENDPOINT, headers=headers, params=querystring)

print(response.raise_for_status())

print(response.json()['response'])