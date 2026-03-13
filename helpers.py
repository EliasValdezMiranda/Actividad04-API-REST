import json
import os


LLAVES_PRODUCTO = {"id", "nombre", "precio", "stock", "idCategoría"}
"""
Almacena las llaves que conformarán un producto en el archivo JSON.
"""

LLAVES_CATEGORIA = {"id", "nombre"}
"""
Almacena las llaves que conformarán un producto en el archivo JSON.
"""

def cargarDatosJSON(nombreArchivo):
    """
    Carga los datos de un archivo en formato JSON en una estructura
    de datos de Python

    :param nombreArchivo: Nombre del archivo del que se cargarán los datos.
    :return: Una estructura de datos de Python con la información del archivo JSON. `None` si el archivo no existe.
    """

    if not os.path.exists(nombreArchivo):
        return None
    with open(nombreArchivo, 'r', encoding="utf-8") as file:
        return json.load(file)

def guardarDatosJSON(datos, nombreArchivo):
    """
    Guarda los datos de una estructura de datos de Python en un archivo JSON.

    :param datos: Estructura de datos con la información por guardar.
    :param nombreArchivo: Nombre del archivo en el que se guardarán los datos. Por defecto `datosSensor.json`.
    """

    with open(nombreArchivo, 'w', encoding="utf-8") as file:
        json.dump(datos, file, indent=4, ensure_ascii=False)

def verificarProducto(diccionario, incluirID):
    """
    Verifica que un diccionario otorgado cuente con las claves esperadas
    de un producto de acuerdo a la especificación en este programa.

    :param diccionario: Diccionario por analizar.
    :return: `True` si el diccionario cumple con la estructura esperada por el programa, `False` de lo contrario.
    """
    referencia = set(LLAVES_PRODUCTO)
    # Se elimina la ID para la verificación de solicitudes POST y PUT del usuario
    if not incluirID:
        referencia.remove("id")
    if set(diccionario) == referencia:
        return True
    else:
        return False

def verificarCategoria(diccionario, incluirID):
    """
    Verifica que un diccionario otorgado cuente con las claves esperadas
    de una categoria de acuerdo a la especificación en este programa.

    :param diccionario: Diccionario por analizar.
    :param incluirID: Valor booleano que indica si se eliminará la clave `id` del set de referencia.
    :return: `True` si el diccionario cumple con la estructura esperada por el programa, `False` de lo contrario.
    """
    referencia = set(LLAVES_CATEGORIA)
    # Se elimina la ID para la verificación de solicitudes POST y PUT del usuario
    if not incluirID:
        referencia.remove("id")
    if set(diccionario) == referencia:
        return True
    else:
        return False