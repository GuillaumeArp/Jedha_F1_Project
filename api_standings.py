import requests
import pandas as pd
import boto3
import datetime
import time


# Ergast API base request
def ergast_retrieve(api_endpoint: str):
    url = f'https://ergast.com/api/f1/{api_endpoint}.json'
    response = requests.get(url).json()
    
    return response['MRData']

# Get drivers standings
def update_driver_standings(rounds):
    standings_dict = {}
    for i in range(1, rounds+1):
        try:
            r = ergast_retrieve(f'current/{i}/driverStandings')
            standings = r['StandingsTable']['StandingsLists'][0]['DriverStandings']
            for j in standings:
                if j['Driver']['code'] not in standings_dict:
                    if i > 1:
                        num = i - 1
                        standings_dict[j['Driver']['code']] = [0] * num
                        standings_dict[j['Driver']['code']].append(j['points'])
                    else:
                        standings_dict[j['Driver']['code']] = [j['points']]
                else:
                    if len(standings_dict[j['Driver']['code']]) < (i - 1):
                        num_missing = (i + 1) - len(standings_dict[j['Driver']['code']])
                        print(num_missing)
                        standings_dict[j['Driver']['code']] = standings_dict[j['Driver']['code']] + [0] * num_missing
                        standings_dict[j['Driver']['code']].append(j['points'])
                    else:
                        standings_dict[j['Driver']['code']].append(j['points'])
        except IndexError:
            break
    
    df_drivers = pd.DataFrame.from_dict(standings_dict, orient='index')
    df_drivers.columns = df_drivers.columns + 1
    df_drivers[df_drivers.columns] = df_drivers[df_drivers.columns].apply(pd.to_numeric)
    df_drivers.sort_values(by=df_drivers.columns[-1], ascending=False, inplace=True)
    return df_drivers

# Get constructors standings
def update_constructor_standings(rounds):
    standings_dict = {}
    for i in range(1, rounds+1):
        try:
            r = ergast_retrieve(f'current/{i}/constructorStandings')
            standings = r['StandingsTable']['StandingsLists'][0]['ConstructorStandings']
            for i in standings:
                if i['Constructor']['name'] not in standings_dict:
                    standings_dict[i['Constructor']['name']] = [i['points']]
                else:
                    standings_dict[i['Constructor']['name']].append(i['points'])
        except IndexError:
            break
        
    df_constructors = pd.DataFrame.from_dict(standings_dict, orient='index')
    df_constructors.columns = df_constructors.columns + 1
    df_constructors[df_constructors.columns] = df_constructors[df_constructors.columns].apply(pd.to_numeric)
    df_constructors.sort_values(by=df_constructors.columns[-1], ascending=False, inplace=True)
    return df_constructors

start = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
print(f"{start} - Beginning of script")
print('----------------------------------------------------------------')
time.sleep(1)
print('Getting drivers standings...')
df_drivers = update_driver_standings(22)
df_drivers.to_csv('/home/guillaume/Python_Projects/Jedha_F1_Project/data/drivers_standings.csv')
print('Done!')
print('Getting constructors standings...')
df_constructors = update_constructor_standings(22)
df_constructors.to_csv('/home/guillaume/Python_Projects/Jedha_F1_Project/data/constructors_standings.csv')
print('Done!')

print('Uploading...')
session = boto3.Session()
s3 = boto3.resource('s3')
s3.Bucket('f1-jedha-bucket').upload_file('/home/guillaume/Python_Projects/Jedha_F1_Project/data/constructors_standings.csv', 'data/constructors_standings.csv', ExtraArgs={'GrantRead': 'uri="http://acs.amazonaws.com/groups/global/AllUsers"'})
s3.Bucket('f1-jedha-bucket').upload_file('/home/guillaume/Python_Projects/Jedha_F1_Project/data/drivers_standings.csv', 'data/drivers_standings.csv', ExtraArgs={'GrantRead': 'uri="http://acs.amazonaws.com/groups/global/AllUsers"'})
print('Done!')
print('----------------------------------------------------------------')
time.sleep(1)
end = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
print(f"{end} - End of script")
print('\n')
print('\n')