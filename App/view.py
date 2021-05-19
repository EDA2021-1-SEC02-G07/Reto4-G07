import config as cf
import sys
import controller
from DISClib.ADT.graph import gr
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
internetFile = 'landing_points.csv'
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        analyzer = controller.init()
        analyzer = controller.loadData(analyzer, internetFile)
        print("Cargando información de los archivos ....")
        vertexN = gr.numVertices(analyzer['cables'])
        edgesN = gr.numEdges(analyzer['cables'])
        vertex = lt.firstElement(gr.vertices(analyzer['cables']))
        edges = gr.adjacentEdges(analyzer['cables'], vertex)
        edgesL = []
        for x in range(lt.size(edges)):
            edgesL.append(lt.getElement(edges, x))
        adjV = gr.adjacentEdges(analyzer['cables'], vertex)
        print(f'\nNúmero de vértices: {vertexN}.')
        print(f'Número de arcos: {edgesN}.')
        print(f'En primer vértice es {vertex}, sus arcos son {edgesL} y sus adyacentes son {adjV}')

    elif int(inputs[0]) == 2:
        pass

    else:
        sys.exit(0)
sys.exit(0)
