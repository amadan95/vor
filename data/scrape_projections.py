import requests
from bs4 import BeautifulSoup as BS
import pandas as pd
import config

def scrape_projections():

    df = pd.DataFrame()

    base_url = config.FANTASY_PROS_PROJECTIONS_URL

    positions = [
        'https://www.fantasypros.com/nfl/projections/wr.php',
        'https://www.fantasypros.com/nfl/projections/rb.php',
        'https://www.fantasypros.com/nfl/projections/te.php',
        'https://www.fantasypros.com/nfl/projections/qb.php'
    ]

    for url in positions:

        res = requests.get(url)

        pos = url.split('/')[-1].replace('.php', '').upper()

        soup = BS(res.content, 'html.parser')

        table = soup.find('table', {'id': 'data'})

        pos_df = pd.read_html(str(table))[0]
        pos_df.columns = pos_df.columns.droplevel(level=0)

        if 'REC' in pos_df.columns:
            pos_df['FPTS'] = pos_df['FPTS'] + pos_df['REC']*0.5

        pos_df['Player'] = pos_df['Player'].apply(
            lambda x: ' '.join(x.split()[:-1])
        )

        pos_df['Pos'] = pos

        pos_df = pos_df[['Player', 'Pos', 'FPTS']]

        df = pd.concat([df, pos_df])

    df = df.sort_values(by='FPTS', ascending=False)
    return df