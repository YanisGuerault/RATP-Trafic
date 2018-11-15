import folium,branca,json

files = [ 'GARES-RER.geojson',
          'GARES-METRO.geojson',
          'trafic.json' ]
#files = ['france-geojson-master/departements/75-paris/communes-75-paris.geojson',
    #'france-geojson-master/departements/77-seine-et-marne/communes-77-seine-et-marne.geojson',
    #'france-geojson-master/departements/78-yvelines/communes-78-yvelines.geojson',
    #'france-geojson-master/departements/91-essonne/communes-91-essonne.geojson',
    #'france-geojson-master/departements/92-hauts-de-seine/communes-92-hauts-de-seine.geojson',
    #'france-geojson-master/departements/93-seine-saint-denis/communes-93-seine-saint-denis.geojson',
    #'france-geojson-master/departements/94-val-de-marne/communes-94-val-de-marne.geojson',
    #'france-geojson-master/departements/95-val-d-oise/communes-95-val-d-oise.geojson']

""" coords = (48.7453229,2.5073644)
map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=9)

#style function
sf = lambda x :{'fillColor':'#E88300', 'fillOpacity':0.5, 'color':'#E84000', 'weight':1, 'opacity':1}

i = 0

for overlay in files :

    folium.GeoJson(
        data=overlay,
        name=overlay,
        popup="CCC",
        style_function= sf
    ).add_to(map)
    print(i)
    i=i+1 """

coords = (48.7190835,2.4609723)
map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=9)

geo_data = {"type": "FeatureCollection", "features": []} # master dict structure
datastation = dict()
for file in files:
    f = open(file, 'r', encoding='utf8')
    g = json.loads(f.read())
    if(file.split(".")[1] == "geojson"):
        geo_data["features"].extend((g["features"])) # add current geojson data to master dict
    elif(file.split(".")[1] == "json"):
        for to in g:
            datastation[to['fields']['station']] = to['fields']
    f.close()

print(datastation['GARE DU NORD']['trafic'])
"""map.choropleth(
    geo_data=geo_data,
    name='choropleth',
    #data=datastation,
    columns=['reseau', 'trafic'], # data key/value pair
    #key_on='feature.properties.reseau', # corresponding layer in GeoJSON
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Population'
)"""

sf = lambda x :{'fillColor':'#E88300', 'fillOpacity':0.5, 'color':'#E84000', 'weight':1, 'opacity':1}
folium.GeoJson(
        data=geo_data,
        name="BONSOIR",
        style_function= sf
    ).add_to(map)

map.save(outfile='map.html')