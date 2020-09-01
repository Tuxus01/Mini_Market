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




##Classe para VUE ONLINE

##Componentes, ALL
class SubCategoriaSerializer(serializers.ModelSerializer):
	class Meta:
		model = SubCategoria
		fields ='__all__'

class ColorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Color
		fields ='__all__'

class TallaSerializer(serializers.ModelSerializer):
	class Meta:
		model = Talla
		fields ='__all__'

class PresentacionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Presentacion
		fields ='__all__'

class CategoriaSerializer(serializers.ModelSerializer):
	class Meta:
		model = Categoria
		fields ='__all__'

class ComponenteAllSerializer(serializers.ModelSerializer):
    presentacion = PresentacionSerializer()
    categoria = CategoriaSerializer()
    subcategoria = SubCategoriaSerializer()
    color = ColorSerializer()
    talla = TallaSerializer()
    
    class Meta:
        model = Componente
        fields ='__all__'
##Componentes, ALL

##Carrito 
class CarritoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Carrito
		fields ='__all__'

class Detalle_CarritoSerializer(serializers.ModelSerializer):
    componente = ComponenteSerializer()
    class Meta:
        model = Detalle_Carrito
        fields ='__all__'


##Classe para VUE ONLINE