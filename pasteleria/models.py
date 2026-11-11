import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Linea(models.Model):
    nombre = models.CharField(
        max_length=100,
        unique=True
    )

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Línea"
        verbose_name_plural = "Líneas"

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    linea = models.ForeignKey(
        Linea,
        on_delete=models.CASCADE,
        related_name="productos"
    )
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    fotografia = models.ImageField(upload_to="productos/")
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=0
    )
    porciones = models.PositiveIntegerField(default=1)
    apto_celiacos = models.BooleanField(default=False)
    stock = models.PositiveIntegerField(default=0)
    disponible = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre


class Encargo(models.Model):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name="encargos"
    )
    nombre_comprador = models.CharField(max_length=150)
    correo = models.EmailField()
    fecha_retiro = models.DateField()
    cantidad = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(3)
        ]
    )
    fecha_encargo = models.DateTimeField(auto_now_add=True)
    codigo = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    class Meta:
        ordering = ["-fecha_encargo"]
        verbose_name = "Encargo"
        verbose_name_plural = "Encargos"

    def __str__(self):
        return f"Encargo {self.codigo} - {self.nombre_comprador}"

    @property
    def total(self):
        return self.producto.precio * self.cantidad
