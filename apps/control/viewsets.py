from rest_framework import viewsets, permissions, filters
from django.db.models import Prefetch
from rest_framework import permissions
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from django.contrib.auth.decorators import permission_required
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser,MultiPartParser, FormParser,JSONParser
from .email import *
import threading


class ComponenteViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Componente.objects.all().order_by('-id')
    serializer_class = ComponenteSerializer
    search_fields = ['=serie','nombre']
    filter_backends = (filters.SearchFilter,)


class ComponenteALLViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Componente.objects.all().order_by('-id')
    serializer_class = ComponenteAllSerializer
    search_fields = ['=serie','nombre','descripcion','color__nombre','categoria__nombre','subcategoria__nombre','presentacion__nombre','talla__nombre']
    filter_backends = (filters.SearchFilter,)


class DetalleCompraViewSet(viewsets.ModelViewSet):
    #authentication_classes = [SessionAuthentication, BasicAuthentication]
    #permission_classes = [IsAuthenticated]
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = DetalleCompra.objects.all()
    serializer_class = DetalleCompraSerializer
    search_fields = ['=compra__id', '=componente__serie']
    filter_backends = (filters.SearchFilter,)
    #filter_fields = ('compra',)


class DetalleCompraViewSet1(viewsets.ModelViewSet):
    #authentication_classes = [SessionAuthentication, BasicAuthentication]
    #permission_classes = [IsAuthenticated]
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = DetalleCompra.objects.all()
    serializer_class = DetalleCompraSerializer1
    search_fields = ['=compra__id', 'componente__ip']
    filter_backends = (filters.SearchFilter,)
    #filter_fields = ('compra',)


class DetalleVentasViewSet(viewsets.ModelViewSet):
    #authentication_classes = [SessionAuthentication, BasicAuthentication]
    #permission_classes = [IsAuthenticated]
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = DetalleVentas.objects.all()
    serializer_class = DetalleVentasSerializer
    search_fields = ['=ventas__id', '=componente__serie']
    #search_fields = ['ventas__id', 'componente__serie']
    filter_backends = (filters.SearchFilter,)
    #filter_fields = ('compra',)


class DetalleVentasViewSet1(viewsets.ModelViewSet):
    #authentication_classes = [SessionAuthentication, BasicAuthentication]
    #permission_classes = [IsAuthenticated]
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = DetalleVentas.objects.all()
    serializer_class = DetalleVentasSerializer1
    search_fields = ['=ventas__id', 'componente__id']
    filter_backends = (filters.SearchFilter,)
    #filter_fields = ('compra',)


class ClienteViewSet(viewsets.ModelViewSet):
    #authentication_classes = [SessionAuthentication, BasicAuthentication]
    #permission_classes = [IsAuthenticated]
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    search_fields = ['identidad', 'nombre', 'apellidos' , 'telefono','email']
    filter_backends = (filters.SearchFilter,)
    #filter_fields = ('compra',)


class VentasViewSet(viewsets.ModelViewSet):
    #authentication_classes = [SessionAuthentication, BasicAuthentication]
    #permission_classes = [IsAuthenticated]
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Ventas.objects.all()
    serializer_class = VentaSerializer
    #search_fields = ['identidad', 'nombre', 'apellidos' , 'telefono','email']
    #filter_backends = (filters.SearchFilter,)
    #filter_fields = ('compra',)
    
    def update(self, request,  *args, **kwargs):
        #print(kwargs.get('pk'))
        instance = self.queryset.get(pk=kwargs.get('pk'))
        
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        #Proceso de rebajas de materiales o Componentes por ventas
        detalle = DetalleVentas.objects.filter(ventas=kwargs.get('pk'))
        for i in detalle:
            componente = Componente.objects.get(pk=i.componente.id)
            stock = componente.stock_actual
            ventas_stock = i.cantidad
            resta_total = float(stock) - float(ventas_stock)
            #print(stock)
            #print(ventas_stock)
            #print(resta_total)
            componente.stock_actual = resta_total

            if componente.minimo_notificacion:
                if resta_total < componente.minimo_notificacion:
                    SendEmailT2=SendEmailInfoThread(componente.nombre, resta_total)
                    SendEmailT2.start()

            componente.save()
            

        #Envio de email si la compra es al credito
        if instance.pago == 2:
            #Envio de email con Fotografia de la persona que ingreso de forma no autorizada
            SendEmailT= SendEmailThread(instance.id)
            SendEmailT.start()
        
        
        return Response(serializer.data)



class CarritoViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Carrito.objects.all().order_by('-id')
    serializer_class = CarritoSerializer
    search_fields = ['=owner__id','=activo']
    filter_backends = (filters.SearchFilter,)