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

def loadData(analyzer, internetFile):
    internetFile = cf.data_dir + internetFile
    input_file = csv.DictReader(open(internetFile, encoding="utf-8"),
                                delimiter=",")
    lastPoint = None
    for point in input_file:
        if lastPoint is not None:
            '''samePoint = lastPoint['landing_point_id'] == point['landing_point_id']
            sameLati = lastPoint['latitude'] == point['latitude']
            sameLongi = lastPoint['longitude'] == point['longitude']
            if not samePoint and not sameLati and not sameLongi:'''
            model.addPointConnection(analyzer, lastPoint, point)
        lastPoint = point
    
    return analyzer
# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
