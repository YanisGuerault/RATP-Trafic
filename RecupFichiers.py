
# Télécharger un fichier provenant de l'API et mettre dans un fichier spécifique (racine du projet)
# Le Renommer (car quand on télécharge, le nom peut varier)
# https://stackoverflow.com/questions/22676/how-do-i-download-a-file-over-http-using-python
# https://www.codementor.io/aviaryan/downloading-files-from-urls-in-python-77q3bs0un
# https://stackoverflow.com/questions/7243750/download-file-from-web-in-python-3
# pip install requests

import urllib.request
import shutil
import requests
from os.path import basename


def Telecharge(nomfichier,varURL):
    with urllib.request.urlopen(varURL) as response, open(nomfichier+"."+str(response.url.split('format=')[1].split('&')[0]), 'wb') as out_file:
        shutil.copyfileobj(response, out_file)



if __name__ == '__main__':
    Telecharge("Trafic","https://data.ratp.fr/explore/dataset/trafic-annuel-entrant-par-station-du-reseau-ferre-2017/download/?format=csv&timezone=Europe/Berlin&use_labels_for_header=true")
