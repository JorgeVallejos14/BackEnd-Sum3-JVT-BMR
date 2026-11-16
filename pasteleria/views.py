
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EncargoForm
from .models import Linea, Producto, Encargo


def formato_clp(valor):
    return f"${valor:,.0f}".replace(",", ".")


def catalogo(request):
    productos = Producto.objects.filter(
        disponible=True
    ).select_related("linea")

    lineas = Linea.objects.all()

    busqueda = request.GET.get("q", "").strip()
    linea_id = request.GET.get("linea", "").strip()

    if busqueda:
        productos = productos.filter(
            nombre__icontains=busqueda
        )

    if linea_id:
        productos = productos.filter(
            linea_id=linea_id
        )

    contexto = {
        "productos": productos,
        "lineas": lineas,
        "busqueda": busqueda,
        "linea_seleccionada": linea_id,
    }

    return render(
        request,
        "pasteleria/catalogo.html",
        contexto,
    )


def detalle_producto(request, producto_id):
    producto = get_object_or_404(
        Producto.objects.select_related("linea"),
        id=producto_id,
        disponible=True,
    )

    return render(
        request,
        "pasteleria/detalle_producto.html",
        {
            "producto": producto,
            "form": EncargoForm(),
            "precio_clp": formato_clp(producto.precio),
        },
    )


def crear_encargo(request, producto_id):
    producto = get_object_or_404(
        Producto.objects.select_related("linea"),
        id=producto_id,
        disponible=True,
    )

    if request.method != "POST":
        return redirect(
            "detalle_producto",
            producto_id=producto.id
        )

    form = EncargoForm(request.POST)

    if form.is_valid():
        cantidad = form.cleaned_data["cantidad"]

        if producto.stock < cantidad:
            form.add_error(
                "cantidad",
                f"Solo quedan {producto.stock} unidades disponibles."
            )
        else:
            with transaction.atomic():
                actualizados = Producto.objects.filter(
                    pk=producto.pk,
                    disponible=True,
                    stock__gte=cantidad,
                ).update(
                    stock=F("stock") - cantidad
                )

                if actualizados == 1:
                    encargo = form.save(commit=False)
                    encargo.producto = producto
                    encargo.save()

                    return redirect(
                        "comprobante",
                        codigo=encargo.codigo,
                    )

            producto.refresh_from_db()

            form.add_error(
                "cantidad",
                f"Solo quedan {producto.stock} unidades disponibles."
            )

    return render(
        request,
        "pasteleria/detalle_producto.html",
        {
            "producto": producto,
            "form": form,
            "precio_clp": formato_clp(producto.precio),
        },
    )


def comprobante(request, codigo):
    encargo = get_object_or_404(
        Encargo.objects.select_related("producto"),
        codigo=codigo,
    )

    return render(
        request,
        "pasteleria/comprobante.html",
        {
            "encargo": encargo,
            "total_clp": formato_clp(encargo.total),
        },
    )
