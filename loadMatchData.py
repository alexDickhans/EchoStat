import json
from scipy.linalg import solve
import numpy as np

def load_match_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Example usage
file_path = 'output.json'
match_data = load_match_data(file_path)

ids = dict()

scores = []

for event in match_data['events']:
    for match in event['matches']:
        ids[match['alliances'][0]['teams'][0]['team']['id']] = match['alliances'][0]['teams'][0]['team']['name']
        ids[match['alliances'][0]['teams'][1]['team']['id']] = match['alliances'][0]['teams'][1]['team']['name']
        ids[match['alliances'][1]['teams'][0]['team']['id']] = match['alliances'][1]['teams'][0]['team']['name']
        ids[match['alliances'][1]['teams'][1]['team']['id']] = match['alliances'][1]['teams'][1]['team']['name']

        scores.append({"score": match['alliances'][0]['score'], "teams": [match['alliances'][0]['teams'][0]['team']['id'], match['alliances'][0]['teams'][1]['team']['id']], "opponents": [match['alliances'][1]['teams'][0]['team']['id'], match['alliances'][1]['teams'][1]['team']['id']]})
        scores.append({"score": match['alliances'][1]['score'], "teams": [match['alliances'][1]['teams'][0]['team']['id'], match['alliances'][1]['teams'][1]['team']['id']], "opponents": [match['alliances'][0]['teams'][0]['team']['id'], match['alliances'][0]['teams'][1]['team']['id']]})

listId = list(ids)
listId.sort()

b = np.array([score['score'] for score in scores], dtype=float)
A = np.zeros((len(scores), len(ids)))

for score in scores:
    A[scores.index(score)][listId.index(score['teams'][0])] = 1
    A[scores.index(score)][listId.index(score['teams'][1])] = 1

x, residuals, rank, s = np.linalg.lstsq(A, b)
print(x)

score_dict = {ids[listId[i]]: score for i, score in enumerate(x)}
sorted_scores = dict(sorted(score_dict.items(), key=lambda item: item[1]))

for team, score in sorted_scores.items():
    print(team, score)
