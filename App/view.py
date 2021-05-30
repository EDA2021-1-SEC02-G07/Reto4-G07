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
        analyzer = controller.loadData(analyzer, pointFile, connectFile, countryFile)
        print("Cargando información de los archivos ....")
        LPs = gr.numVertices(analyzer['cables'])
        ARCs = gr.numEdges(analyzer['cables'])
        vertex = lt.firstElement(gr.vertices(analyzer['cables']))
        infoV = me.getValue(mp.get(analyzer['landingPoints'], vertex))
        print(f'\nEl número total de Landing Points es {LPs}.')
        print(f'El número total de conexiones es {ARCs}.')
        print(f'En primer Landing Point tiene el identificador {vertex}.\nNombre: {infoV[2]}.\nID: {infoV[1]}.\nLatitud: {infoV[0][1]}.\nLongitud: {infoV[0][0]}.')

    elif int(inputs[0]) == 2:
        pass

    else:
        sys.exit(0)
sys.exit(0)
