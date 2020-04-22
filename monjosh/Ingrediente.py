class Ingrediente:
    def __init__(self, nombre_ingrediente, cantidad_ingrediente, unidad_ingrediente):
        self.nombre_ingrediente = nombre_ingrediente
        self.cantidad_ingrediente = cantidad_ingrediente
        self.unidad_ingrediente = unidad_ingrediente

    def ingredienteADiccionario(self, ingrediente):
        return {
            'Name': ingrediente.nombre_ingrediente,
            'Amount': ingrediente.cantidad_ingrediente,
            'Unit': ingrediente.unidad_ingrediente
        }

    def __str__(self):
        return 'Name: ', self.nombre_ingrediente
