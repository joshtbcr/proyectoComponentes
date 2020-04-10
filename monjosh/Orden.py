
class Orden:
    def __init__(self, numero_orden, fecha, estado, precio, productos=[]):
        self.numero_orden = numero_orden
        self.fecha = fecha
        self.estado = estado
        self.precio = precio
        self.productos = productos

    def __str__(self):
        return self.numero_orden
