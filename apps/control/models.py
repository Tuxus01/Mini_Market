from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from datetime import date
from datetime import datetime
from django.forms import model_to_dict



#Base Global para todas las tablas
class ModelBase(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.BooleanField('Status', default=True)
    date_create = models.DateField('Date of Create',auto_now = False, auto_now_add = True)
    date_change = models.DateField('Date of Change',auto_now = True, auto_now_add = False)
    date_delete = models.DateField('Date of Delete',auto_now = True, auto_now_add = False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    date_time_c = models.TimeField(auto_now = False, auto_now_add = True)
    date_time_m = models.TimeField(auto_now = True, auto_now_add = False)

    class Meta:
        abstract = True



class SubCategoria(ModelBase):
    nombre = models.CharField('Sub Categoria',max_length=80, unique=True)
    descripcion = models.TextField(max_length=600, blank=True, null=True)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def __str__(self):
        return self.nombre 


class Color(ModelBase):
    nombre = models.CharField('Color',max_length=80, unique=True)
    descripcion = models.TextField(max_length=600, blank=True, null=True)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def __str__(self):
        return self.nombre 



class Talla(ModelBase):
    nombre = models.CharField('Talla',max_length=80, unique=True)
    descripcion = models.TextField(max_length=600, blank=True, null=True)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def __str__(self):
        return self.nombre 


class Presentacion(ModelBase):
    nombre = models.CharField('Presentacion ',max_length=80, unique=True)
    descripcion = models.TextField(max_length=600, blank=True, null=True)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def __str__(self):
        return self.nombre


class Categoria(ModelBase):
    nombre = models.CharField('Categoria ',max_length=80, unique=True)
    descripcion = models.TextField(max_length=600, blank=True, null=True)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def __str__(self):
        return self.nombre



def Componente_file(self,filename):
    today = date.today()
    year = format(today.year)
    mes = format(today.month)
    dia = format(today.day)
    path = "static/MultimediaData/img/%s/%s/%s/%s/%s" %(str(year), str(mes), str(dia), str(self.nombre), str(filename))
    return path


class Componente(ModelBase):
    nombre = models.CharField('Nombre Producto ',max_length=100, unique=True)
    presentacion = models.ForeignKey(Presentacion, on_delete=models.CASCADE, blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, blank=True, null=True)
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.CASCADE, blank=True, null=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    talla = models.ForeignKey(Talla, on_delete=models.CASCADE, blank=True, null=True)
    serie = models.CharField(max_length=300, unique=True)
    pre_compra = models.DecimalField(verbose_name='Precio Compra', max_digits=20,decimal_places=2)
    pre_venta = models.DecimalField(verbose_name='Precion Venta', max_digits=20, decimal_places=2)
    isv = models.IntegerField(choices=((1,("0%")),(2,("15%")),(3,("18%"))),default=2)
    stock_inicial = models.DecimalField(verbose_name='Stock Inicial', max_digits=20, decimal_places=2, default=0.0)
    stock_actual = models.DecimalField(verbose_name='Stock Actual', max_digits=20, decimal_places=2, default=0.0)
    descripcion = models.TextField(max_length=600, blank=True, null=True)
    imagen = models.ImageField(upload_to=Componente_file, blank=True, null=True)
    imagen2 = models.ImageField(upload_to=Componente_file, blank=True, null=True)
    imagen3 = models.ImageField(upload_to=Componente_file, blank=True, null=True)
    imagen4 = models.ImageField(upload_to=Componente_file, blank=True, null=True)
    imagen5 = models.ImageField(upload_to=Componente_file, blank=True, null=True)
    imagen6 = models.ImageField(upload_to=Componente_file, blank=True, null=True)
    multiplicador = models.DecimalField(verbose_name='Cuantas Unidades ?', max_digits=20, decimal_places=2, default=1)
    minimo_notificacion = models.FloatField(verbose_name="Notificar al Minimo", blank=True, null=True)
    online = models.BooleanField('Activo para Ventas Online ?',default=False)
    


    def toJSON(self):
        item = model_to_dict(self, fields=['id','nombre','presentacion','categoria','serie','pre_compra','pre_venta','isv','stock_inicial','stock_actual','descripcion'])
        if self.presentacion != None:
            nombre = Presentacion.objects.get(pk=self.presentacion.id)
            item['presentacion'] = str(nombre)
        
        if self.categoria != None:
            nombre = Categoria.objects.get(pk=self.categoria.id)
            item['categoria'] = str(nombre)
        
        if self.isv == 1:
            item['isv'] = "0%"
        
        if self.isv == 2:
            item['isv'] = "15%"
        
        if self.isv == 3:
            item['isv'] = "18%"

        if self.pre_compra == None or self.pre_compra == "":
            item['pre_compra'] = 'L. 0.00'
        else:
            item['pre_compra'] = 'L. {:,.2f}'.format(self.pre_compra)
        
        if self.pre_venta == None or self.pre_venta == "":
            item['pre_venta'] = 'L. 0.00'
        else:
            item['pre_venta'] = 'L. {:,.2f}'.format(self.pre_venta)
        
        return item

    def __str__(self):
        return self.nombre


class Cliente(ModelBase):
    identidad = models.CharField('Identidad', max_length=15, unique=True)
    nombre = models.CharField('Nombres ' , max_length=150)
    apellidos = models.CharField('Apellidos', max_length=150, blank=True, null=True)
    telefono = models.CharField('Telefono', max_length=10, blank=True, null=True)
    email = models.EmailField('Email', blank=True, null=True)
    direccion = models.TextField('Direccion ', max_length=300, blank=True, null=True)

    def toJSON(self):
        item = model_to_dict(self, fields=['id','identidad','nombre','apellidos','telefono','email','direccion'])
        return item

    def __str__(self):
        return self.nombre


class Proveedores(ModelBase):
    rtn = models.CharField('RTN', max_length=15, unique=True)
    empresa = models.CharField('Empresa ', max_length=150, blank=True, null=True)
    nombre = models.CharField('Nombres ' , max_length=150)
    apellidos = models.CharField('Apellidos', max_length=150, blank=True, null=True)
    direccion = models.TextField('Direccion ', max_length=300, blank=True, null=True)
    telefono = models.CharField('Telefono', max_length=10, blank=True, null=True)
    phone = models.CharField('Telefono', max_length=10, blank=True, null=True)
    email = models.EmailField('Email', blank=True, null=True)

    def toJSON(self):
        item = model_to_dict(self, fields=['id','empresa','nombre','apellidos','direccion','telefono','phone','email'])
        return item

    def __str__(self):
        return self.empresa
    


def code_compras():
    last_id = Compras.objects.all().order_by('id').last()
    if last_id == None:
        new_last_int = 0 + 1
    else:
        last_int =int(last_id.id)
        new_last_int = last_int + 1
    return 'ORDER' + str(new_last_int).zfill(10)


class Compras(ModelBase):
    codigo = models.CharField('Codigo', max_length=60 , default=code_compras, unique=True)
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE, blank=True, null=True)
    factura = models.CharField('Numero Factura', max_length=150, blank=True , null=True)
    pago = models.IntegerField(choices=((1,("Efectivo")),(2,("Credito")),(3,("Tarjeta"))),default=1)
    isv = models.FloatField(verbose_name='ISV', blank=True, null=True)
    comentarios = models.TextField('Comentarios', max_length=1800, blank=True, null=True)
    subtotal = models.FloatField(verbose_name='Sub Total', blank=True, null=True)
    total = models.FloatField(verbose_name='Total', blank=True, null=True)
    proceso = models.IntegerField(choices=((1,("Compra")),(2,("Finalizado"))),default=1)

    def toJSON(self):
        item = model_to_dict(self, fields=['id','codigo','proveedor','pago','factura','isv','comentarios','subtotal','total','date_create'])
        if self.proveedor != None:
            nombre = Proveedores.objects.get(pk=self.proveedor.id)
            item['proveedor'] = str(nombre)
        
        if self.pago == 1:
            item['pago'] = "Efectivo"
        if self.pago == 2:
            item['pago'] = "Credito"
        if self.pago == 3:
            item['pago'] = "Tarjeta"

        #Fomartos para los numero totales 
        if self.subtotal == None or self.subtotal == "":
            item['subtotal'] = 'L. 0.00'
        else:
            item['subtotal'] = 'L. {:,.2f}'.format(self.subtotal)
        


        if self.isv == None or self.isv == "":
            item['isv'] ='L. 0.00'
        else:
            item['isv'] = 'L. {:,.2f}'.format(self.isv)
        


        if self.total == None or self.total == "":
            item['total'] = 'L. 0.00'
        else:
            item['total'] = 'L. {:,.2f}'.format(self.total)
        
        item['date_create'] = self.date_create
        return item

        return item

    def __str__(self):
        return self.codigo
    


class DetalleCompra(ModelBase):
    compra = models.ForeignKey(Compras, on_delete=models.CASCADE)
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE)
    cantidad = models.DecimalField(verbose_name='Cantidad', max_digits=40, decimal_places=2)
    precio_c = models.DecimalField(verbose_name='Precio Compra', max_digits=40,decimal_places=2)
    precio_v = models.DecimalField(verbose_name='Precio Venta', max_digits=40,decimal_places=2)
    isv = models.FloatField(verbose_name='Isv')
    total = models.FloatField(verbose_name='Total')

    def toJSON(self):
        item = model_to_dict(self)
        return item





def code_ventas():
    last_id = Ventas.objects.all().order_by('id').last()
    if last_id == None:
        new_last_int = 0 + 1
    else:
        last_int =int(last_id.id)
        new_last_int = last_int + 1
    return 'VENTA' + str(new_last_int).zfill(10)


class Ventas(ModelBase):
    codigo = models.CharField('Codigo', max_length=60 , default=code_ventas, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True, null=True)
    pago = models.IntegerField(choices=((1,("Efectivo")),(2,("Credito")),(3,("Tarjeta"))),default=1)
    isv = models.FloatField(verbose_name='ISV', blank=True, null=True)
    comentarios = models.TextField('Comentarios', max_length=1800, blank=True, null=True)
    subtotal = models.FloatField(verbose_name='Sub Total', blank=True, null=True)
    total = models.FloatField(verbose_name='Total', blank=True, null=True)

    def toJSON(self):
        item = model_to_dict(self,exclude=['comentarios'],fields=['id','codigo','cliente','pago','isv','subtotal','total','date_create'])
        if self.cliente != None:
            nombre = Cliente.objects.get(pk=self.cliente.id)
            item['cliente'] = str(nombre)
        else:
            item['cliente']= "Cliente Final"
        
        if self.pago == 1:
            item['pago'] = "Efectivo"
        if self.pago == 2:
            item['pago'] = "Credito"
        if self.pago == 3:
            item['pago'] = "Tarjeta"
        
        #Fomartos para los numero totales 
        if self.subtotal == None or self.subtotal == "":
            item['subtotal'] = 'L. 0.00'
        else:
            item['subtotal'] = 'L. {:,.2f}'.format(self.subtotal)
        


        if self.isv == None or self.isv == "":
            item['isv'] ='L. 0.00'
        else:
            item['isv'] = 'L. {:,.2f}'.format(self.isv)
        


        if self.total == None or self.total == "":
            item['total'] = 'L. 0.00'
        else:
            item['total'] = 'L. {:,.2f}'.format(self.total)
        
        
        item['date_create'] = self.date_create
        return item
    
    def __str__(self):
        return self.codigo
    



class DetalleVentas(ModelBase):
    ventas = models.ForeignKey(Ventas, on_delete=models.CASCADE)
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE)
    cantidad = models.DecimalField(verbose_name='Cantidad', max_digits=4, decimal_places=2)
    precio_c = models.FloatField(verbose_name='Precio Compra')
    precio_v = models.FloatField(verbose_name='Precio Venta')
    isv = models.FloatField(verbose_name='Isv' )
    total = models.FloatField(verbose_name='Total')

    def toJSON(self):
        item = model_to_dict(self)
        return item



class CuentasPorPagar(ModelBase):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    abono = models.FloatField(verbose_name="Abono")
    comentario = models.TextField('Comentario', max_length=800, blank=True, null=True)

    def __str__(self):
        return self.cliente.nombre
    


#Apartado carrito ONLINE
###################################################################### ONLINE ############################################################


#Ventas Online
class CommentarioOnline(ModelBase):
    producto = models.ForeignKey(Componente, on_delete=models.CASCADE)
    comentario = models.TextField('Comentario' , max_length=1800)




def code_carrito():
    last_id = Carrito.objects.all().order_by('id').last()
    if last_id == None:
        new_last_int = 0 + 1
    else:
        last_int =int(last_id.id)
        new_last_int = last_int + 1
    return 'CAR' + str(new_last_int).zfill(10)

class Carrito(ModelBase):
    codigo = models.CharField('Codigo', max_length=60 , default=code_carrito, unique=True)
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_username" ,blank=True, null=True)
    pago = models.IntegerField(choices=((1,("Pagar al Entregar")),(2,("Tigo Money")),(3,("Transferencia Bancaria")),(4,("Paypal"))),default=1)
    isv = models.FloatField(verbose_name='ISV', blank=True, null=True)
    comentarios = models.TextField('Comentarios', max_length=1800, blank=True, null=True)
    subtotal = models.FloatField(verbose_name='Sub Total', blank=True, null=True)
    total = models.FloatField(verbose_name='Total', blank=True, null=True)
    activo = models.BooleanField(default=True) #Estatus de compras activas 
    estado = models.IntegerField(choices=((1,("Compra Iniciada")),(2,("Confimacion de Compra")),(3,("Proceso de envio")),(4,("Entregado"))),default=1)


    def toJSON(self):
        item = model_to_dict(self,exclude=['comentarios'],fields=['id','codigo','cliente','pago','isv','subtotal','total','date_create'])
        if self.cliente != None:
            nombre = User.objects.get(pk=self.cliente.id)
            item['cliente'] = str(nombre)
        else:
            item['cliente']= "Cliente Final"
        
        if self.pago == 1:
            item['pago'] = "Pagar al Entregar"
        if self.pago == 2:
            item['pago'] = "Tigo Money"
        if self.pago == 3:
            item['pago'] = "Transferencia Bancaria"
        if self.pago == 4:
            item['pago'] = "Paypal"
        
        #Fomartos para los numero totales 
        if self.subtotal == None or self.subtotal == "":
            item['subtotal'] = '$. 0.00'
        else:
            item['subtotal'] = '$. {:,.2f}'.format(self.subtotal)
        


        if self.isv == None or self.isv == "":
            item['isv'] ='$. 0.00'
        else:
            item['isv'] = '$. {:,.2f}'.format(self.isv)
        


        if self.total == None or self.total == "":
            item['total'] = '$. 0.00'
        else:
            item['total'] = '$. {:,.2f}'.format(self.total)
        
        
        item['date_create'] = self.date_create
        return item


    def __str__(self):
        return self.codigo


class Detalle_Carrito(ModelBase):
    codigo = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE)
    cantidad = models.DecimalField(verbose_name='Cantidad', max_digits=4, decimal_places=2)
    precio_c = models.FloatField(verbose_name='Precio Compra')
    precio_v = models.FloatField(verbose_name='Precio Venta')
    isv = models.FloatField(verbose_name='Isv' )
    total = models.FloatField(verbose_name='Total')

    def __str__(self):
        return self.codigo


class Detalle_envio(ModelBase):
    codigo = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    nombre = models.CharField('Nombre Completo ', max_length=100)
    telefono = models.CharField('Telefono', max_length=11)
    telefono2 = models.CharField('Telefono (Opcional)', max_length=11, blank=True, null=True)
    direccion = models.TextField('Direccion', max_length=600)
    direccion2 = models.TextField('Direccion (Opcional)', max_length=600, blank=True, null=True)
    email = models.EmailField('Correo Electronico', blank=True, null=True)
    email2 = models.EmailField('Correo Electronico', blank=True, null=True)

    #def __str__(self):
    #    return self.codigo

    
