from django.shortcuts import get_object_or_404, render

from .models import Linea, Producto


def catalogo(request):
    productos = Producto.objects.filter(disponible=True).select_related("linea")
    lineas = Linea.objects.all()

    busqueda = request.GET.get("q", "").strip()
    linea_id = request.GET.get("linea", "").strip()

    if busqueda:
        productos = productos.filter(nombre__icontains=busqueda)

    if linea_id:
        productos = productos.filter(linea_id=linea_id)

    contexto = {
        "productos": productos,
        "lineas": lineas,
        "busqueda": busqueda,
        "linea_seleccionada": linea_id,
    }
    return render(request, "pasteleria/catalogo.html", contexto)


def detalle_producto(request, producto_id):
    producto = get_object_or_404(
        Producto.objects.select_related("linea"),
        id=producto_id,
        disponible=True,
    )
    return render(
        request,
        "pasteleria/detalle_producto.html",
        {"producto": producto},
    )
