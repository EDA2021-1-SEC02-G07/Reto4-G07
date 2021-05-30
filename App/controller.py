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
    return analyzer
# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
