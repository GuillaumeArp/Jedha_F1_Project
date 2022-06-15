import fastf1 as ff1
import pandas as pd
import numpy as np
ff1.Cache.enable_cache('../cache/')
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import boto3
import datetime
import time
import re

events_list = pd.DataFrame(ff1.get_event_schedule(2022)[2:])
session_dict = {'conventional': ['Practice 1', 'Practice 2', 'Practice 3'],
                'sprint': ['Practice 1', 'Practice 2', 'Sprint']}
session = boto3.Session()
s3 = boto3.resource('s3')

cols = ['Time', 'DriverNumber', 'LapTime', 'LapNumber', 'Stint', 'PitOutTime',
       'PitInTime', 'Sector1Time', 'Sector2Time', 'Sector3Time',
       'Sector1SessionTime', 'Sector2SessionTime', 'Sector3SessionTime',
       'SpeedI1', 'SpeedI2', 'SpeedFL', 'SpeedST', 'IsPersonalBest',
       'Compound', 'TyreLife', 'FreshTyre', 'LapStartTime', 'Team', 'Driver',
       'TrackStatus', 'IsAccurate', 'LapStartDate']

compound_colors = {
    'SOFT': '#FF3333',
    'MEDIUM': '#FFF200',
    'HARD': '#EBEBEB',
}

dict_nb_laps = {1: 57, 2: 50, 3: 58, 4: 63, 5: 57, 6: 66, 7: 78, 8: 51, 9: 70, 10: 52, 11: 71, 12: 53, 13: 70, 14: 44, 15: 72, 16: 53, 17: 61, 18: 53, 19: 56, 20: 71, 21: 71, 22: 58}

def time_to_seconds(string):
    array = re.findall(r'[0-9]+', str(string))
    array = array[1:]
    array[0] = int(array[0]) * 3600
    array[1] = int(array[1]) * 60
    try : 
        array = float(str(array[0] + array[1] + int(array[2])) + "." + array[3])
        return array
    except :
        return float(str(int(array[-2]) + int(array[-1])) + ".0")
 
def get_deg_values(dc, dr):
    list_times = []

    for i in range(1, nb_laps + 1):
        dr = dr * (1 + dc)
        list_times.append(dr)
        
    return list_times

start = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
print(f"{start} - Beginning of script")
print('----------------------------------------------------------------')
time.sleep(1)

for i in events_list.itertuples():
       
       gp_round = i.RoundNumber
       nb_laps = dict_nb_laps[gp_round]
       
       fuel_per_lap_kg = 105 / nb_laps
       mean_laps = 60
       time_gain_per_kg = 0.035
       laps_coeff = mean_laps / nb_laps
       time_gained_per_lap = laps_coeff * time_gain_per_kg * fuel_per_lap_kg
       
       try:
              dffp = pd.DataFrame(columns=cols)
              if i.EventFormat == 'conventional':
                     sessions_list = session_dict['conventional']
              else:
                     sessions_list = session_dict['sprint']   
              
              for j in sessions_list:        
                     session = ff1.get_session(2022, i.RoundNumber, j)
                     session.load(weather=True, telemetry=True)
                     df = session.laps.pick_quicklaps()
                     df = pd.DataFrame(df)
                     df['Session'] = j
                     dffp_complete = pd.concat([dffp, df])
                     
              dffp_complete = dffp_complete.drop(dffp.columns[[0,5,6,7,8,9,10,11,12,13,14,15,16,17,21,25,26]], axis=1)

              dffp_temp = dffp_complete.copy()
              dffp_temp['LapTime'] = dffp_temp['LapTime'].apply(pd.to_timedelta)
              dffp_times = dffp_temp.groupby('Compound')['LapTime'].mean()
              dffp_times = pd.DataFrame(dffp_times).sort_values(by='LapTime').reset_index()
        
              hard_to_soft = (dffp_times['LapTime'].iloc[2] - dffp_times['LapTime'].iloc[0]) * 0.75
              medium_to_soft = (dffp_times['LapTime'].iloc[1] - dffp_times['LapTime'].iloc[0]) * 0.75
       
              dffp_complete = dffp_complete[dffp_complete['TyreLife'].notna()]
              dffp_copy = dffp_complete.copy()
              dffp_copy['LapTime'] = dffp_complete['LapTime'].apply(pd.to_timedelta)
              dffp_copy["LapTimeSeconds"] = dffp_copy["LapTime"].apply(time_to_seconds)
              
              dffp_full = dffp_copy.groupby(['TyreLife','Compound'] ,as_index=False)[['LapTimeSeconds']].mean().sort_values(by= ['Compound','TyreLife'])
              dffp_filtered = dffp_full[dffp_full['TyreLife'] > 5.0]
              
              dffp_soft = dffp_filtered[dffp_filtered['Compound'] == 'SOFT'].reset_index(drop=True)
              dffp_medium = dffp_filtered[dffp_filtered['Compound'] == 'MEDIUM'].reset_index(drop=True)
              dffp_hard = dffp_filtered[dffp_filtered['Compound'] == 'HARD'].reset_index(drop=True)
              
              diff_soft = (dffp_soft['LapTimeSeconds'].iloc[-1] - dffp_soft['LapTimeSeconds'].iloc[0])
              diff_medium = (dffp_medium['LapTimeSeconds'].iloc[-1] - dffp_medium['LapTimeSeconds'].iloc[0])
              diff_hard = dffp_hard['LapTimeSeconds'].iloc[-1] - dffp_hard['LapTimeSeconds'].iloc[0]
              
              if 'WET' in dffp_filtered['Compound'].tolist() or 'INTERDMEDIATE' in dffp_filtered['Compound'].tolist() or diff_soft < 0 or diff_medium < 0 or diff_hard < 0:
                     diff_soft_per_lap = 0.25
                     diff_medium_per_lap = 0.15
                     diff_hard_per_lap = 0.09
              
              else:
                     diff_soft_per_lap = diff_soft / len(dffp_soft)
                     diff_medium_per_lap = diff_medium / len(dffp_medium)
                     diff_hard_per_lap = diff_hard / len(dffp_hard)
                     
              dffp_soft['FuelGain'] = time_gained_per_lap
              dffp_soft['FuelGain'] = dffp_soft['FuelGain'].cumsum()
              dffp_soft['AdjustedTime'] = dffp_soft['LapTimeSeconds'] + dffp_soft['FuelGain']
                     
              laptime_min_series = dffp_full[dffp_full['Compound'] == 'SOFT'].sort_values('LapTimeSeconds', ascending=True).iloc[0]
              laptime_min = {'TyreLife': laptime_min_series['TyreLife'], 'LapTimeSeconds': laptime_min_series['LapTimeSeconds']}
              
              laptime_min_calc_soft =  (laptime_min['LapTimeSeconds'] - ((laptime_min['TyreLife'] - 1) * diff_soft_per_lap)) + (nb_laps * time_gained_per_lap)
              laptime_min_calc_medium = (laptime_min_calc_soft + time_to_seconds(medium_to_soft))
              laptime_min_calc_hard = laptime_min_calc_soft + time_to_seconds(hard_to_soft)
              
              list_times_soft = get_deg_values(0.13, diff_soft_per_lap)
              list_times_medium = get_deg_values(0.085, diff_medium_per_lap)
              list_times_hard = get_deg_values(0.065, diff_medium_per_lap)
              
              df_times_soft = pd.DataFrame(columns=['Lap', 'Tyre', 'LapTimeSeconds', 'DeltaDeg', 'FuelDeg', 'AdjustedTime'])
             
              df_times_soft['Lap'] = list(range(1, nb_laps + 1))
              df_times_soft['Tyre'] = 'SOFT'
              df_times_soft['LapTimeSeconds'] = laptime_min_calc_soft
              df_times_soft['DeltaDeg'] = list_times_soft
              df_times_soft['FuelDeg'] = time_gained_per_lap * df_times_soft['Lap']
              df_times_soft['AdjustedTime'] = df_times_soft.apply(lambda row: row['LapTimeSeconds'] + row['DeltaDeg'], axis=1)
              df_times_soft['FinalLapTime'] = df_times_soft.apply(lambda row: row['AdjustedTime'] - row['FuelDeg'], axis=1)
              
              df_times_medium = pd.DataFrame(columns=['Lap', 'Tyre', 'LapTimeSeconds', 'DeltaDeg', 'FuelDeg', 'AdjustedTime'])

              df_times_medium['Lap'] = list(range(1, nb_laps + 1))
              df_times_medium['Tyre'] = 'MEDIUM'
              df_times_medium['LapTimeSeconds'] = laptime_min_calc_medium
              df_times_medium['DeltaDeg'] = list_times_medium
              df_times_medium['FuelDeg'] = time_gained_per_lap * df_times_medium['Lap']
              df_times_medium['AdjustedTime'] = df_times_medium.apply(lambda row: row['LapTimeSeconds'] + row['DeltaDeg'], axis=1)
              df_times_medium['FinalLapTime'] = df_times_medium.apply(lambda row: row['AdjustedTime'] - row['FuelDeg'], axis=1)
              
              df_times_hard = pd.DataFrame(columns=['Lap', 'Tyre', 'LapTimeSeconds', 'DeltaDeg', 'FuelDeg', 'AdjustedTime'])

              df_times_hard['Lap'] = list(range(1, nb_laps + 1))
              df_times_hard['Tyre'] = 'HARD'
              df_times_hard['LapTimeSeconds'] = laptime_min_calc_hard
              df_times_hard['DeltaDeg'] = list_times_hard
              df_times_hard['FuelDeg'] = time_gained_per_lap * df_times_hard['Lap']
              df_times_hard['AdjustedTime'] = df_times_hard.apply(lambda row: row['LapTimeSeconds'] + row['DeltaDeg'], axis=1)
              df_times_hard['FinalLapTime'] = df_times_hard.apply(lambda row: row['AdjustedTime'] - row['FuelDeg'], axis=1)
              
              df_times = pd.concat([df_times_soft, df_times_medium, df_times_hard])
              df_times['TimeStr'] = df_times['FinalLapTime'].apply(lambda x: str(datetime.timedelta(seconds=x))[2:-3])
              
              csv_name = f'full_data-round_{gp_round}.csv'
              df_times.to_csv('/home/guillaume/Python_Projects/Jedha_F1_Project/data/' + csv_name)
              print(f'{csv_name} written')
              
              full_path = '/home/guillaume/Python_Projects/Jedha_F1_Project/data/' + csv_name
              s3.Bucket('f1-jedha-bucket').upload_file(full_path, f'data/{csv_name}', ExtraArgs={'GrantRead': 'uri="http://acs.amazonaws.com/groups/global/AllUsers"'})
              print(f'{csv_name} uploaded')
              
             
       except:
              break
          
print('----------------------------------------------------------------')
time.sleep(1)
end = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
print(f"{start} - End of script")
print('\n')
print('\n')






