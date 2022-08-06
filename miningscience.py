import Bio
from Bio.Seq import Seq
from Bio import Entrez
import re

def download_pubmed (keyword):
    """
    Funcion que pide como entrada las palabra de busqueda en tipo "str" en la base de datos de PUBMED y como output crea un documento 
    que contiene informcacion de la  busqueda
    """ 
    Entrez.email = "lidia.catota@est.ikiam.edu.ec"
    handle = Entrez.esearch(db="pubmed", 
                        term=keyword+"[Title]",## se trabajo unicamente con titulos para delimitar la informacion y evitar gasto computacional 
                        retmax=543,
                        usehistory="y")
    record = Entrez.read(handle)
    id_list = record["IdList"]
    webenv = record["WebEnv"]
    query_key = record["QueryKey"]
    handle = Entrez.efetch(db="pubmed",
                       rettype="medline", 
                       retmode="text", 
                       retstart=0,
                       retmax=543, 
                       webenv=webenv,
                       query_key=query_key)

    out_handle = open("data/"+keyword, "w")
    data = handle.read()
    handle.close()
    out_handle.write(data)
    out_handle.close()
    return id_list

import re 
import csv 
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
from collections import Counter
def map_science(data):
    """
    Funcion que pide como entrada la data de la funcion download_pubmed() y como resultado muestra un grafico de dispersion 
    con la nacionalidad.  
    """ 
    with open("data/"+data, errors="ignore") as l: 
        texto = l.read()
    texto = re.sub(r"\n\s{6}", " ", texto)
    countries_1 = re.findall (r"AD\s{2}-\s[A-Za-z].*,\s([A-Za-z]*)\.\s", texto)
    unique_countries = list(set(countries_1))
    conteo=Counter(countries_1)
    resultado={}
    ## crearemos un diccionario que tendra su key (pais), con su respectivo values (contador)
    for clave in conteo:  
        valor=conteo[clave]
        if valor > 1:
            resultado[clave] = valor
    #colocamos una funcion que nos responda con la longitud y latitud de los paises encontrados
    lugar = Nominatim(user_agent="my_user_agent")
    long = []
    lat = []
    count = []
    for i in resultado.keys():
        lugar = Nominatim(user_agent="my_user_agent")
        loc = lugar.geocode(i)
        long.append(loc.longitude)
        lat.append(loc.latitude)
    for i in resultado.values(): 
        count.append(i*100)
    #return (count)
    plt.scatter(long, lat, s = count, c=count)
    plt.colorbar()
    ## valores de referencia de cinco paises 
    ard = dict(arrowstyle="->")
    plt.annotate('Ecuador', xy = (-79.3666965, -1.3397668), 
               xytext = (-80.25, 20.05), arrowprops = ard)
    plt.annotate('USA', xy = ( -74.006, 40.714), 
               xytext = (-40, 37.4292), arrowprops= ard)
    plt.annotate('Canada', xy = (-107.991707, 61.0666922), 
               xytext = (-73.1106, 48.3736), arrowprops= ard)
    plt.annotate('Japon', xy = (138.252924, 36.204824), 
               xytext = (-100.6847, 30.8369), arrowprops= ard)
    plt.annotate('Egipto', xy = (26.820553, 30.802498), 
               xytext = (10.33, 47.61), arrowprops= ard)
    params = plt.gcf()
    plSize = params.get_size_inches()
    params.set_size_inches( (plSize[0] * 3, plSize[1] * 3) )
    return (plt.savefig("img/"+data, dpi=150, bbox_inches='tight'))
    plt.show()