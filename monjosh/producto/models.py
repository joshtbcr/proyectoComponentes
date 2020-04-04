from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

   def __str__(self):
        return str(self.nombre) + ": ₡" + str(self.precio)