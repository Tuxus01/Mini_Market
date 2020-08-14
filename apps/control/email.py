
from django.template import loader
import os
import sys
import datetime 
import threading
from .models import *
from datetime import date
from datetime import datetime
#Email
from django.core.mail import send_mail,EmailMultiAlternatives



from django.core.files import File
from django.core.files.base import ContentFile


def Email():
    print("enviando un email")


#Envio del email al administrador reportando acceso no autorizado
class SendEmailThread(threading.Thread):
    def __init__(self, id ):
        threading.Thread.__init__(self)
        #self.adjunto = adjunto
        self.id = id
        
    def run(self):
        ordenventa = Ventas.objects.get(pk=self.id)
        detalle = DetalleVentas.objects.filter(ventas=ordenventa.id)
        #print(detalle)
        cliente = ordenventa.cliente.email
        #subject, from_email, to = 'Compra al Credito', 'ngdz01@gmail.com', 'tuxus01@gmail.com'
        #msg = EmailMultiAlternatives(subject, from_email, [to])
        html_content = loader.render_to_string('base/SendEmail.html', {'VENTA':ordenventa, 'DETALLE':detalle})
        #msg.attach_alternative(html_content, "text/html")
        #msg.send()

        #Envio de Email
        subject, from_email, to = 'Compra al Credito', 'ngdz01@gmail.com', str(cliente)
        #text_content = 'Compra : {0} <br> Por el monto total 100.00 <br> '.format(self.Nombre_camara)
        #html_content = '<p>Se autorizo compra al credio al numero de factura: {0} </p> '.format(self.Nombre_camara)
        msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
        #msg.attach_file(self.adjunto)
        msg.attach_alternative(html_content, "text/html")
        msg.send()




class SendEmailAbonoThread(threading.Thread):
    def __init__(self, cliente, detalleAbono ):
        threading.Thread.__init__(self)
        #self.adjunto = adjunto
        self.cliente = cliente
        self.detalleAbono = detalleAbono
        #self.deuda_actual = deuda_actual
        
    def run(self):
        #ordenventa = Ventas.objects.get(pk=self.id)
        #detalle = DetalleVentas.objects.filter(ventas=ordenventa.id)
        
        cliente = self.cliente.email
       
        html_content = loader.render_to_string('base/SendEmailAbono.html', {'VENTA':self.cliente, 'DETALLE':self.detalleAbono } )
        #msg.attach_alternative(html_content, "text/html")
        #msg.send()

        #Envio de Email
        subject, from_email, to = 'Compra al Credito', 'ngdz01@gmail.com', str(cliente)
        #text_content = 'Compra : {0} <br> Por el monto total 100.00 <br> '.format(self.Nombre_camara)
        #html_content = '<p>Se autorizo compra al credio al numero de factura: {0} </p> '.format(self.Nombre_camara)
        msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
        #msg.attach_file(self.adjunto)
        msg.attach_alternative(html_content, "text/html")
        msg.send()




class SendEmailInfoThread(threading.Thread):
    def __init__(self, producto, cantidad ):
        threading.Thread.__init__(self)
        #self.adjunto = adjunto
        self.producto = producto
        self.cantidad = cantidad
        #self.deuda_actual = deuda_actual
        
    def run(self):
        #ordenventa = Ventas.objects.get(pk=self.id)
        #detalle = DetalleVentas.objects.filter(ventas=ordenventa.id)
        
        #cliente = self.cliente.email
       
        #html_content = loader.render_to_string('base/SendEmailAbono.html', {'VENTA':self.cliente, 'DETALLE':self.detalleAbono } )
        #msg.attach_alternative(html_content, "text/html")
        #msg.send()

        #Envio de Email
        subject, from_email, to = 'Alerta de productos bajos', 'ngdz01@gmail.com','ngdz01@gmail.com'
        #text_content = 'Compra : {0} <br> Por el monto total 100.00 <br> '.format(self.Nombre_camara)
        html_content = 'Informando que solo quedan - {0} {1}  '.format(self.cantidad,self.producto)
        msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
        #msg.attach_file(self.adjunto)
        #msg.attach_alternative(html_content, "text/html")
        msg.send()


##Email de venta Online

#Envio del email al administrador reportando acceso no autorizado
class SendEmailOnlineThread(threading.Thread):
    def __init__(self, id, usuario,Tipo_Pago, Proceso ):
        threading.Thread.__init__(self)
        #self.adjunto = adjunto
        self.id = id
        self.usuario = usuario
        self.Tipo_Pago = Tipo_Pago
        self.Proceso = Proceso
        print(self.id)
        
    def run(self):
        proceso = ""
        if self.Proceso == 1:
            proceso = "Compra Iniciada"
        if self.Proceso == 2:
            proceso = "Confimacion de Compra"
        if self.Proceso == 3:
            proceso = "Proceso de envio"
        if self.Proceso == 4:
            proceso = "Entregado"


        ordenventa = Carrito.objects.get(pk=self.id)
        detalle = Detalle_Carrito.objects.filter(codigo=ordenventa.id)
        
        #Detalle de envio
        cliente = Detalle_envio.objects.filter(owner=self.usuario).last()
        print(cliente.email)
        

        html_content = loader.render_to_string('base/online/SendEmailOnline.html', {'VENTA':ordenventa, 'DETALLE':detalle, 'CLIENTE':cliente, 'Tipo_Pago':self.Tipo_Pago, 'PROCESO':proceso})
        #msg.attach_alternative(html_content, "text/html")
        #msg.send()

        #Envio de Email
        subject, from_email, to = 'Orden Online', 'ngdz01@gmail.com', str(cliente.email)
        #text_content = 'Compra : {0} <br> Por el monto total 100.00 <br> '.format(self.Nombre_camara)
        #html_content = '<p>Se autorizo compra al credio al numero de factura: {0} </p> '.format(self.Nombre_camara)
        msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
        #msg.attach_file(self.adjunto)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        
        