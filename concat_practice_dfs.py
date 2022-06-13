import fastf1 as ff1
import pandas as pd
import numpy as np
ff1.Cache.enable_cache('../cache/')
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import boto3
import datetime
import time

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

start = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
print(f"{start} - Beginning of script")
print('----------------------------------------------------------------')
time.sleep(1)

for i in events_list.itertuples():
       df_full = pd.DataFrame(columns=cols)
       try:
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
                     df_full = pd.concat([df_full, df])
                     
              csv_name = f'full_data-round_{i.RoundNumber}.csv'
              df_full.to_csv('/home/guillaume/Python_Projects/Jedha_F1_Project/data/' + csv_name)
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