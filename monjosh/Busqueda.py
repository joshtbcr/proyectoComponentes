from datetime import datetime


class Busqueda:
    def __init__(self, producto):
        self.producto = producto
        self.fecha = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        self.puntos = 110
