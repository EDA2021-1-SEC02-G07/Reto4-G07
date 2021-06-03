from DISClib.DataStructures.chaininghashtable import contains
import config as cf
from DISClib.ADT.graph import gr
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import quicksort as quick
from DISClib.Algorithms.Graphs import prim as pr
from DISClib.Algorithms.Graphs import bellmanford as bell
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
                    'LPnames': None,
                    'cableNames': None,
                    'cables': None}

        analyzer['landingPoints'] = mp.newMap(numelements=1400,
                                    maptype='PROBING',
                                    comparefunction=LPids)
        
        analyzer['LPnames'] = mp.newMap(numelements=1400,
                                    maptype='PROBING',
                                    comparefunction=LPids)

        analyzer['cableNames'] = mp.newMap(numelements=1400,
                                    maptype='PROBING',
                                    comparefunction=LPids)

        analyzer['cables'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=1400,
                                              comparefunction=LPids)

        analyzer['paises'] = mp.newMap(numelements=237, maptype='PROBING', comparefunction= LPids)

        analyzer['distancias'] = gr. newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=1400,
                                              comparefunction=LPids)
        
        return analyzer
    #except Exception as exp:
        #error.reraise(exp, 'model:newAnalyzer')


def addLandingPoint(analyzer, point):
    pointID = int(point['landing_point_id'])
    pointN = point['name']
    coord = coordFormat(point)
    #try:
    gr.insertVertex(analyzer['cables'], pointID)

    mp.put(analyzer['landingPoints'], pointID, [coord, point['id'], point['name']])
    mp.put(analyzer['LPnames'], pointN, pointID)
    
    return analyzer
    #except Exception as exp:
        #error.reraise(exp, 'model:addPoint')


def addCable(analyzer, cable):
    OG = cable['\ufefforigin']
    origin, destination, lenght = int(OG), int(cable['destination']), distFormat(cable['cable_length'])

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

def addPais(analyzer, pais):
    
    if not mp.contains(analyzer['paises'], pais['CountryName']):
        mp.put(analyzer['paises'], pais['CountryName'], [pais['CapitalName'], pais['Internet users'], pais['Population']])
        #primera posiciòn contiene capital, segunda numero de usuarios de internet y la tercera contiene poblaciòn 
        
  
def addDistance(analyzer, cable):
    #añadir distancia y asi poder agregar un grafo con peso
    print(cable)


# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos
def coordFormat(point):
    lon, lat = float(point['longitude']), float(point['latitude'])
    return [lon, lat]

def distFormat(length):
    import math
    if length == 'n.a.':
            length = round(math.log(12) * (10**4))
    else:
        length = length.replace('km', '').replace(',', '')
        length = float(length)

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
def LPs(analyzer):
    LPs = gr.vertices(analyzer['cables'])
    ltDeg = lt.newList('ARRAY_LIST', cmpfunction=LPids)
    for vertex in lt.iterator(LPs):
        lt.addLast(ltDeg, (vertex, gr.degree(analyzer['cables'], vertex)))

    ltDegO = sortMaster(ltDeg, cmpDeg)
    return ltDegO

def fallas(analyzer, name):
    LPid = me.getValue(mp.get(analyzer['LPnames'], name))
    afectados = gr.adjacents(analyzer['cables'], LPid)
    paises = mp.newMap(37,comparefunction=LPids)
    paisesSet = set()
    ltSort = lt.newList('ARRAY_LIST', cmpfunction=LPids)
    for vertex in lt.iterator(afectados):
        pais = me.getValue(mp.get(analyzer['landingPoints'], vertex))[2]
        pais = pais.split(',')[1].strip()
        paisesSet.add(pais)
        arc = gr.getEdge(analyzer['cables'], LPid, vertex)
        if mp.contains(paises, pais):
            lt.addLast(me.getValue(mp.get(paises, pais)), arc)
        if not mp.contains(paises, pais):
            mp.put(paises, pais, lt.newList('ARRAY_LIST', cmpfunction=LPids))
            lt.addLast(me.getValue(mp.get(paises, pais)), arc)
    
    for pais in paisesSet:
        ltP = me.getValue(mp.get(paises, pais))
        ltPO = sortMaster(ltP, cmpArcW)
        mp.put(paises, pais, ltPO)
        primero = lt.firstElement(ltPO)
        lt.addLast(ltSort, (pais, primero))
    
    ltFinal = sortMaster(ltSort, cmpWtuple)

    return len(list(paisesSet)), ltFinal
    
def InfCrit(analyzer):
    inf = pr.PrimMST(analyzer['cables'])
    LPs = gr.vertices(analyzer['cables'])
    tree = lt.newList('ARRAY_LIST', cmpfunction=LPids)
    total = 0
    for vertex in lt.iterator(LPs):
        distance = bell.distTo(inf, vertex)
        if distance != 0: #El algoritmo prim pone 0, asumimos que los que se mantienen en 0 son porque no pertenecen al MST
            lt.addLast(tree, (vertex, distance))
            total += distance
    treeO = sortMaster(tree, cmpDeg)

    return lt.size(tree), total, lt.firstElement(treeO), lt.lastElement(treeO)

def clusterL(analyzer, point1, point2):
    data = mp.keySet(analyzer['cableNames'])
    for cable in lt.iterator(data):
        print(cable)
        info = mp.get(analyzer['cableNames'], cable)
        print(info)


def distPais(analyzer, A, B):
    pass
    data = mp.valueSet(analyzer['landingPoints'])
    grafo = analyzer['cables']
    #distancia de ciudades a 
    
    for info in lt.iterator(data):
        ubi = info[2]
        ubi = ubi.lower()
        if A in ubi:
            cordi = info[0]
            lt.addLast(ciudadesA, [ubi, cordi])
        elif B in ubi:
            cordi = info[0]
            lt.addLast(ciudadesB, [ubi, cordi])

    print(ciudadesA, ciudadesB)





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
def cmpDeg(d1, d2):
    result = float(d1[1]) > float(d2[1])
    return result

def cmpArcW(w1, w2):
    result = float(w1['weight']) > float(w2['weight'])
    return result
def cmpWtuple(a1, a2):
    result = float(a1[1]['weight']) > float(a2[1]['weight'])
    return result
def sortMaster(lista, cmp):
    lista = lista.copy()
    quick.sort(lista, cmp)
    return lista