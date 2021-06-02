import config as cf
import sys
import controller
from DISClib.ADT.graph import gr
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
assert cf


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
        print("Cargando información de los archivos ....")
        analyzer = controller.loadData(analyzer, pointFile, connectFile, countryFile)
        LPs = gr.numVertices(analyzer['cables'])
        ARCs = gr.numEdges(analyzer['cables'])
        vertex = lt.firstElement(gr.vertices(analyzer['cables']))
        infoV = me.getValue(mp.get(analyzer['landingPoints'], vertex))
        last = lt.lastElement(mp.keySet(analyzer['paises']))
        infoL = mp.get(analyzer['paises'], last)
        infoL = infoL['value']
        print(infoL)
        print(f'El número total de Landing Points es {LPs}.')
        print(f'El número total de conexiones es {ARCs}.')
        print(f'En primer Landing Point tiene el identificador {vertex}.\nNombre: {infoV[2]}.\nID: {infoV[1]}.\nLatitud: {infoV[0][1]}.\nLongitud: {infoV[0][0]}.')
        print(f'El último país cargado es: {last}. \nPoblación: {infoL[2]}. \nUsuarios de internet: {infoL[1]}')
    
    elif int(inputs[0]) == 2:
        point1 = input("Ingrese el primer LandingPoint: ")
        point2 = input("Ingrese el segundo landingPoint: ")
        ans = controller.callClusterL(analyzer, point1, point2)

    else:
        sys.exit(0)
sys.exit(0)
