
from django.contrib import admin
from .models import Linea, Producto, Encargo


@admin.register(Linea)
class LineaAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)
    ordering = ("nombre",)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "linea",
        "precio_clp",
        "porciones",
        "apto_celiacos",
        "stock",
        "disponible",
    )

    list_filter = (
        "linea",
        "apto_celiacos",
    )

    search_fields = ("nombre",)
    ordering = ("nombre",)

    @admin.display(description="Precio")
    def precio_clp(self, obj):
        return f"${obj.precio:,.0f}".replace(",", ".")


@admin.register(Encargo)
class EncargoAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "producto",
        "nombre_comprador",
        "cantidad",
        "fecha_retiro",
    )

    list_filter = (
        "producto",
        "fecha_retiro",
    )

    search_fields = (
        "nombre_comprador",
        "correo",
    )

    readonly_fields = (
        "codigo",
        "fecha_encargo",
    )
