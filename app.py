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

# Ruta /productos [POST]
@app.route('/productos', methods=['POST'])
def subirProducto():
    productos = cargarDatosJSON(ARCHIVO_PRODUCTOS_JSON)
    # Si la función cargarDatosJSON devuelve None,
    # el archivo está vacío y se empieza desde una lista vacía.
    if productos is None:
        productos = []
    
    # El programa pide al usuario los datos los cuales pueden ser ingresados desde POSTMAN.
    datos = request.get_json()
    # En caso de que el producto no cumple con las cabeceras, se le informa al usuario.
    if not verificarProducto(datos, False):
        return jsonify({'Error': 'Producto no compatible. Verifique que ingresó los datos correctamente'}), 400
    
    # El programa verifica que el precio sea un número y sea mayor a 0.
    # En caso de que el producto no cumpla con las condiciones, se le informa al usuario.
    if not isinstance(datos["precio"], (int, float)) or datos["precio"] < 0:
        return jsonify({'Error': 'Precio inválido. Verifique haber introducido un valor numérico mayor o igual a 0'}), 400

    # El programa verifica que el precio sea un número entero y sea mayor a 0.
    # En caso de que el producto no cumpla con las condiciones, se le informa al usuario.
    if not isinstance(datos["stock"], int) or datos["stock"] < 0:
        return jsonify({'Error': 'Stock inválido. Verifique haber introducido un valor numérico entero mayor o igual a 0'}), 400

    categorias = cargarDatosJSON(ARCHIVO_CATEGORIAS_JSON)
    # Si la función cargarDatosJSON devuelve None,
    # el archivo no existe y se le informa al usuario.
    if categorias is None:
        return jsonify({'Error': 'No existen categorías registradas. Cree una categoría primero.'}), 404
    # Verificación de la ID en forma de iteración. Itera sobre el archivo que contiene las categorias
    # hasta que encuentra la ID.
    categoria_existe = False
    for categoria in categorias:
        if verificarCategoria(categoria, True) and categoria['id'] == datos['idCategoría']:
            categoria_existe = True
            break
    # En caso de que la iteración no encuentre la categoría, se le informa al usuario.
    if not categoria_existe:
        return jsonify({'Error': 'La categoría no existe'}), 404
    
    # Asignación de ID automáticamente.
    nuevaID = 1 if not productos else productos[-1]['id'] + 1
    
    # Asignar datos a un nuevo producto en formato JSON
    nuevoProducto = {
        "id": nuevaID,
        "nombre": datos['nombre'],
        "precio": datos['precio'],
        "stock": datos['stock'],
        "idCategoría": datos['idCategoría']
    }
    # Guardar los datos en el archivo JSON
    productos.append(nuevoProducto)
    guardarDatosJSON(productos, ARCHIVO_PRODUCTOS_JSON)
    return jsonify(nuevoProducto), 201

# Ruta /productos/<id> [PUT]
@app.route('/productos/<int:id>', methods=['PUT'])
def editarProducto(id):
    productos = cargarDatosJSON(ARCHIVO_PRODUCTOS_JSON)
    # Si la función cargarDatosJSON devuelve None,
    # el archivo está vacío y se le lanza una advertencia al usuario.
    if productos is None:
        return jsonify({'Error':'No hay productos para editar. Ingresar productos con "POST"'}), 404
    
    # Busca en todo el archivo que contiene los productos (legible para Python)
    for producto in productos:
        # Verifica que la ID del producto coincida con la ID de un producto en el archivo
        if verificarProducto(producto, True) and producto["id"]  == id:
            datos = request.get_json()
            # Verifica que las cabeceras del producto a añadir coincidan con las demas cabeceras
            if not verificarProducto(datos, False):
                return jsonify({'Error':'Datos no compatibles. Verifique que ingresó los datos correctamente'}), 400

            # El programa verifica que el precio sea un número y sea mayor a 0.
            # En caso de que el producto no cumpla con las condiciones, se le informa al usuario.
            if not isinstance(datos["precio"], (int, float)) or datos["precio"] < 0:
                return jsonify({'Error': 'Precio inválido. Verifique haber introducido un valor numérico mayor o igual a 0'}), 400

            # El programa verifica que el precio sea un número entero y sea mayor a 0.
            # En caso de que el producto no cumpla con las condiciones, se le informa al usuario.
            if not isinstance(datos["stock"], int) or datos["stock"] < 0:
                return jsonify({'Error': 'Stock inválido. Verifique haber introducido un valor numérico entero mayor o igual a 0'}), 400
            
            categorias = cargarDatosJSON(ARCHIVO_CATEGORIAS_JSON)
                # Si la función cargarDatosJSON devuelve None,
                # el archivo está vacío y se le lanza una advertencia al usuario.
            if categorias is None:
                return jsonify({'Error':'No existen categorías registradas. Cree una categoría primero.'}), 404
            # Verificación de la ID en forma de iteración. Itera sobre el archivo que contiene las categorias
            # hasta que encuentra la ID.
            categoria_existe = False
            for categoria in categorias:
                if verificarCategoria(categoria, True) and categoria['id'] == datos['idCategoría']:
                    categoria_existe = True
                    break
            # En caso de que la iteración no encuentre la categoría, se le informa al usuario.
            if not categoria_existe:
                return jsonify({'Error':'La categoría no existe'}), 404
            
            # Remplaza los valores por los nuevos que ingrese el usuario mediante el 'request'
            producto["nombre"] = datos["nombre"]
            producto["precio"] = datos["precio"]
            producto["stock"] = datos["stock"]
            producto["idCategoría"] = datos["idCategoría"]
            
            # Guarda los datos en el archivo JSON
            guardarDatosJSON(productos, ARCHIVO_PRODUCTOS_JSON)
            return jsonify(producto), 200
    # En caso de que el producto no haya sido encontrado, lanza un mensaje de error.
    return jsonify({'Error':'No se encontró el producto buscado.'}), 404

# Ruta /productos/<id> [DELETE]
@app.route('/productos/<int:id>', methods=['DELETE'])
def eliminarProducto(id):
    productos = cargarDatosJSON(ARCHIVO_PRODUCTOS_JSON)

    # Si la función cargarDatosJSON devuelve None,
    # el archivo está vacío y se le lanza una advertencia al usuario.
    if productos is None:
        return jsonify({'Error': 'No hay productos para eliminar. Ingresar productos con "POST".'}), 404

    # Itera sobre el archivo productos.json (formato legible para Python) hasta que
    # encuentra el producto que coincida con la ID pasada del parámetro
    for producto in productos:
        if verificarProducto(producto, True) and producto["id"] == id:
            # Copia la lista de productos y elimina el producto de esa copia de la lista
            copiaProductos = productos.copy()
            copiaProductos.remove(producto)

            # Guarda los datos y devuelve un mensaje de éxito
            guardarDatosJSON(copiaProductos, ARCHIVO_PRODUCTOS_JSON)
            return jsonify({'Éxito': 'Producto eliminado.'}), 200

    # En caso de no encontrar el producto que coincida con la ID, se le indica al usuario
    return jsonify({'Error': 'No se encontró el producto buscado.'}), 404

def main():
    app.run(debug = True)

if __name__ == "__main__":
    main()