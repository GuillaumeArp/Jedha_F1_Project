#Import
import fastf1 as ff1
import pandas as pd
import warnings
import datetime
import boto3
import time
warnings.simplefilter(action='ignore', category=FutureWarning)
ff1.Cache.enable_cache('/home/guillaume/Python_Projects/Jedha_F1_Project/cache/')

# Définition des variables
events_list = pd.DataFrame(ff1.get_event_schedule(2022)[2:])
dict_nb_laps = {1: 57, 2: 50, 3: 58, 4: 63, 5: 57, 6: 66, 7: 78, 8: 51, 9: 70, 10: 52, 11: 71, 12: 53, 13: 70, 14: 44, 15: 72, 16: 53, 17: 61, 18: 53, 19: 56, 20: 71, 21: 71, 22: 58}
dict_pit_stops_time = {1: 25, 2: 21, 3: 22, 4: 25, 5: 25, 6: 22, 7: 24, 8: 20, 9: 24, 10: 29, 11: 21, 12: 30, 13: 22, 14: 23, 15: 19, 16: 25, 17: 29, 18: 24, 19: 24, 20: 23, 21: 23, 22: 22}

session = boto3.Session()
s3 = boto3.resource('s3')

start = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
print(f"{start} - Beginning of script")
print('----------------------------------------------------------------')
time.sleep(1)

for event in events_list.itertuples():
    
    try:
        gp_round = event.RoundNumber
        tourTot = dict_nb_laps[gp_round]
        perteArret = dict_pit_stops_time[gp_round]

        #Génère le nombre de tour avec 2 arrêts
        df_combi = pd.DataFrame(columns=['Train1', 'Train2', 'Train3'])

        for i in range(1,tourTot-1):
            T1 = i
            for j in range(1, tourTot-1):        
                if (i+j) > tourTot-1:
                    continue
                T2 = j
                T3 = tourTot - j - i
                df_combi = df_combi.append({'Train1' : T1, 'Train2' : T2, 'Train3' : T3}, ignore_index = True)
                        
        #Génère le nombre de tour avec 1 arrêt
        df_combi2 = pd.DataFrame(columns=['Train1', 'Train2'])

        for i in range(1,tourTot):
            T1 = i
            T2 = tourTot-i
            df_combi2 = df_combi2.append({'Train1' : T1, 'Train2' : T2}, ignore_index = True)        

        # Ouvre le csv avec le temps par tour et type de pneu
        dffp_complet = pd.read_csv(f'https://f1-jedha-bucket.s3.eu-west-3.amazonaws.com/data/tyre_life_data_{gp_round}.csv', index_col=0)

        # Mets les temps sous forme de tableau
        dffp_soft = dffp_complet[dffp_complet['Tyre'] == 'SOFT'].copy()
        dffp_soft.drop(columns = ['Tyre', 'LapTimeSeconds', 'DeltaDeg', 'TimeStr', 'FinalLapTime'], inplace = True)
        dffp_soft.rename(columns={'AdjustedTime': 'S', 'Lap': 'TyreLife'}, inplace = True)

        dffp_medium = dffp_complet[dffp_complet['Tyre'] == 'MEDIUM'].copy()
        dffp_medium.drop(columns = ['Tyre', 'LapTimeSeconds', 'DeltaDeg', 'TimeStr', 'FinalLapTime'], inplace = True)
        dffp_medium.rename(columns={'AdjustedTime': 'M', 'Lap': 'TyreLife'}, inplace = True)

        dffp_hard = dffp_complet[dffp_complet['Tyre'] == 'HARD'].copy()
        dffp_hard.drop(columns = ['Tyre', 'LapTimeSeconds', 'DeltaDeg', 'TimeStr' ,'FinalLapTime'], inplace = True)
        dffp_hard.rename(columns={'AdjustedTime': 'H', 'Lap': 'TyreLife'}, inplace = True)

        dffp_final = dffp_soft.merge(dffp_medium, how = 'inner', left_on = 'TyreLife', right_on = 'TyreLife')
        dffp_final = dffp_final.merge(dffp_hard, how = 'inner', left_on = 'TyreLife', right_on = 'TyreLife')
        dffp_final.drop(columns = ['FuelDeg_y', 'FuelDeg_x'], inplace = True)
        dffp_final = dffp_final[['TyreLife', 'S', 'M', 'H', 'FuelDeg']]

        #Ouvre le csv avec les combinaisons pour 1 arrêts
        tyreCombi2 = pd.read_csv('/home/guillaume/Python_Projects/Jedha_F1_Project/data/TyreCombi2.csv', sep = ";")

        #Ouvre le csv avec les combinaisons pour 2 arrêts
        tyreCombi3 = pd.read_csv('/home/guillaume/Python_Projects/Jedha_F1_Project/data/TyreCombi3.csv', sep = ";")

        # Boucle sur tous les types de pneu pour 2 arrêts afin de générer tous les temps totaux pour la course
        time1 = 0
        time2 = 0
        time3 = 0
        listeT = []
        df_timerace3 = pd.DataFrame(columns=['combiTyre','Train1', 'Train2', 'Train3','TimeT1', 'TimeT2', 'TimeT3', 'Total_time'])
        df_timeracebis = pd.DataFrame(columns=['combiTyre','Train1', 'Train2', 'Train3','TimeT1', 'TimeT2', 'TimeT3', 'Total_time'])
        df_timeraceter = pd.DataFrame(columns=['combiTyre','Train1', 'Train2', 'Train3','TimeT1', 'TimeT2', 'TimeT3', 'Total_time'])
        df_timerace3 = df_timeraceter

        #Boucle sur le df tyre_combi
        for a in range(len(tyreCombi3)):
            lig = a
            df_timeracebis = pd.DataFrame(columns=['combiTyre','Train1', 'Train2', 'Train3','TimeT1', 'TimeT2', 'TimeT3', 'Total_time'])

            # Calcul du T1 en fonction du type de pneu 
            col = 0
            liste_combi = []
            liste_combi.append(tyreCombi3.iloc[lig,col])
            
            if tyreCombi3.iloc[lig,col] == 'S':
                colT = 1
            elif tyreCombi3.iloc[lig,col] == 'M':
                colT = 2
            else :
                colT = 3
                
            #Boucle sur la longueur du df
            for l in range(len(df_combi)):
                #nombre de tour égal à la valeur de la 1ère colonne
                nbTour = df_combi.iloc[l,0]
                    
                #Addition des nbTours premières lignes            
                for i in range(nbTour):
                    time1 += dffp_final.iloc[i,colT]      
                    
                df_timeracebis = df_timeracebis.append({'TimeT1' : time1}, ignore_index = True)
                df_timeracebis.iloc[l,1] = nbTour
                time1 = 0
                
                
        # Calcul du T2 en fonction du type de pneu        
            col = 1
            liste_combi.append(tyreCombi3.iloc[lig,col])
            
            if tyreCombi3.iloc[lig,col] == 'S':
                colT = 1
            elif tyreCombi3.iloc[lig,col] == 'M':
                colT = 2
            else :
                colT = 3        
                
            #Boucle sur la longueur du df    
            for l in range(len(df_combi)):
                #nombre de tour égal à la valeur de la 1ère colonne
                nbTour = df_combi.iloc[l,1]
                
                #Addition des nbTours premières lignes    
                for i in range(nbTour):
                    time2 = time2 + dffp_final.iloc[i,colT]
                    
                df_timeracebis.iloc[l,5] = time2
                df_timeracebis.iloc[l,2] = nbTour
                time2 = 0        
                
        # Calcul du T3 en fonction du type de pneu        
            col = 2
            liste_combi.append(tyreCombi3.iloc[lig,col])
            
            if tyreCombi3.iloc[lig,col] == 'S':
                colT = 1
            elif tyreCombi3.iloc[lig,col] == 'M':
                colT = 2
            else :
                colT = 3        
            
            #Boucle sur la longueur du df    
            for l in range(len(df_combi)):
                #nombre de tour égal à la valeur de la 1ère colonne
                nbTour = df_combi.iloc[l,2]
                
                #Addition des nbTours premières lignes
                
                for i in range(nbTour): #J'itère autant de fois qu'il y a de tours
                    time3 = time3 + dffp_final.iloc[i,colT]
                    
                df_timeracebis.iloc[l,6]=time3
                df_timeracebis.iloc[l,3] = nbTour
                time3 = 0
                
                df_timeracebis.iloc[l,0] = "".join(liste_combi)

            df_timerace3 = pd.concat([df_timerace3,df_timeracebis], ignore_index = True)

        #Calcul du temps total
        df_timerace3['Total_time'] = df_timerace3['TimeT1'] + df_timerace3['TimeT2'] + df_timerace3['TimeT3'] + ( 2 * perteArret)

        # Boucle sur tous les types de pneu pour 2 arrêts afin de générer tous les temps totaux pour la course
        time1 = 0
        time2 = 0
        time3 = 0
        listeT = []
        df_timerace2 = pd.DataFrame(columns=['combiTyre','Train1', 'Train2', 'Train3','TimeT1', 'TimeT2', 'TimeT3', 'Total_time'])
        df_timeracebis = pd.DataFrame(columns=['combiTyre','Train1', 'Train2', 'Train3','TimeT1', 'TimeT2', 'TimeT3', 'Total_time'])
        df_timeracequa = pd.DataFrame(columns=['combiTyre','Train1', 'Train2', 'Train3','TimeT1', 'TimeT2', 'TimeT3', 'Total_time'])
        df_timerace2 = df_timeracequa

        #Boucle sur le df tyre_combi
        for a in range(0,len(tyreCombi2)):
            lig = a
            df_timeracebis = df_timeraceter

            # Calcul du T1 en fonction du type de pneu 
            col = 0
            liste_combi = []
            liste_combi.append(tyreCombi2.iloc[lig,col])
            
            if tyreCombi2.iloc[lig,col] == 'S':
                colT = 1
            elif tyreCombi2.iloc[lig,col] == 'M':
                colT = 2
            else :
                colT = 3
                
            #Boucle sur la longueur du df
            for l in range(len(df_combi2)):
                #nombre de tour égal à la valeur de la 1ère colonne
                nbTour = df_combi2.iloc[l,0]
                    
                #Addition des nbTours premières lignes
                    
                for i in range(nbTour):
                    time1 = time1 + dffp_final.iloc[i,colT]      
                    
                df_timeracebis = df_timeracebis.append({'TimeT1' : time1}, ignore_index = True)
                df_timeracebis.iloc[l,1] = nbTour
                time1 = 0        
                
        # Calcul du T2 en fonction du type de pneu        
            col = 1
            liste_combi.append(tyreCombi2.iloc[lig,col])
            
            if tyreCombi2.iloc[lig,col] == 'S':
                colT = 1
            elif tyreCombi2.iloc[lig,col] == 'M':
                colT = 2
            else :
                colT = 3
                        
            #Boucle sur la longueur du df    
            for l in range(len(df_combi2)):
                #nombre de tour égal à la valeur de la 2ème colonne
                nbTour = df_combi2.iloc[l,1]
                
                #Addition des nbTours premières lignes        
                for i in range(nbTour):
                    time2 += dffp_final.iloc[i,colT]
                    
                df_timeracebis.iloc[l,5] = time2
                df_timeracebis.iloc[l,2] = nbTour
                time2 = 0
                        
        # Génération du Train3 et Time3 à 0      
            
            #Boucle sur la longueur du df    
            for l in range(len(df_combi2)):        
                    
                df_timeracebis.iloc[l,6]=0
                df_timeracebis.iloc[l,3] = 0
                
                
                df_timeracebis.iloc[l,0] = "".join(liste_combi)

            df_timerace2 = pd.concat([df_timerace2,df_timeracebis], ignore_index = True)

        #Calcul du temsp total
        df_timerace2['Total_time'] = df_timerace2['TimeT1'] + df_timerace2['TimeT2'] + df_timerace2['TimeT3']  + ( perteArret)


        #Concatène les 2 df
        df_timerace2 = df_timerace2.sort_values(by='Total_time', ascending=True)
        df_timerace3 = df_timerace3.sort_values(by='Total_time', ascending=True)
        df_timerace = pd.concat([df_timerace2,df_timerace3], ignore_index = True)

        #Retrait du temps gagné par la consommation d'essence
        total_fuel = dffp_final['FuelDeg'].sum()
        df_timerace['Total_time'] = df_timerace['Total_time'] - total_fuel

        #Garde uniquement les deux meilleures stratégies à un et deux arrêts
        df_final = pd.concat([df_timerace[df_timerace['Train3'] == 0].iloc[:2], df_timerace[df_timerace['Train3'] != 0].iloc[:2]]).reset_index(drop=True).drop([1, 3], axis=0).reset_index(drop=True).sort_values(by='Total_time', ascending=True)
        df_final['TotalTimeStr'] = df_final['Total_time'].apply(lambda x: str(datetime.timedelta(seconds=x))[:-3])

        #Export du csv
        csv_times = f'predicted_strategy_round_{gp_round}.csv'
        df_final.to_csv('/home/guillaume/Python_Projects/Jedha_F1_Project/data/' + csv_times)
        print(f'{csv_times} written')
        
        full_path = '/home/guillaume/Python_Projects/Jedha_F1_Project/data/' + csv_times
        s3.Bucket('f1-jedha-bucket').upload_file(full_path, f'data/{csv_times}', ExtraArgs={'GrantRead': 'uri="http://acs.amazonaws.com/groups/global/AllUsers"'})
        print(f'{csv_times} uploaded \n')
    
    except Exception as e:
        print(e)
        break
    
print('----------------------------------------------------------------')
time.sleep(1)
end = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
print(f"{end} - End of script")
print('\n')
print('\n')