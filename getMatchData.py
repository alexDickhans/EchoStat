import requests
import json
from keys import BEARER_ID

def get_team_id_by_number(team_number):
    url = f"https://www.robotevents.com/api/v2/teams?number={team_number}"
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer ' + BEARER_ID
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data['data']:
            return data['data'][0]['id']
        else:
            return None
    else:
        response.raise_for_status()

def get_events_by_team_id(team_id):
    url = f"https://www.robotevents.com/api/v2/teams/{team_id}/events?season%5B%5D=190"
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer ' + BEARER_ID
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data['data']
    else:
        response.raise_for_status()

def get_matches_by_event_id(event_id):
    url = f"https://www.robotevents.com/api/v2/events/{event_id}/divisions/1/matches"
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer ' + BEARER_ID
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data['data']
    else:
        response.raise_for_status()

# Example usage
team_number = '229V'
team_id = get_team_id_by_number(team_number)
print(team_id)
if team_id:
    events = get_events_by_team_id(team_id)
    if events:
        all_matches = []
        output = {
            "team_number": team_number,
            "events": []
        }
        for event in events:
            event_info = {
                "name": event['name'],
                "end": event['end'],
                "matches": get_matches_by_event_id(event['id'])
            }
            output["events"].append(event_info)
            all_matches.extend(event_info["matches"])
        output["total_matches"] = len(all_matches)
        with open('output.json', 'w') as file:
            json.dump(output, file, indent=4)
    else:
        print(f"No events found for team number {team_number}")
else:
    print(f"No team found with number {team_number}")