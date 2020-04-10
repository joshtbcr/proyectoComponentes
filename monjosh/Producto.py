class Producto:
    def __init__(self, nombre_producto, cantidad_producto, precio_producto, ingredientes=[]):
        self.nombre_producto = nombre_producto
        self.cantidad_producto = cantidad_producto
        self.precio_producto = precio_producto
        self.ingredientes = ingredientes

    def productoADiccionario(self, producto):
        return {
            'nombreProducto': producto.nombre_producto,
            'cantidadProducto': producto.cantidad_producto,
            'precioProducto': producto.precio_producto,
            'ingredientes': producto.ingredientes
        }

    def __str__(self):
        return 'nombre: ', self.nombre_producto
