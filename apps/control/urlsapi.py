from rest_framework import routers

from .viewsets import *

router = routers.SimpleRouter()
router.register('componente', ComponenteViewSet )
router.register('componenteAll', ComponenteALLViewSet )
router.register('detallecompras', DetalleCompraViewSet )
router.register('detallecompras1', DetalleCompraViewSet1 )
router.register('detalleventas', DetalleVentasViewSet )
router.register('detalleventas1', DetalleVentasViewSet1 )
router.register('cliente', ClienteViewSet )
router.register('ventas', VentasViewSet )


router.register('carrito', CarritoViewSet )

urlpatterns = router.urls