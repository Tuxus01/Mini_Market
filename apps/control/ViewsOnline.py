from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from .models import *
from .forms import *
from django.utils import timezone
from django.contrib.auth.decorators import permission_required

#Login
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView
import Mini_Marker.settings as setting


#JSON API
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .email import *
import threading
import json
#Email
from django.core.mail import send_mail,EmailMultiAlternatives
from django.core.files import File
from django.core.files.base import ContentFile
from django.template import loader


from datetime import date
from datetime import datetime
import datetime

from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from .views import *

from django.contrib.auth.middleware import RemoteUserMiddleware
from social_django.models import UserSocialAuth



#Buscador Global
#@login_required(login_url='/login/')
def buscar(texto):
    print(texto)
    componente = Componente.objects.filter(online=True).filter(Q(categoria__nombre__icontains=texto) | Q(nombre__icontains=texto) | Q(talla__nombre__icontains=texto) | Q(subcategoria__nombre__icontains=texto) | Q(color__nombre__icontains=texto)  )
    #componente = Componente.objects.filter(online=True).filter(categoria__nombre__icontains=texto).filter(nombre__icontains=texto)
    #Iterar componentes con items > 0 
    compo = []
    for i in componente:
        if i.stock_actual > 0:
            compo.append(i)
    return compo



#Compras Online
#@login_required(login_url='/login/')
def store_view(request):
    client_ip = request.META['REMOTE_ADDR']

    '''
    user = request.user
    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None
    '''
    

    print(client_ip)
    #Aplicando el buscador de componente globales
    if request.method == 'GET':
        search = request.GET.get('buscar')
        if search != None:
            items = buscar(search)
            paginator = Paginator(items, 20) # Show 25 contacts per page.
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            ctx = {'ITEMS' : items , 'page_obj': page_obj,}
            return render(request, 'base/online/storeSearch.html' ,ctx )
            #return HttpResponseRedirect('/store/search/' , ctx)
    #Aplicando el buscador de componente globales      
    #listar los ultimos 20 registros que tienen activo ONLINE
    articulos = []
    componente = Componente.objects.filter(online=True).order_by('-id')[:20]
    #Extraer componentes que cumplan con stock disponible para ventas
    for i in componente:
        if i.stock_actual > 0:
            articulos.append(i)

    

    subcategoria = SubCategoria.objects.all()
    #Enviar cantidad de objetos por orden a template
    ################Aplicando la compra sin loge
    if request.user.is_authenticated:
        car_ord = Carrito.objects.filter(activo=True).filter(owner=request.user)[:1]
    else:
        car_ord = 0
    car_int = Detalle_Carrito.objects.filter(codigo=car_ord)
    ctx = {'Lista': articulos,'SUBCATEGORIA': subcategoria, 'CAR_INT':car_int.count()}
    return render(request, 'base/store.html' ,ctx )

#Producto ID Y agregado de Carrito !! IMPORTANTE
#@login_required(login_url='/login/')
def store_view_id(request, id):
    
    #Aplicando el buscador de componente globales
    if request.method == 'GET':
        search = request.GET.get('buscar')
        if search != None:
            items = buscar(search)
            paginator = Paginator(items, 20) # Show 25 contacts per page.
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            ctx = {'ITEMS' : items , 'page_obj': page_obj,}
            return render(request, 'base/online/storeSearch.html' ,ctx )
            #return HttpResponseRedirect('/store/search/' , ctx)
    detalle = Componente.objects.get(pk=id)

    #Metodo para agregar al carrito y validacion de orden de compra abierta
    if request.method == 'POST':

        #Validar si hay orden abierta ?
        if request.user.is_authenticated:
            instanacias = Carrito.objects.filter(activo=True).filter(owner=request.user)[:1]
        else:
            instanacias = 0
        if instanacias:
            qty = request.POST.get('quantity')
            #Validar el el producto esta agregado ya ? y sumarle la cantidad
            #detalle_v = Detalle_Carrito.objects.filter(componente=detalle)

            #Modificando componentes de Carrito 
            if Detalle_Carrito.objects.filter(codigo=instanacias).filter(componente=detalle):
                #Agregando Item y sumando a la orden abierta por el cliente
                print("Detalles ++ agregados ")
                #extraer id para realizar su modificacion
                isn = Detalle_Carrito.objects.filter(codigo=instanacias).filter(componente=detalle)[:1]
                ids = Detalle_Carrito.objects.get(pk=isn)
                cantidad = float(ids.cantidad)
                ids.cantidad = cantidad + float(qty)
                ids.save()
                print("Se salvo los datos")

            else:
                print("Detalles nuevos -- ")
                #Agregando nuevos iten a la orden abierta del cliente
                detalle_c = Detalle_Carrito()
                detalle_c.owner = request.user
                detalle_c.codigo = Carrito.objects.get(pk=instanacias)
                detalle_c.componente = detalle
                detalle_c.cantidad = float(request.POST.get('quantity'))
                detalle_c.precio_c = detalle.pre_compra
                detalle_c.precio_v = detalle.pre_venta
                #Calculo del ISV
                if detalle.isv == 1:
                    isv_c = 0
                if detalle.isv == 2:
                    isv_c = 0.15
                if detalle.isv == 3:
                    isv_c = 0.18
                
                detalle_c.isv = (float(detalle.pre_venta) * float(isv_c)) * float(request.POST.get('quantity'))
                detalle_c.total = (float(detalle.pre_venta) * float(request.POST.get('quantity'))) + (float(detalle.pre_venta) * float(isv_c)) * float(request.POST.get('quantity'))
                detalle_c.save()
                

        else:
            #Crear orden de compra
            if request.user.is_authenticated:
                crear_orden = Carrito()
                crear_orden.owner = request.user
                crear_orden.cliente = request.user
                crear_orden.save()
            else:
                print("por favor crea una cuenta ")
                crear_orden = 0
                return HttpResponseRedirect('/signup')
            #agregar detalle a la orden 
            if crear_orden:
                detalle_c = Detalle_Carrito()
                detalle_c.owner = request.user
                detalle_c.codigo = crear_orden
                detalle_c.componente = detalle
                detalle_c.cantidad = float(request.POST.get('quantity'))
                detalle_c.precio_c = detalle.pre_compra
                detalle_c.precio_v = detalle.pre_venta
                #Calculo del ISV
                if detalle.isv == 1:
                    isv_c = 0
                if detalle.isv == 2:
                    isv_c = 0.15
                if detalle.isv == 3:
                    isv_c = 0.18
                
                detalle_c.isv = (float(detalle.pre_venta) * float(isv_c)) * float(request.POST.get('quantity'))
                detalle_c.total = (float(detalle.pre_venta) * float(request.POST.get('quantity'))) + (float(detalle.pre_venta) * float(isv_c)) * float(request.POST.get('quantity'))
                detalle_c.save()

    if request.user.is_authenticated:   
        car_ord = Carrito.objects.filter(activo=True).filter(owner=request.user)[:1]
    else:
        car_ord = 0

    car_int = Detalle_Carrito.objects.filter(codigo=car_ord)
    ctx = {'DETALLE' : detalle,'CAR_INT':car_int.count()}
    return render(request, 'base/online/store_view.html' , ctx)

#Json Request Finalizacion de pago por Paypal:
#Este proceso finaliza la venta Online
#@login_required(login_url='/login/')
def paymentComplete(request):
    body = json.loads(request.body)
    print('body : ', body)
    #Captura de la orden 
    order = Carrito.objects.filter(codigo=body['ordenId'])[:1]
    #Proceso de desactivacion de compra
    orden = Carrito.objects.get(pk=order)
    orden.activo = False
    
    #Rebajar los productos
    ids = orden
    detalles = Detalle_Carrito.objects.filter(codigo=ids)

    #Variables para calcular totales por segunda vez
    isv_15 = 0
    isv_18 = 0
    subtotal = 0
    total = 0
    isv_por = 0

    for i in detalles:
        #Proceso de calculos totales
        if i.componente.isv == 1:
            isv_por += ((float(i.precio_v) * float(i.cantidad)) * 0 ) 
        if i.componente.isv == 2:
            isv_por +=  ((float(i.precio_v) * float(i.cantidad)) * 0.15 ) 
            isv_15 += ((float(i.precio_v) * float(i.cantidad)) * 0.15 ) 
        if i.componente.isv == 3:
            isv_por +=  ((float(i.precio_v) * float(i.cantidad))* 0.18 ) 
            isv_18 += ((float(i.precio_v) * float(i.cantidad))* 0.18 ) 
        
        subtotal += (float(i.precio_v) * float(i.cantidad) - isv_por )
        total += (float(i.precio_v) * float(i.cantidad) )


        #Proceso de rebaja de productos de Componente Items
        item = i.componente.id
        comp = Componente.objects.get(pk=item)

        #Validar si el stock cumple con el requerimiento.
        if comp.stock_actual >= i.cantidad:
            #print(i.componente.nombre)
            #print(i.cantidad)
            #print(comp.stock_actual)
            comp.stock_actual -= i.cantidad

            #Guardar el cambio de registros
            comp.save()
            #print(comp.stock_actual)
        else:
            print("este producto no se puede vender")
        #print(comp)
    #Guardar Cambio de Orden a estatus a Vendido
    orden.isv = isv_15 + isv_18
    orden.subtotal = subtotal
    orden.total = total

    #print(isv_15)
    #print(isv_18)
    #print(subtotal)
    #print(total)
    #Guardar orden de compra Finalizacion sin retorno
    orden.save()
    
    


    #Envio de correo electronico de compra.
    print("estamos enviando correo electronico de la orden : " + str(orden))
    
    return JsonResponse("Pago Completado", safe=False)

#@login_required(login_url='/login/')
def store_categoria(request,Model):

    if request.method == 'GET':
        search = request.GET.get('buscar')
        if search != None:
            items = buscar(search)
            paginator = Paginator(items, 20) # Show 25 contacts per page.
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            ctx = {'ITEMS' : items , 'page_obj': page_obj,}
            return render(request, 'base/online/storeSearch.html' ,ctx )

    subcategoria = SubCategoria.objects.get(pk=Model)
    componente = Componente.objects.filter(subcategoria=subcategoria.id).order_by('color').order_by('talla')
    talla = Talla.objects.all()
    color = Color.objects.all()
    cate = Categoria.objects.all()
    subcategorias = SubCategoria.objects.all()

                    
    if request.user.is_authenticated:
        car_ord = Carrito.objects.filter(activo=True).filter(owner=request.user)[:1]
    else:
        car_ord = 0
    car_int = Detalle_Carrito.objects.filter(codigo=car_ord)
    ctx = {'CAR_INT':car_int.count(), "COMPONENTE": componente, 'CATEGORIA':cate ,'SUBCATEGORIA': subcategorias ,'COLOR': color, 'TALLA': talla}
    return render(request, "base/online/categoria.html" , ctx)
    #return HttpResponseRedirect('/store/'+ str(Model) +'/list')

#Compras SHOP all Categoria
#@login_required(login_url='/login/')
def Shop(request):

    if request.method == 'GET':
        search = request.GET.get('buscar')
        if search != None:
            items = buscar(search)
            paginator = Paginator(items, 20) # Show 25 contacts per page.
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            car_ord = Carrito.objects.filter(activo=True).filter(owner=request.user)[:1]
            car_int = Detalle_Carrito.objects.filter(codigo=car_ord)
            ctx = {'CAR_INT':car_int.count(), 'ITEMS' : items , 'page_obj': page_obj,}
            return render(request, 'base/online/storeSearch.html' ,ctx )

    subcategorias = SubCategoria.objects.all()
    

    #catego = request.GET.get('Limpieza')
    #print(catego)

    


    articulos = [] #Todos los articulos
    articulosxCategori = [] #Articulos filtrados por categoria
    cate_list = [] #Categorias de producto activos
    subcate_list = [] #SubCategorias de producto activos
    talla_list = [] #Tallas de productos activos
    check_list_active = []

    componente = Componente.objects.filter(online=True).order_by('-id')

    cate = Categoria.objects.all()
    


    #Extraer componentes que cumplan con stock disponible para ventas
    for i in componente:
        if i.stock_actual > 0:
            articulos.append(i)


    #Buscador por Ctegorias
    for i in cate:
        if i.nombre == request.GET.get(i.nombre):
            check_list_active.append({'nombre':request.GET.get(i.nombre), 'tipo':'categoria', 'check':'si'}) #agregamos el dato a buscar, para retornarlo al template y rellenar los item activos
            for c in articulos:
                #print(c.categoria.nombre)
                if c.categoria.nombre == i.nombre:
                    #print(c)
                    articulosxCategori.append(c)
        else:
            pass
            #check_list_active.append({'nombre':i.nombre, 'tipo':'categoria', 'check':'no'})


    #Buscar por SubCategoria
    for i in SubCategoria.objects.all():
        if request.GET.get(i.nombre):
            check_list_active.append({'nombre':request.GET.get(i.nombre), 'tipo':'subcategoria', 'check':'si'})
            if i.nombre == str(request.GET.get(i.nombre)):
                for c in articulos:
                    if c.subcategoria:
                        if c.subcategoria.nombre == i.nombre:
                            articulosxCategori.append(c)
                            #print(c.subcategoria)
                
    #Buscar por Tala
    for i in Talla.objects.all():
        if request.GET.get(i.nombre):
            check_list_active.append({'nombre':request.GET.get(i.nombre), 'tipo':'talla', 'check':'si'})
            if i.nombre == str(request.GET.get(i.nombre)):
                for c in articulos:
                    if c.talla:
                        if c.talla.nombre == i.nombre:
                            articulosxCategori.append(c)
                            #print(c.subcategoria)

        '''if i.nombre == request.GET.get(i.nombre):
            for c in articulos:
                if c.subcategoria.nombre == i.nombre:
                    articulosxCategori.append(c)'''
    


    #Solo muestra las categorias activas
    #Validar categorias activas en producto
    for i in Categoria.objects.all():
        for c in articulos:
            if c.categoria:
                if i.nombre == c.categoria.nombre:
                    cate_list.append(i)
                    break
            else:
                break


    for i in SubCategoria.objects.all():
        for c in articulos:
            if c.subcategoria:
                if i.nombre == c.subcategoria.nombre:
                    subcate_list.append(i)
                    break  
            else:
                break     
        #cate_list.append(i)
    

    for i in Talla.objects.all():
        for c in articulos:
            if c.talla:
                if i.nombre == c.talla.nombre:
                    talla_list.append(i)
                    break


    

    if articulosxCategori:
        paginator = Paginator(articulosxCategori, 10) # Show 10 productos 
    else:
        paginator = Paginator(articulos, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.user.is_authenticated:
        car_ord = Carrito.objects.filter(activo=True).filter(owner=request.user)[:1]
    else:
        car_ord = 0

    car_int = Detalle_Carrito.objects.filter(codigo=car_ord)
    ctx = {'CAR_INT':car_int.count(), 'page_obj': page_obj, 'SUBCATEGORIA':subcate_list,'CATEGORIA':cate_list, 'TALLA':talla_list ,'CHECK':check_list_active}
    return render(request, 'base/online/shop.html' , ctx)

#Listado de productos y pago
#@login_required(login_url='/login/')
def carrito_list(request):
    if request.user.is_authenticated:
        instanacias = Carrito.objects.filter(activo=True).filter(owner=request.user)[:1]
    else:
        instanacias = 0


    detalle = Detalle_Carrito.objects.filter(codigo=instanacias)
    isv_15 = 0
    isv_18 = 0
    subtotal = 0
    total = 0
    isv_por = 0
    #Calculos de pago
    for i in detalle:
        #validar el % de interes por producto
        if i.componente.isv == 1:
            isv_por += ((float(i.precio_v) * float(i.cantidad)) * 0 ) 
        if i.componente.isv == 2:
            isv_por +=  ((float(i.precio_v) * float(i.cantidad)) * 0.15 ) 
            isv_15 += ((float(i.precio_v) * float(i.cantidad)) * 0.15 ) 
        if i.componente.isv == 3:
            isv_por +=  ((float(i.precio_v) * float(i.cantidad))* 0.18 ) 
            isv_18 += ((float(i.precio_v) * float(i.cantidad))* 0.18 ) 
        
        subtotal += (float(i.precio_v) * float(i.cantidad) - isv_por )
        total += (float(i.precio_v) * float(i.cantidad) )

    #print(total)
    if request.user.is_authenticated:
        car_ord = Carrito.objects.filter(activo=True).filter(owner=request.user)[:1]
    else:
        car_ord = 0
    car_int = Detalle_Carrito.objects.filter(codigo=car_ord)
    #ctx = {'Lista': articulos,'SUBCATEGORIA': subcategoria, 'CAR_INT':car_int.count()}

    ctx = {'ITEMS' : instanacias, 'DETALLES':detalle, 'ISV_18':isv_18 , 'ISV_15':isv_15 , 'SUBTOTAL': subtotal, 'TOTAL':total,  'CAR_INT':car_int.count()}
    return render(request, 'base/online/cart.html' , ctx)

#@login_required(login_url='/login/')
def carrito_check(request):
    #Variable que habilita el pago por paypal
    status = 0
    if request.method == 'POST':
        status = 1

    if request.user.is_authenticated:
        instanacias = Carrito.objects.filter(activo=True).filter(owner=request.user)[:1]
        #Enviar item para finalizar pago paypal para funcion final
        paypal_fin = Carrito.objects.get(pk=instanacias)
    else:
        instanacias = 0
        paypal_fin = 0

    
    
    detalle = Detalle_Carrito.objects.filter(codigo=instanacias)
    isv_15 = 0
    isv_18 = 0
    subtotal = 0
    total = 0
    isv_por = 0
    #Calculos de pago
    for i in detalle:
        #validar el % de interes por producto
        if i.componente.isv == 1:
            isv_por += ((float(i.precio_v) * float(i.cantidad)) * 0 ) 
        if i.componente.isv == 2:
            isv_por +=  ((float(i.precio_v) * float(i.cantidad)) * 0.15 ) 
            isv_15 += ((float(i.precio_v) * float(i.cantidad)) * 0.15 ) 
        if i.componente.isv == 3:
            isv_por +=  ((float(i.precio_v) * float(i.cantidad))* 0.18 ) 
            isv_18 += ((float(i.precio_v) * float(i.cantidad))* 0.18 ) 
        
        subtotal += (float(i.precio_v) * float(i.cantidad) - isv_por )
        total += (float(i.precio_v) * float(i.cantidad) )

    #Extraer Direccion de envios por usuario
    if request.user.is_authenticated:
        cliente = Detalle_envio.objects.filter(owner=request.user).last()
    else:
        cliente = ""

    #print(total)
    ctx = {'ITEMS' : instanacias,'ITEMP':paypal_fin, 'DETALLES':detalle, 'ISV_18':isv_18 , 'ISV_15':isv_15 , 'SUBTOTAL': subtotal, 'TOTAL':total, 'DIRECCION':cliente, 'STATUS':status}
    return render(request, 'base/online/check.html' , ctx)

#Funcion encargada de agregar a la lista de compras de x usuario
#@login_required(login_url='/login/')
def AddCarrito(request):
    pass
