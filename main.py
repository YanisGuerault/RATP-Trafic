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

def CreerMap():
    files = [ 'GARES-METRO.json',
          'GARES-RER.json',
          'trafic.json' ]

    coords = (48.7190835,2.4609723)
    map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=9)

    global datastationtrafic
    datastationtrafic = dict()
    global datastationposition
    datastationposition = dict()
    Telecharge("trafic","https://data.ratp.fr/explore/dataset/trafic-annuel-entrant-par-station-du-reseau-ferre-2017/download/?format=json&timezone=Europe/Berlin")
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
                     icon=folium.Icon(color='lightgray', prefix='fa',icon='train')
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
    webbrowser.open('trafic-metro-rer.html') 

CreerMap()
#help(folium.Icon)