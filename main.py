import numpy as np # import package
import matplotlib.pyplot as plt # import module
import math
import tkinter as tk
from tkinter import *

import folium,branca,json,unicodedata,urllib.request,shutil,requests,os, webbrowser
from os.path import basename

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
	
    string = "Moyenne="+str(round(np.mean(l),2))+",\nEcartType="+str(round(np.std(l),2))+"\nMediane="+str(round(np.median(l),2))
    plt.text(30000000, 70, string)

    plt.show()
""" Fin Histogramme """

"""Permet de supprimer les accents des noms de stations"""
def supprime_accent(string):
        """ supprime les accents du texte source """
        accent = ['É','é']
        sans_accent = ['E','e']

        i = 0
        while i < len(accent):
            string = string.replace(accent[i], sans_accent[i])
            i += 1

        return string

"""Telecharge et stock un fichier avec le nom passer en paramètre"""
def Telecharge(nomfichier,varURL):
    with urllib.request.urlopen(varURL) as response, open(nomfichier+"."+str(response.url.split('format=')[1].split('&')[0]), 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
"""Permet de creer (ou recreer) les dictionnaires des stations en fonction de l'année en paramètre"""
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

"""Permet de creer une carte en fonction de l'année en paramètres"""
def CreerMap(annee):
    CreerDico(annee)

    coords = (48.858273, 2.347211)
    map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=13,min_zoom=12)

    for station in datastationposition:
        for trafic in datastationtrafic:

            stationNameTrafic = supprime_accent(trafic).upper()
            stationNameCoorLong = supprime_accent(station).upper()
            stationNameCoorNomGare = supprime_accent(datastationposition[station]["nom_gare"]).upper()

            if(stationNameTrafic[-3:]== "RER"):
                stationNameTrafic = stationNameTrafic[:-4]

            if((stationNameTrafic == stationNameCoorLong or stationNameCoorNomGare == stationNameTrafic) or (stationNameTrafic in stationNameCoorLong or stationNameTrafic in stationNameCoorNomGare)):
                
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

    map.save(outfile='trafic-metro-rer.html')
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    webbrowser.get(chrome_path).open('trafic-metro-rer.html') 

"""Permet de générer la GUI Tkinter"""
def CreerGUI():
    ANNEES = [
        "2017",
        "2016",
        "2015",
        "2014"
    ]

    mainw= Tk()
    mainw.title('Trafic des stations RATP en 2017')

    anneeselect = StringVar()
    anneeselect.set(ANNEES[0])

    w = OptionMenu(mainw,anneeselect,*ANNEES).pack()

    tk.Button(mainw, text="Carte", command= lambda: CreerMap(anneeselect.get()),padx = 150, pady = 50).pack()
    tk.Button(mainw, text="Histo", command= lambda: CreerHisto(anneeselect.get()),padx = 150, pady = 50).pack()
    
    mainw.mainloop()


CreerGUI()