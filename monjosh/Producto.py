class Producto:
    def __init__(self, nombre_producto, porciones_producto, precio_producto, imagen_producto, ingredientes=[]):
        self.nombre_producto = nombre_producto
        self.porciones_producto = porciones_producto
        self.precio_producto = precio_producto
        self.imagen_producto = imagen_producto
        self.ingredientes = ingredientes

    def productoADiccionario(self, producto):
        return {
            'Name': producto.nombre_producto,
            'Servings': producto.porciones_producto,
            'PricePerServing': producto.precio_producto,
            'Image': producto.imagen_producto,
            'Ingredients': producto.ingredientes
        }

    def __str__(self):
        return 'Name: ', self.nombre_producto
