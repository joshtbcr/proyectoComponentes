class Ingrediente:
    def __init__(self, nombre_ingrediente, cantidad_ingrediente, precio_ingrediente):
        self.nombre_ingrediente = nombre_ingrediente
        self.cantidad_ingrediente = cantidad_ingrediente
        self.precio_ingrediente = precio_ingrediente

    def ingredienteADiccionario(self, ingrediente):
        return {
            'nombreIngrediente': ingrediente.nombre_ingrediente,
            'cantidadIngrediente': ingrediente.cantidad_ingrediente,
            'precioIngrediente': ingrediente.precio_ingrediente
        }

    def __str__(self):
        return 'nombre: ', self.nombre_ingrediente
