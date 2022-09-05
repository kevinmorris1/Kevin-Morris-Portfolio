import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

years = list(range(2022, 2016, -1))
all_matches = []
standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"

for year in years:  # loop for all years in range
    print(year)
    data = requests.get(standings_url) # request page
    soup = BeautifulSoup(data.text, features='html.parser') # extract all information form page
    standings_table = soup.select('table.stats_table')[0] # log the standings table for the current year

    links = [l.get("href") for l in standings_table.find_all('a')] # get the reference to all the links from all links on page
    links = [l for l in links if '/squads/' in l] # all links with '/squads/' in order to find the team pages for all clubs
    team_urls = [f"https://fbref.com{l}" for l in links] # absolute links for club specific pages
    
    previous_season = soup.select("a.prev")[0].get("href") # set new standings page to the previous season for next loop
    standings_url = f"https://fbref.com{previous_season}"
    
    for team_url in team_urls: # loop for all team links on standings page
        team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ") # parse team name
        print(team_name)
        data = requests.get(team_url)
        
        matches = pd.read_html(data.text, match="Scores & Fixtures")[0] # Scores and fixtures dataframe for the club
        matches = matches[['Date', 'Time', 'Comp', 'Round', 'Day', 'Venue', 'Result', 'GF', 'GA', 'Opponent', 'Attendance', 'Captain', 'Formation','Referee']]

        soup = BeautifulSoup(data.text, features='html.parser') # extract all information from page
        links = soup.find_all('a') # find all links on page for the club
        links = [l.get("href") for l in links] # get reference urls for those links
        links = [l for l in links if l and (('all_comps/shooting/' in l) or ('all_comps/possession/' in l) or ('all_comps/passing/' in l) or ('all_comps/defense/' in l))] # filter to only shooting stats links
        links = [*set(links)]

        df_info = {
            'matches': {
                'name': 'Matches',
                'column_levels': [],
                'df': matches,
            },
            'shooting': {
                'name': 'Shooting',
                'column_levels': ['Expected', '', 'Standard', ''],
                'df': pd.DataFrame()
            },
            'possession': {
                'name': 'Possession',
                'column_levels': ['Carries', 'Dribbles', '', 'Receiving', 'Touches', ''],
                'df': pd.DataFrame()
            },
            'passing': {
                'name': 'Passing',
                'column_levels': ['', 'Long', 'Medium', 'Short', 'Total', '', '', '', '', '', '', '', ''],
                'df': pd.DataFrame()
            },
            'defense': {
                'name': 'Defensive Actions',
                'column_levels': ['Blocks', '', 'Pressures', 'Tackles', '', '', '', '', '', 'Vs Dribbles'],
                'df': pd.DataFrame()
            }
        }

        # Update dataframes in our dictionary to pull web page tables
        for l in links:
            for key, webster in df_info.items():

                if (key != 'matches') and ('all_comps/'+ key in l):
                        data = requests.get(f"https://fbref.com{l}") # pull that data for the stats link
                        webster['df'] = pd.read_html(data.text, match=webster['name'])[0] # read the link's data from the table
                        d = dict(zip(webster['df'].columns.levels[0], webster['column_levels'])) # Clear out unecessary multi indexed column names and rename columns to specify features
                        webster['df'] = webster['df'].rename(columns=d, level=0)

        # Clean dataframe structure
        for key, webster in df_info.items():
            if (key != 'matches'):
                webster['df'].columns = ['_'.join(col).strip() for col in webster['df'].columns.values]
            webster['df'].columns = webster['df'].columns.str.lstrip("_")
            webster['df'].columns = webster['df'].columns.str.replace(' ', '_')
            webster['df'].columns = webster['df'].columns.str.replace('-', '_')
            webster['df'].columns = webster['df'].columns.str.replace(':', '_')
            webster['df'].columns = webster['df'].columns.str.lower()
            webster['df'] = webster['df'].set_index(['date', 'time', 'comp', 'round', 'day', 'venue', 'result', 'gf', 'ga', 'opponent'])
            webster['df'] = webster['df'].add_prefix(key + '_')
            webster['df'] = webster['df'].reset_index()
        
        try:
            team_data = df_info['matches']['df'].copy()
            for key, webseter in df_info.items():
                if (key != 'matches'):
                    team_data = team_data.merge(df_info[key]['df'], on=['date', 'time', 'comp', 'round', 'day', 'venue', 'result', 'gf', 'ga', 'opponent'])

        except ValueError:
            continue

        team_data = team_data[team_data["comp"] == "Premier League"]
        
        team_data["team"] = team_name
        all_matches.append(team_data)
        time.sleep(1)


match_df = pd.concat(all_matches).reset_index(drop=True)
match_df = match_df.sort_values('date', ascending=False)

columns_ordered = [
    'team',
    'opponent',    
    'date',    
    'time',
    'day',
    'comp',
    'round',
    'venue',
    'result',
    'gf',
    'ga',
    'matches_attendance',
    'matches_captain',
    'matches_formation',
    'matches_referee',
    'shooting_standard_gls',
    'shooting_standard_sh',
    'shooting_standard_sot',
    'shooting_standard_sot%',
    'shooting_standard_g/sh',
    'shooting_standard_g/sot',
    'shooting_standard_dist',
    'shooting_standard_fk',
    'shooting_standard_pk',
    'shooting_standard_pkatt',
    'possession_poss',
    'possession_touches_touches',
    'possession_touches_def_pen',
    'possession_touches_def_3rd',
    'possession_touches_mid_3rd',
    'possession_touches_att_3rd',
    'possession_touches_att_pen',
    'possession_touches_live',
    'possession_dribbles_succ',
    'possession_dribbles_att',
    'possession_dribbles_succ%',
    'possession_dribbles_#pl',
    'possession_dribbles_megs',
    'possession_carries_carries',
    'possession_carries_totdist',
    'possession_carries_prgdist',
    'possession_carries_prog',
    'possession_carries_1/3',
    'possession_carries_cpa',
    'possession_carries_mis',
    'possession_carries_dis',
    'possession_receiving_targ',
    'possession_receiving_rec',
    'possession_receiving_rec%',
    'possession_receiving_prog',
    'passing_total_cmp',
    'passing_total_att',
    'passing_total_cmp%',
    'passing_total_totdist',
    'passing_total_prgdist',
    'passing_short_cmp',
    'passing_short_att',
    'passing_short_cmp%',
    'passing_medium_cmp',
    'passing_medium_att',
    'passing_medium_cmp%',
    'passing_long_cmp',
    'passing_long_att',
    'passing_long_cmp%',
    'passing_ast',
    'passing_kp',
    'passing_1/3',
    'passing_ppa',
    'passing_crspa',
    'passing_prog',
    'defense_tackles_tkl',
    'defense_tackles_tklw',
    'defense_tackles_def_3rd',
    'defense_tackles_mid_3rd',
    'defense_tackles_att_3rd',
    'defense_vs_dribbles_tkl',
    'defense_vs_dribbles_att',
    'defense_vs_dribbles_tkl%',
    'defense_vs_dribbles_past',
    'defense_pressures_press',
    'defense_pressures_succ',
    'defense_pressures_%',
    'defense_pressures_def_3rd',
    'defense_pressures_mid_3rd',
    'defense_pressures_att_3rd',
    'defense_blocks_blocks',
    'defense_blocks_sh',
    'defense_blocks_shsv',
    'defense_blocks_pass',
    'defense_int',
    'defense_tkl+int',
    'defense_clr',
    'defense_err'
]

match_df = match_df[columns_ordered]

match_df.to_csv('epl_match_data.csv', index = False)