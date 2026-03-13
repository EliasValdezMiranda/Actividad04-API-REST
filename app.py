from flask import Flask, jsonify, request, Response
from helpers import cargarDatosJSON, guardarDatosJSON, verificarProducto, verificarCategoria

# Creación del objeto app y configuración del ordenamiento de claves en JSON
app = Flask(__name__)
app.json.sort_keys = False

# Nombre de los archivos que se almacenarán localmente
ARCHIVO_PRODUCTOS_JSON = 'productos.json'
ARCHIVO_CATEGORIAS_JSON = 'categorias.json'

# Ruta /productos
@app.route("/productos", methods=['GET'])
def obtenerInventario():
    inventario = cargarDatosJSON(ARCHIVO_PRODUCTOS_JSON)
    # Si la función cargarDatosJSON devuelve None,
    # el archivo no existe y se le informa al usuario.
    if inventario is None:
        return jsonify({"Error": "No existen registros de productos (Crear con métodos POST)"}), 404
    return jsonify(inventario), 200

# Ruta /productos/id
@app.route("/productos/<int:id>", methods=['GET'])
def obtenerProducto(id):
    inventario = cargarDatosJSON(ARCHIVO_PRODUCTOS_JSON)
    # Si la función cargarDatosJSON devuelve None,
    # el archivo no existe y se le informa al usuario.
    if inventario is None:
        return jsonify({"Error": "No existen registros de productos (Crear con métodos POST)"}), 404
    for producto in inventario:
        # Si el producto cuenta con la estructura esperada y la id coincide
        # con la id solicitada, se devuelve la solicitud.
        if verificarProducto(producto, True) and producto["id"]  == id:
            return jsonify(producto), 200
    else:
        return jsonify({"Error": "No se encontró el producto buscado."}), 404

# Ruta /categorias
@app.route("/categorias", methods=['GET', 'POST'])
def categorias():
    categorias = cargarDatosJSON(ARCHIVO_CATEGORIAS_JSON)
    # Método GET
    if request.method == 'GET':
        # Si la función cargarDatosJSON devuelve None,
        # el archivo no existe y se le informa al usuario.
        if categorias is None:
            return jsonify({"Error": "No existen registros de categorias (Crear con métodos POST)"}), 404
        return jsonify(categorias), 200
    # Método POST
    elif request.method == 'POST':
        # Si la función cargarDatosJSON devuelve None,
        # se trabajará con una lista vacía.
        if categorias is None:
            categorias = []
        solicitud = request.get_json()
        # Si el formato JSON adjunto con la solicitud no cumple con
        # las claves esperadas, se informa al usuario.
        if not verificarCategoria(solicitud, False):
            return jsonify({'Error':'Datos de categoría incompatibles'}), 400
        # Si se trabaja con una lista vacía, se usa la id 1. Si no, se suma 1 a la
        # última id de categoría en el archivo local.
        nuevaID = 1 if not categorias else categorias[-1]['id'] + 1
        # Se crea una nueva categoría con la información de la solicitud.
        nuevaCategoria = {
        'id' : nuevaID,
        'nombre': solicitud['nombre']
        }
        # Se guarda la nueva categoría en el archivo local y se regresa al usuario.
        categorias.append(nuevaCategoria)
        guardarDatosJSON(categorias, ARCHIVO_CATEGORIAS_JSON)
        return jsonify(nuevaCategoria), 201

# Ruta /categorias/id
@app.route("/categorias/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def categoriasID(id):
    categorias = cargarDatosJSON(ARCHIVO_CATEGORIAS_JSON)
    # Si la función cargarDatosJSON devuelve None,
    # el archivo no existe y se le informa al usuario.
    if categorias is None:
        return jsonify({"Error": "No existen registros de categorias (Crear con métodos POST)"}), 404
    for categoria in categorias:
        # Se verifica que las categorías almacenadas sean válidas y coincidan con la id solicitada.
        if verificarCategoria(categoria, True) and categoria["id"] == id:
            # Método GET
            if request.method == 'GET':
                return jsonify(categoria), 200
            # Método PUT
            elif request.method == 'PUT':
                solicitud = request.get_json()
                # Si el formato JSON adjunto con la solicitud no cumple con
                # las claves esperadas, se informa al usuario.
                if not verificarCategoria(solicitud, False):
                    return jsonify({'Error':'Datos de categoría incompatibles'}), 400
                # Se actualizan las variables de la categoría y se guardan en el archivo local.
                categoria["nombre"] = solicitud["nombre"]
                guardarDatosJSON(categorias, ARCHIVO_CATEGORIAS_JSON)
                return jsonify(categoria), 200
            # Método DELETE
            elif request.method == 'DELETE':
                # Se crea una copia de la lista de categorias
                # y se elimina la categoría, sobrescribiendo el archivo.
                copiaCategorias = categorias.copy()
                copiaCategorias.remove(categoria)
                guardarDatosJSON(copiaCategorias, ARCHIVO_CATEGORIAS_JSON)
                return jsonify({'Éxito':'Categoría eliminada'}), 200
    else:
        return jsonify({"Error": "No se encontró la categoría buscada."}), 404

def main():
    app.run(debug = True)

if __name__ == "__main__":
    main()