from datetime import datetime

class Orden:
    def __init__(self, numero_orden, estado, precio, productos=[]):
        self.numero_orden = numero_orden
        self.fecha = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        self.estado = estado
        self.precio = precio
        self.productos = productos

    def __str__(self):
        return self.numero_orden
