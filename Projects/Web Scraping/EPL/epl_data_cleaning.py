import numpy as np
import pandas as pd
import datetime as dt

df = pd.read_csv('epl_match_data.csv')
df = df.drop(columns = ['matches_attendance', 'shooting_standard_gls', 'shooting_standard_g/sot', 'defense_tkl+int'])
df = df.dropna()

df.loc[:,'date'] = df.loc[:,'date'].str.cat(df.loc[:,'time'], sep=' ')
df.loc[:,'date'] = pd.to_datetime(df.loc[:,'date'])
df.loc[:,'hour'] = df.loc[:,'date'].dt.hour
df.loc[:,'day_weekend'] = df.loc[:,'date'].dt.day.isin([5,6])

df.loc[:,'is_home'] = (df.loc[:,'venue'] == 'Home')
df.loc[:,'is_win'] = (df.loc[:, 'result'] == 'W')
df.loc[:,'is_loss'] = (df.loc[:, 'result'] == 'L')
df.loc[:,'is_draw'] = (df.loc[:, 'result'] == 'D')

df.loc[:,'matchweek'] = df.loc[:, 'round'].str.partition(' ')[2].astype(int)

ordered_columns = [
    'team',
    'opponent',
    'comp',
    'matchweek',
    'date',
    'result',
    'is_win',
    'is_loss',
    'is_draw',
    'hour',
    'day_weekend',
    'is_home',
    'gf',
    'ga',
    'shooting_standard_sh',
    'shooting_standard_sot',
    'shooting_standard_sot%',
    'shooting_standard_g/sh',
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
    'defense_clr',
    'defense_err'
]

df = df[ordered_columns]

# Column Reference Lists
numerics = ['int64', 'float64']
columns_numeric = list((df.select_dtypes(include=numerics).columns))

removes = ['hour', 'day_weekend', 'is_home', 'team', 'opponent','comp', 'matchweek','date','result','is_draw','is_loss']
columns_match_info = [col for col in ordered_columns if col not in removes]

columns_results = ['is_win','is_draw','is_loss']

columns_rolling_5_mean = [f'{c}_rolling_5_mean' for c in columns_numeric]
columns_prev_ecounter = [f'{c}_prev_encounter' for c in columns_match_info]
columns_recent_form = [f'{c}_rolling_5_count' for c in columns_results]


def rolling_info(group, cols, new_cols, num, func):
    group = group.sort_values('date')
    rolling_stats = func(group[cols].rolling(num, closed='left'))
    group[new_cols] = rolling_stats
    group = group.dropna(subset=new_cols)
    return group

def rolling_mean(obj):
    return obj.mean()

def rolling_sum(obj):
    return obj.sum()

# Add previous enounter stats
df = df.groupby(['team','opponent']).apply(lambda x: rolling_info(x, columns_match_info, columns_prev_ecounter, 1, rolling_sum))
df.droplevel(['team', 'opponent'])
df = df.reset_index(drop=True)

# Stats average from past 5 matches
df = df.groupby('team').apply(lambda x: rolling_info(x, columns_numeric, columns_rolling_5_mean, 5, rolling_mean))
df = df.droplevel('team')
df = df.reset_index(drop=True)

# recent form counts
df = df.groupby('team').apply(lambda x: rolling_info(x, columns_results, columns_recent_form, 5, rolling_sum))
df = df.droplevel('team')
df = df.reset_index(drop=True)

df.loc[:,'team_name'] = df.loc[:,'team']
df.loc[:,'opponent_name'] = df.loc[:,'opponent']
df = pd.get_dummies(data=df, columns=['team_name', 'opponent_name'], dtype=bool)

df.to_csv('epl_match_data_cleaned.csv', index = False)