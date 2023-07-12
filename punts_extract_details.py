import pandas as pd
import re

def extract_play_data(play):
    match = re.search(r"^(.*?) punts (\d+)", play)
    punter = match.group(1) if match else None
    punt_distance = int(match.group(2)) if match else None
    play = play.replace(match.group(0), '') if match else play

    return_distance = None
    end_location = None

    match = re.search(r"fair catch by (.*?) at (.*)", play)
    if match:
        returner = match.group(1)
        end_location = match.group(2)
        play = play.replace(match.group(0), '')
    else:
        match = re.search(r"returned by (.*?) for ((-?\d+)|(no gain))", play)
        returner = match.group(1) if match else None
        return_distance = 0 if match and match.group(2) == 'no gain' else int(match.group(2)) if match else None
        play = play.replace(match.group(0), '') if match else play

    match = re.search(r"tackle by (.*?)\)", play)
    tackler = match.group(1) if match else None
    play = play.replace(match.group(0), '') if match else play

    match = re.search(r"Penalty on (.*?):", play)
    penalized_player = match.group(1) if match else None
    play = play.replace(match.group(0), '') if match else play

    match = re.search(r"downed by (.*)", play)
    downer = match.group(1) if match else None
    play = play.replace(match.group(0), '') if match else play

    match = re.search(r"blocked by (.*?) recovered by (.*)", play)
    blocker = match.group(1) if match else None
    recoverer = match.group(2) if match else None
    play = play.replace(match.group(0), '') if match else play

    if not end_location:
        match = re.search(r"at (.*?)$", play)
        end_location = match.group(1) if match else None
        play = play.replace(match.group(0), '') if match else play

    match = re.search(r"(touchback|out of bounds|downed|touchdown)", play)
    play_outcome = match.group(0) if match else None
    play = play.replace(match.group(0), '') if match else play

    unprocessed = play.strip()

    return pd.Series({
        'punter': punter,
        'punt_distance': punt_distance,
        'returner': returner,
        'return_distance': return_distance,
        'tackler': tackler,
        'penalized_player': penalized_player,
        'downer': downer,
        'blocker': blocker,
        'recoverer': recoverer,
        'end_location': end_location,
        'play_outcome': play_outcome,
        'unprocessed': unprocessed
    })

# Load the CSV data
df = pd.read_csv('punts_since_2019.csv')

# Apply the function to the 'Detail' column
df_play_data = df['Detail'].apply(extract_play_data)

df_play_data.to_csv('punts_play_data.csv', index=False)
print(df_play_data)
