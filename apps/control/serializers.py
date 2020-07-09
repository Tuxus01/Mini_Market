from rest_framework import serializers
from .models import *

class ComponenteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Componente
		fields ='__all__'


class DetalleCompraSerializer(serializers.ModelSerializer):
    componente = ComponenteSerializer()
    class Meta:
        model = DetalleCompra
        fields ='__all__'



class DetalleCompraSerializer1(serializers.ModelSerializer):
    class Meta:
        model = DetalleCompra
        fields ='__all__'

class DetalleCompraSerializer1(serializers.ModelSerializer):
    
    class Meta:
        model = DetalleCompra
        fields ='__all__'


class DetalleVentasSerializer(serializers.ModelSerializer):
    componente = ComponenteSerializer()
    class Meta:
        model = DetalleVentas
        fields ='__all__'



class DetalleVentasSerializer1(serializers.ModelSerializer):
    class Meta:
        model = DetalleVentas
        fields ='__all__'


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields ='__all__'


class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ventas
        fields ='__all__'
