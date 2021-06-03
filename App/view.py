import config as cf
import sys
import controller
from DISClib.ADT.graph import gr
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
assert cf

YELLOW = '\033[93m'
BOLD = '\033[1m'
END = '\033[0m'
"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("\nBienvenido")
    print("1- Cargar información en el catálogo.")
    print("2- Identificar clústeres de comunicación.")
    print("3- Identificar puntos de conexión críticos")
    print("4- Identificar ruta de menor distancia.")
    print("5- Identificar infraesrtuctira crítica.")
    print("6- Análisis de fallas.")
    print("7- Identificar mejores canales de transmisión.")
    print("8- Identificar mejor ruta de comunicación.")
    print("9- Graficar.")
    print("0- Salir.")

catalog = None
pointFile = 'landing_points.csv'
connectFile = 'connections.csv'
countryFile = 'countries.csv'
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        analyzer = controller.init()
        print("\nCargando información de los archivos...")
        analyzer = controller.loadData(analyzer, pointFile, connectFile, countryFile)
        LPs = gr.numVertices(analyzer['cables'])
        ARCs = gr.numEdges(analyzer['cables'])
        vertex = lt.firstElement(gr.vertices(analyzer['cables']))
        infoV = me.getValue(mp.get(analyzer['landingPoints'], vertex))
        last = lt.lastElement(mp.keySet(analyzer['paises']))
        infoL = mp.get(analyzer['paises'], last)
        infoL = infoL['value']
        print(infoL)
        print(f'El número total de Landing Points es {YELLOW}{LPs}{END}.')
        print(f'El número total de conexiones es {YELLOW}{ARCs}{END}.')
        print(f'En primer Landing Point tiene el identificador {YELLOW}{vertex}{END}.\nNombre: {YELLOW}{infoV[2]}{END}.\nID: {YELLOW}{infoV[1]}{END}.\
        \nLatitud: {YELLOW}{infoV[0][1]}{END}.\nLongitud: {YELLOW}{infoV[0][0]}{END}.')
        print(f'El último país cargado es: {YELLOW}{last}{END}. \nPoblación: {YELLOW}{infoL[2]}{END}. \nUsuarios de internet: {YELLOW}{infoL[1]}{END}.')
    
    elif int(inputs[0]) == 2:
        point1 = input("Ingrese el primer LandingPoint: ")
        point2 = input("Ingrese el segundo landingPoint: ")
        ans = controller.callClusterL(analyzer, point1, point2)

    elif int(inputs[0]) == 3:
        LPs = controller.getLPs(analyzer)
        print('Los 10 vértices con más Landing Points conectados son:\n')
        i = 0
        for vertex in lt.iterator(LPs):
            vertexN = me.getValue(mp.get(analyzer['landingPoints'], vertex[0]))[2]
            if i >= 10:
                break
            print(f'{i+1}. El vértice {YELLOW}{vertexN}{END} identificado con el número {YELLOW}{vertex[0]}{END} está conectado a {YELLOW}{vertex[1]}{END} Landing Points.')
            i +=1
    elif int(inputs[0]) == 4:
        pass
    elif int(inputs[0]) == 5:
        infCrit = controller.getInfCrit(analyzer)
    elif int(inputs[0]) == 6:
        name = input('Escriba el nombre del Landing Point donde se presentó la falla: ')
        fallas = controller.getFallas(analyzer, name)
        print(f'Hay un total de {YELLOW}{fallas[0]}{END} paises afectados por la falla presentada en {YELLOW}{name}{END}.')
        print('Los paises afectados son:')
        for pais in lt.iterator(fallas[1]):
            hola = pais[1]['weight']
            print(f'{YELLOW}{pais[0]}{END}. Longitud del cable: {YELLOW}{hola}km{END}.')
    elif int(inputs[0]) == 7:
        pass
    elif int(inputs[0]) == 8:
        pass
    elif int(inputs[0]) == 9:
        pass
    else:
        sys.exit(0)
sys.exit(0)
