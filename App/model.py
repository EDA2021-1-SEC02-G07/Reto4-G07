import config as cf
from DISClib.ADT.graph import gr
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Utils import error as error
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newAnalyzer():
    #try:
        analyzer = {
                    'landingPoints': None,
                    'cableNames': None,
                    'cables': None}

        analyzer['landingPoints'] = mp.newMap(numelements=1400,
                                    maptype='PROBING',
                                    comparefunction=LPids)

        analyzer['cableNames'] = mp.newMap(numelements=1400,
                                    maptype='PROBING',
                                    comparefunction=LPids)

        analyzer['cables'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=1400,
                                              comparefunction=LPids)
        return analyzer
    #except Exception as exp:
        #error.reraise(exp, 'model:newAnalyzer')


def addLandingPoint(analyzer, point):
    pointID = point['landing_point_id']
    coord = coordFormat(point)
    #try:
    gr.insertVertex(analyzer['cables'], pointID)

    mp.put(analyzer['landingPoints'], pointID, [coord, point['id'], point['name']])
    
    return analyzer
    #except Exception as exp:
        #error.reraise(exp, 'model:addPoint')


def addCable(analyzer, cable):
    OG = cable['\ufefforigin']
    origin, destination, lenght = OG, cable['destination'], distFormat(cable['cable_length'])

    if not mp.contains(analyzer['cableNames'], cable['cable_id']):
        mp.put(analyzer['cableNames'], cable['cable_id'],
                                [[(OG, cable['destination'])], cable['cable_rfs'], cable['owners'], cable['capacityTBPS']])
    if mp.contains(analyzer['cableNames'], cable['cable_id']):
        value = me.getValue(mp.get(analyzer['cableNames'], cable['cable_id']))
        value[0].append((OG, cable['destination']))
        mp.put(analyzer['cableNames'], cable['cable_id'], value)

    edge = gr.getEdge(analyzer['cables'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['cables'], origin, destination, lenght)

    return analyzer

    

# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos
def coordFormat(point):
    lon, lat = float(point['longitude']), float(point['latitude'])
    return [lon, lat]

def distFormat(length):
    length = length.replace('km', '')
    length = length.strip()
    return length


    
def haversine(coord1, coord2):
    import math

    # Coordinates in decimal degrees (e.g. 2.89078, 12.79797)
    lon1, lat1 = coord1
    lon2, lat2 = coord2

    R = 6371000  # radius of Earth in meters
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)

    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) ** 2
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    meters = R * c  # output distance in meters
    km = meters / 1000.0  # output distance in kilometers

    metersR = round(meters, 3)
    kmR = round(km, 3)


    return km
# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista
def LPids(LPid, keyvaluestop):
    stopcode = keyvaluestop['key']
    if (LPid == stopcode):
        return 0
    elif (LPid > stopcode):
        return 1
    else:
        return -1
# Funciones de ordenamiento
