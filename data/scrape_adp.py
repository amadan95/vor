import requests
from bs4 import BeautifulSoup as BS
import pandas as pd
import config

def fix_player_name(player_name):
    player_name_items = player_name.split()
    player_name = ' '.join(player_name_items[:-2])
    return player_name

def get_adp_data():
    pd.set_option('display.max_rows', None)
    url = config.FANTASY_PROS_HALF_PPR_ADP_URL
    res = requests.get(url)

    soup = BS(res.content, 'html.parser')

    table = soup.find('table', {'id': 'data'})

    df = pd.read_html(str(table))[0]

    df['Player'] = df['Player Team (Bye)'].apply(fix_player_name)

    df = df[[
        'Player', 'POS', 'Rank', 'AVG'
    ]]

    return df

def find_replacement_players(n=100):
    df = get_adp_data()
    df = df[:n]

    replacement_players = {
        'RB': None,
        'WR': None,
        'TE': None,
        'QB': None
    }

    positions = replacement_players.keys()

    for _, row in df.iterrows():
        row_pos = str(row['POS'])
        for p in positions:
            if p in row_pos:
                replacement_players[p] = row['Player']
        
    return replacement_players