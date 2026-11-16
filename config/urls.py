
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from pasteleria import views


urlpatterns = [
    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "",
        views.catalogo,
        name="catalogo"
    ),

    path(
        "producto/<int:producto_id>/",
        views.detalle_producto,
        name="detalle_producto"
    ),

    path(
        "producto/<int:producto_id>/encargar/",
        views.crear_encargo,
        name="crear_encargo"
    ),

    path(
        "comprobante/<uuid:codigo>/",
        views.comprobante,
        name="comprobante"
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
