from django.db import models

class Ingrediente(models.Model):
    numeroOrden = models.CharField(max_length=200)
    fecha = models.DateTimeField('Fecha de registro')
    cantidad = models.PositiveIntegerField()
