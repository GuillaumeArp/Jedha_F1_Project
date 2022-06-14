# import des librairies

import pandas as pd
import plotly.express as px

# fonction de calcul du temps
def decoupe(seconde):
    heure = seconde /3600
    seconde %= 3600
    minute = seconde/60
    seconde%=60
    return (heure,minute,seconde)

# import du dataframe avec les simuls de temps total
df_timerace_import = pd.read_csv('D:\Data analyst\Jedha\Projet\Projet F1\Data\df_timerace.csv', sep = ",", index_col = 0)
df_timerace_import = df_timerace_import.sort_values(['Total_time'], ascending=True)

# création du dataframe avec les 2 temps retenus
df_final = pd.DataFrame(columns=['combiTyre','Train1', 'Train2', 'Train3','TimeT1', 'TimeT2', 'TimeT3', 'Total_time', 'Total_tour'])
df_finalT2 = df_timerace_import[df_timerace_import['Train3']!=0].sort_values(['Total_time'], ascending=True)
df_finalT3 = df_timerace_import[df_timerace_import['Train3']==0].sort_values(['Total_time'], ascending=True)
df_final = df_final.append(df_finalT2.iloc[0,:])
df_final = df_final.append(df_finalT3.iloc[0,:])

# calcul du temps total par course
totalTimeT2 = df_final.iloc[0,7]
totalTimeT3 = df_final.iloc[1,7]

heure = str(int(decoupe(totalTimeT2)[0]))
minute = str(int(decoupe(totalTimeT2)[1]))
seconde = str(round((decoupe(totalTimeT2)[2]),3))
a = 'Total estimated race time : '+ heure + ' h ' + minute + ' mn ' + seconde + ' s  '

heure = str(int(decoupe(totalTimeT3)[0]))
minute = str(int(decoupe(totalTimeT3)[1]))
seconde = str(round((decoupe(totalTimeT3)[2]),3))
b = 'Total estimated race time : '+ heure + ' h ' + minute + ' mn ' + seconde + ' s  '

#Importe les temps au tour par type de pneu
dffp_complet = pd.read_csv('D:\Data analyst\Jedha\Projet\Projet F1\Data\Monaco.csv', sep = ",")


# Mets les temps sous forme de tableau
dffp_soft = dffp_complet[dffp_complet['Compound']=='SOFT']
dffp_soft.drop(columns = ['Compound'], inplace = True)
dffp_soft.rename(columns={'LapTime': 'S'}, inplace = True)

dffp_medium = dffp_complet[dffp_complet['Compound']=='MEDIUM']
dffp_medium.drop(columns = ['Compound'], inplace = True)
dffp_medium.rename(columns={'LapTime': 'M'}, inplace = True)

dffp_hard = dffp_complet[dffp_complet['Compound']=='HARD']
dffp_hard.drop(columns = ['Compound'], inplace = True)
dffp_hard.rename(columns={'LapTime': 'H'}, inplace = True)

dffp_final = dffp_soft.merge(dffp_medium, how = 'inner', left_on = 'TyreLife', right_on = 'TyreLife' )
dffp_final = dffp_final.merge(dffp_hard, how = 'inner', left_on = 'TyreLife', right_on = 'TyreLife' )

# Mets tout les temps au tour dans un dataframe pour la viz

df_viz = pd.DataFrame(columns=['combiTyre','tyreType', 'Tour', 'Time', 'Total_time', 'Id'])
df_vizbis = pd.DataFrame(columns=['combiTyre','tyreType', 'Tour', 'Time', 'Total_time', 'Id'])
df_vizter = pd.DataFrame(columns=['combiTyre','tyreType', 'Tour', 'Time', 'Total_time', 'Id'])
df_viz = df_vizter

for t in range(len(df_final)):

    listCombi = list(df_final.iloc[t,0].strip())
    cpt = 1
    maListe = []
    maListeTypeT = []
    ligneMax = 0

    for tyreType in listCombi:
        if tyreType == "S":
            col = 1
        elif tyreType == "M":
            col = 2
        else :
            col = 3
        


        ligneMax =  int(df_final.iloc[t,cpt])
        cpt += 1
        
        maListeT = dffp_final.iloc[0:ligneMax, col].tolist()
        maListe = maListe + maListeT
        
    
        maListeM = list(len(maListeT) * tyreType.strip())
        
        maListeTypeT = maListeTypeT + maListeM
     

        
    df_vizbis['Time'] = maListe
    df_vizbis['combiTyre'] = df_final.iloc[t,0] #+ str(t+1)
    df_vizbis['Tour'] = df_vizbis.index + 1
    df_vizbis['tyreType'] = maListeTypeT
    df_vizbis['id'] = int(t+1)

    #Ajout du temps d'arrêt

    arr1 = int(df_final.iloc[t,1])
    timeList = df_vizbis['Time'].tolist()
    timeList[arr1] = timeList[arr1]+25

    if  df_final.iloc[t,3] != 0:
        arr1 = int(df_final.iloc[t,2]) + int(df_final.iloc[t,1])
        timeList[arr1] = timeList[arr1]+25
    
    df_vizbis['Time2'] = timeList
    df_vizbis['Total_time'] = df_vizbis['Time2'].cumsum() 
    
    df_viz = pd.concat([df_viz,df_vizbis], ignore_index = True)
    
def estimatedTime(df_viz):
    # Mets le nombre total de tours en variable
    nbTourMax = df_viz['Tour'].max()
        
    # réalise la dataviz
    fig = px.line(df_viz, x= 'Tour', y = 'Time2', color = 'tyreType', width = 1400, height = 800,labels=dict(Time2="Time", Tour = "Lap", combiTyre = "Tyre type"), 
                color_discrete_map = {'S': '#FF3333','M': '#FFF200','H': '#EBEBEB'}, facet_row = 'combiTyre', template = 'plotly_dark')

    fig.update_layout(title_text='Time by lap', title_x=0.5)

    fig.add_vline(x=nbTourMax, line_dash="dot",
                annotation_text=a,
                annotation_position="bottom left", row = 0)

    fig.add_vline(x=nbTourMax, line_dash="dot",
                annotation_text=b,
                annotation_position="bottom left", row = 1)

    return fig

estimatedTime(df_viz)

