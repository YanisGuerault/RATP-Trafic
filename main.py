import folium,branca,json
import numpy as np # import package
import matplotlib.pyplot as plt # import module
import math
import tkinter as tk
from tkinter import *

annee = 2017
# filedialog is used in this case to save the file path selected by the user.
#from tkinter import filedialog

#Rapport : les deux figures + commentaires + Intro + Conclusion, cadre, pq on l'a choisit, ce que ca nous a apporté.
"""files = [ 'Trafic.json']

datastation = dict()
for file in files:
    f = open(file, 'r', encoding='utf8')
    g = json.loads(f.read())
    if(file.split(".")[1] == "geojson"):
        geo_data["features"].extend((g["features"])) # add current geojson data to master dict
    elif(file.split(".")[1] == "json"):
        for to in g:
            datastation[to['fields']['station']] = to['fields']
    f.close()"""

#print(datastation['GARE DU NORD']['trafic'])

""" Histogramme """
def CreerHisto(annee):
    CreerDico(annee)
    l = []
    for k in datastationtrafic.keys():
        l.append(datastationtrafic[k]['trafic'])
    
    b = list(range(0,56000000,1000000))
    n, bins, patches = plt.hist(l, bins=b,facecolor='g')
	
    plt.xlabel('Trafic (en dizaine de millions)')
    plt.ylabel('Nombre de stations')
    plt.title('Nombre de stations en fonction du nombre de personnes')
	
    string = "Moyenne="+str(np.mean(l))+",\nEcartType="+str(np.std(l))+"\nMediane="+str(np.median(l))
    plt.text(30000000, 70, string)
    plt.show()
""" Fin Histogramme """

import folium,branca,json,unicodedata,urllib.request,shutil,requests,os, webbrowser
from os.path import basename

def supprime_accent(string):
        """ supprime les accents du texte source """
        accent = ['É','é']
        sans_accent = ['E','e']
        i = 0
        while i < len(accent):
            string = string.replace(accent[i], sans_accent[i])
            i += 1
        return string

def Telecharge(nomfichier,varURL):
    with urllib.request.urlopen(varURL) as response, open(nomfichier+"."+str(response.url.split('format=')[1].split('&')[0]), 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

def CreerDico(annee):
    files = [ 'GARES-METRO.json',
          'GARES-RER.json',
          'trafic.json' ]
    global datastationtrafic
    datastationtrafic = dict()
    global datastationposition
    datastationposition = dict()
    Telecharge("trafic","https://data.ratp.fr/explore/dataset/trafic-annuel-entrant-par-station-du-reseau-ferre-"+str(annee)+"/download/?format=json&timezone=Europe/Berlin")
    Telecharge("GARES-METRO","https://opendata.stif.info/explore/dataset/emplacement-des-gares-idf/download/?format=json&refine.mode=Metro&timezone=Europe/Berlin")
    Telecharge("GARES-RER","https://opendata.stif.info/explore/dataset/emplacement-des-gares-idf/download/?format=json&refine.mode=RER&timezone=Europe/Berlin")

    for file in files:
        f = open(file, 'r', encoding='utf8')
        g = json.loads(f.read())
        if(file.split("-")[0] == "GARES"):
            for to in g:
                if(to['fields']['nomlong'] in datastationposition and to['fields']['reseau'] == "RER"):
                    datastationposition[to['fields']['nomlong']+"-RER"] = {"type":to['fields']['reseau'],"coordonnes":to['fields']['geo_point_2d'],"nom_gare":to['fields']['nom_gare'],"num_gare":to['fields']['gares_id'],"ligne":to['fields']['ligne']}
                else:
                    datastationposition[to['fields']['nomlong']] = {"type":to['fields']['reseau'],"coordonnes":to['fields']['geo_point_2d'],"nom_gare":to['fields']['nom_gare'],"num_gare":to['fields']['gares_id'],"ligne":to['fields']['ligne']}
        else:
            for to in g:
                datastationtrafic[to['fields']['station']] = to['fields']
        f.close()

def CreerMap(annee):
    CreerDico(annee)
    coords = (48.7190835,2.4609723)
    map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=9)

    cmp = 0
    cmp2 = 0
    for station in datastationposition:
        for trafic in datastationtrafic:
            stationNameTrafic = supprime_accent(trafic).upper()
            stationNameCoorLong = supprime_accent(station).upper()
            stationNameCoorNomGare = supprime_accent(datastationposition[station]["nom_gare"]).upper()

            if(stationNameTrafic[-3:]== "RER"):
                stationNameTrafic = stationNameTrafic[:-4]
            if(stationNameCoorLong == "2"):
                print(str(datastationposition[station]))
            if((stationNameTrafic == stationNameCoorLong or stationNameCoorNomGare == stationNameTrafic) or (stationNameTrafic in stationNameCoorLong or stationNameTrafic in stationNameCoorNomGare)):
                cmp=cmp+1
                icon=folium.Icon(color='white')
                if(datastationposition[station]['type'] == "RER"):
                     icon=folium.Icon(color='green', prefix='fa',icon='train')
                else:
                    icon=folium.Icon(color='cadetblue', prefix='fa',icon='subway')
                iframe = stationNameTrafic
                folium.Marker(
                location=datastationposition[station]['coordonnes'],
                popup=datastationposition[station]['type']+" : "+str(datastationtrafic[trafic]['trafic']),
                icon=icon
                ).add_to(map)
                print(str(datastationposition[station]['nom_gare']))
    print(cmp)
    print(cmp2)

    map.save(outfile='trafic-metro-rer.html')
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    webbrowser.get(chrome_path).open('trafic-metro-rer.html') 
#Tk allows you to register and unregister a callback function which will be called from the Tk mainloop when I/O is possible on a file descriptor
def CreerGUI():
    mainw= Tk()
    mainw.title('Trafic des stations RATP en 2017')
    ANNEES = [
        "2017",
        "2016",
        "2015",
        "2014"
    ]
    anneeselect = StringVar()
    anneeselect.set(ANNEES[0])
    w = OptionMenu(mainw,anneeselect,*ANNEES).pack()
    # create Button that link to methods used to process said file.
    tk.Button(mainw, text="Carte", command= lambda: CreerMap(anneeselect.get()),padx = 150, pady = 50).pack()
    tk.Button(mainw, text="Histo", command= lambda: CreerHisto(anneeselect.get()),padx = 150, pady = 50).pack()

    """menubar = Menu(fenetre)
    menu1 = Menu(mainw, tearoff=0)
    menu1.add_command(label="2014")
    menu1.add_command(label="2015")
    menu1.add_command(label="2016")
    fenetre.config(menu=menubar)"""
    mainw.mainloop()


CreerGUI()

