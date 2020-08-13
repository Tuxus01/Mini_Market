from django.contrib import admin
from django.urls import path,include
from django.conf.urls import handler400, handler403, handler404, handler500
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from .ViewsOnline import *


app_name='base'

urlpatterns = [
    path('', Index, name='index'),
    #Loign
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/',signup, name='signup'),
    path('base/<str:Model>/list/', List , name="list"),
    path('base/<str:Model>/create/', Create , name="create"),
    path('base/<str:Model>/<int:id>/delete/', Delete , name="delete"),
    path('base/<str:Model>/<int:id>/update/', Update , name="update"),
    #API JSON
    #path('api/<str:Model>/<str:id>/', ApiList, name="Api-list"),
    #path('api/create/<str:Model>/', ApiCreate, name="ApiCreate-list"),
    #path('api/update/<str:Model>/<int:id>/', ApiUpdate, name="ApiUpdate-list"),
    path('base/cobros/',ListCuentasPorCobrar, name="cobros-list"),
    path('base/cobros/<int:id>/', abonoCuenta , name="abonos"),
    path('base/reporte/', Reporte, name='reporte'),

    #Online
    path('store/', store_view, name='store'),
    path('store/<int:id>/', store_view_id, name='store_id'),
    path('store/<int:Model>/list/', store_categoria , name="store_categoria"),
    path('store/shop/', Shop, name="shop"),
    path('store/carrito/', carrito_list, name="carrito_list"),
    path('store/carrito/check', carrito_check, name="carrito_check"),
    path('store/complete', paymentComplete, name="complete"),
    path('store/<str:Model>/list/', SubCategor , name="personalizado"),
    

]

