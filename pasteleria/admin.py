from django.contrib import admin

from .models import Encargo, Linea, Producto


admin.site.register(Linea)
admin.site.register(Producto)
admin.site.register(Encargo)
