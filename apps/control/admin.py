from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Presentacion)
admin.site.register(Categoria)
admin.site.register(Componente)
admin.site.register(Cliente)
admin.site.register(Proveedores)
admin.site.register(Compras)
admin.site.register(DetalleCompra)
admin.site.register(Ventas)
admin.site.register(DetalleVentas)
admin.site.register(CuentasPorPagar)
admin.site.register(SubCategoria)
admin.site.register(CommentarioOnline)
admin.site.register(Color)
admin.site.register(Talla)

#ONLINE
admin.site.register(Carrito)
admin.site.register(Detalle_Carrito)
admin.site.register(Detalle_envio)

