import requests
import pandas as pd

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": "https://www.fangraphs.com/projections",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
}

def getHitters():
    params = {
        "type": "atc",
        "stats": "bat",
        "pos": "all",
        "team": "0",
        "players": "0",
        "lg": "all",
    }
    resp = requests.get("https://www.fangraphs.com/api/projections", params=params, headers=HEADERS)
    print(f"Hitters  — Status: {resp.status_code}, Length: {len(resp.text)}")
    return pd.DataFrame(resp.json())


def getPitchers():
    params = {
        "type": "atc",
        "stats": "pit",
        "pos": "all",
        "team": "0",
        "players": "0",
        "lg": "all",
    }
    resp = requests.get("https://www.fangraphs.com/api/projections", params=params, headers=HEADERS)
    print(f"Pitchers — Status: {resp.status_code}, Length: {len(resp.text)}")
    return pd.DataFrame(resp.json())
