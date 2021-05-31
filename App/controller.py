import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de cables
def init():
    analyzer = model.newAnalyzer()
    return analyzer

def loadData(analyzer, pointFile, connectFile, countryFile):
    pointFile = cf.data_dir + pointFile
    connectFile = cf.data_dir + connectFile
    countryFile = cf.data_dir + countryFile

    input_file1 = csv.DictReader(open(pointFile, encoding="utf-8"),
                                delimiter=",")
    for point in input_file1:
        model.addLandingPoint(analyzer, point)
    
    input_file2 = csv.DictReader(open(connectFile, encoding="utf-8"),
                                delimiter=",")
    for cable in input_file2:
        model.addCable(analyzer, cable)

    input_file3 = csv.DictReader(open(countryFile, encoding="utf-8"),
                                delimiter=",")
    contador = 0                            
    for pais in input_file3:
        model.addPais(analyzer, pais)
        contador+=1
    print(f'Se cargaron {contador} países')
    
    return analyzer
# Funciones para la carga de datos
def callClusterL(analyzer, point1, point2):
    ans = model.clusterL(analyzer, point1, point2)
    

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
