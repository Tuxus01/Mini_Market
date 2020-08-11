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
from .ViewsOnline import *

from social_django.models import UserSocialAuth


class LoginFormView(LoginView):
    template_name = 'base/login.html'
    success_url = reverse_lazy('base:index')
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(setting.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar sesión'
        return context

class LogoutRedirectView(RedirectView):
    pattern_name = 'login'
    success_url = reverse_lazy('base:login')
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)


@login_required(login_url='/login/')
@method_decorator(csrf_exempt)
@permission_required('is_staff', login_url='/store')
def Index(request):
    #today = date.today()
    #Cantidad y Gasto Global de clientes
    total_dinero = 0
    cliente_t = Cliente.objects.all().count()
    for i in Ventas.objects.all():
        if i.total == None or i.total < 0:
            total_dinero += 0
        else:
            total_dinero += i.total
    #Cantidad y Gasto Global de clientes

    #Cantidad y Gasto Global de Proveedores
    total_dinero_compras = 0
    proveedor = Proveedores.objects.all().count()
    for c in Compras.objects.all():
        if c.total == None or c.total < 0:
            total_dinero_compras += 0
        else:
            total_dinero_compras += c.total
    #Cantidad y Gasto Global de Proveedores

    #Clientes que deben actualmente y su monto
    cliente = Cliente.objects.all()
    ventas = Ventas.objects.filter(pago=2)
    cuentas = CuentasPorPagar.objects.all()
    datos = []
    total_ventas = 0
    total_abono = 0
    total_resta = 0 
    cuenta_cobrar_total = 0
    for i in cliente:
        print("Iniciando : " + str(i.nombre))
        for c in ventas:
            if i.id == c.cliente.id:
                total_ventas += float(c.total)
                print("Cliente que debe : " + str(i.nombre))

        for u in cuentas:
            if i.id == u.cliente.id:
                total_abono += float(u.abono)
                print("Abono :" + str(u.cliente.nombre) + " De : " + str(u.abono))
                
        if total_ventas > 0 and total_abono < total_ventas:
            print("Total Venta :" + str(total_ventas))
            print("Total Abono :" + str(total_abono))
            total_resta = total_ventas - total_abono
            print("Total Resta :" + str(total_resta))
            cuenta_cobrar_total += total_resta
            print("Sumando Restas  :" + str(cuenta_cobrar_total))
            datos.append({'id':str(i.id),'identidad':str(i.identidad),'nombre':str(i.nombre),'apellidos':str(i.apellidos), 'ventas':str(total_ventas), 'abono':str(total_abono), 'restante':str(total_resta)})
            total_resta = 0
            total_ventas = 0
            total_abono = 0
            #cuenta_cobrar_total = 0
    #print(len(datos))
    #print(cuenta_cobrar_total)
    #Clientes que deben actualmente y su monto


    #TOtal invertido en compras
    total_compras_final = 0 
    conteo = Compras.objects.all().count()
    for i in Compras.objects.all():
        if i.pago == 1:
            if i.total == None or i.total == 0:
                total_compras_final += 0
            else:
                total_compras_final += i.total
    
    #TOtal invertido en compras


    #Graficos
    Ventas_Semanales = []
    Compras_Semanales = []
    ahora = datetime.datetime.utcnow()
    ahoraC = 0 #Ventas
    ahoraCC = 0 #Compras
    ayer1 = ahora - datetime.timedelta(days=1)
    ayer1C = 0
    ayer1CC = 0
    ayer2 = ahora - datetime.timedelta(days=2)
    ayer2C = 0
    ayer2CC = 0
    ayer3 = ahora - datetime.timedelta(days=3)
    ayer3C = 0
    ayer3CC = 0
    ayer4 = ahora - datetime.timedelta(days=4)
    ayer4C = 0
    ayer4CC = 0
    ayer5 = ahora - datetime.timedelta(days=5)
    ayer5C = 0
    ayer5CC = 0
    ayer6 = ahora - datetime.timedelta(days=6)
    ayer6C = 0
    ayer6CC = 0
    ayer7 = ahora - datetime.timedelta(days=7)
    ayer7C = 0
    ayer7CC = 0

    #Semana Pasada
    ayer8 = ahora - datetime.timedelta(days=8)
    ayer8C = 0
    ayer8CC = 0
    ayer9 = ahora - datetime.timedelta(days=9)
    ayer9C = 0
    ayer9CC = 0
    ayer10 = ahora - datetime.timedelta(days=10)
    ayer10C = 0
    ayer10CC = 0
    ayer11 = ahora - datetime.timedelta(days=11)
    ayer11C = 0
    ayer11CC = 0
    ayer12 = ahora - datetime.timedelta(days=12)
    ayer12C = 0
    ayer12CC = 0
    ayer13 = ahora - datetime.timedelta(days=13)
    ayer13C = 0
    ayer13CC = 0
    ayer14 = ahora - datetime.timedelta(days=14)
    ayer14C = 0
    ayer14CC = 0
    ayer15 = ahora - datetime.timedelta(days=15)
    ayer15C = 0
    ayer15CC= 0

    repor = Ventas.objects.all()
    for i in repor:
        if i.date_create == ahora.date():
            if i.total == None or i.total == 0:
                ahoraC += 0
            else:
                ahoraC += i.total
        if i.date_create == ayer1.date():
            if i.total == None or i.total == 0:
                ayer1C += 0
            else:
                ayer1C += i.total
        if i.date_create == ayer2.date():
            if i.total == None or i.total == 0:
                ayer2C += 0
            else:
                ayer2C += i.total
        if i.date_create == ayer3.date():
            if i.total == None or i.total == 0:
                ayer3C += 0
            else:
                ayer3C += i.total
        if i.date_create == ayer4.date():
            if i.total == None or i.total == 0:
                ayer4C += 0
            else:
                ayer4C += i.total
        if i.date_create == ayer5.date():
            if i.total == None or i.total == 0:
                ayer5C += 0
            else:
                ayer5C += i.total
        if i.date_create == ayer6.date():
            if i.total == None or i.total == 0:
                ayer6C += 0
            else:
                ayer6C += i.total
        if i.date_create == ayer7.date():
            if i.total == None or i.total == 0:
                ayer7C += 0
            else:
                ayer7C += i.total
        
        #Semana Pasada
        if i.date_create == ayer8.date():
            if i.total == None or i.total == 0:
                ayer8C += 0
            else:
                ayer8C += i.total
        if i.date_create == ayer9.date():
            if i.total == None or i.total == 0:
                ayer9C += 0
            else:
                ayer9C += i.total
        if i.date_create == ayer10.date():
            if i.total == None or i.total == 0:
                ayer10C += 0
            else:
                ayer10C += i.total
        if i.date_create == ayer11.date():
            if i.total == None or i.total == 0:
                ayer11C += 0
            else:
                ayer11C += i.total
        if i.date_create == ayer12.date():
            if i.total == None or i.total == 0:
                ayer12C += 0
            else:
                ayer12C += i.total
        if i.date_create == ayer13.date():
            if i.total == None or i.total == 0:
                ayer13C += 0
            else:
                ayer13C += i.total
        if i.date_create == ayer14.date():
            if i.total == None or i.total == 0:
                ayer14C += 0
            else:
                ayer14C += i.total
        if i.date_create == ayer15.date():
            if i.total == None or i.total == 0:
                ayer15C += 0
            else:
                ayer15C += i.total


    
    comp = Compras.objects.all()
    for i in comp:
        if i.date_create == ahora.date():
            if i.total == None or i.total == 0:
                ahoraCC += 0
            else:
                ahoraCC += i.total
        if i.date_create == ayer1.date():
            if i.total == None or i.total == 0:
                ayer1CC += 0
            else:
                ayer1CC += i.total
        if i.date_create == ayer2.date():
            if i.total == None or i.total == 0:
                ayer2CC += 0
            else:
                ayer2CC += i.total
        if i.date_create == ayer3.date():
            if i.total == None or i.total == 0:
                ayer3CC += 0
            else:
                ayer3CC += i.total
        if i.date_create == ayer4.date():
            if i.total == None or i.total == 0:
                ayer4CC += 0
            else:
                ayer4C += i.total
        if i.date_create == ayer5.date():
            if i.total == None or i.total == 0:
                ayer5CC += 0
            else:
                ayer5CC += i.total
        if i.date_create == ayer6.date():
            if i.total == None or i.total == 0:
                ayer6CC += 0
            else:
                ayer6CC += i.total
        if i.date_create == ayer7.date():
            if i.total == None or i.total == 0:
                ayer7CC += 0
            else:
                ayer7CC += i.total
        
        #Semana Pasada
        if i.date_create == ayer8.date():
            if i.total == None or i.total == 0:
                ayer8CC += 0
            else:
                ayer8CC += i.total
        if i.date_create == ayer9.date():
            if i.total == None or i.total == 0:
                ayer9CC += 0
            else:
                ayer9CC += i.total
        if i.date_create == ayer10.date():
            if i.total == None or i.total == 0:
                ayer10CC += 0
            else:
                ayer10CC += i.total
        if i.date_create == ayer11.date():
            if i.total == None or i.total == 0:
                ayer11C += 0
            else:
                ayer11CC += i.total
        if i.date_create == ayer12.date():
            if i.total == None or i.total == 0:
                ayer12CC += 0
            else:
                ayer12C += i.total
        if i.date_create == ayer13.date():
            if i.total == None or i.total == 0:
                ayer13CC += 0
            else:
                ayer13CC += i.total
        if i.date_create == ayer14.date():
            if i.total == None or i.total == 0:
                ayer14CC += 0
            else:
                ayer14CC += i.total
        if i.date_create == ayer15.date():
            if i.total == None or i.total == 0:
                ayer15CC += 0
            else:
                ayer15CC += i.total
        
    #Carga de informacion para el reporte de ventas semanal versus semana anterior
    Ventas_Semanales.append({'ahoraC': ahoraC, 'ayer8C': ayer8C, 'ayer1C': ayer1C, 'ayer9C': ayer9C, 'ayer2C': ayer2C, 'ayer10C': ayer10C,'ayer3C': ayer3C, 'ayer11C': ayer11C,'ayer4C': ayer4C, 'ayer12C': ayer12C,'ayer5C': ayer5C, 'ayer13C': ayer13C,'ayer6C': ayer6C, 'ayer14C': ayer14C,'ayer7C': ayer7C, 'ayer15C': ayer15C})
    Compras_Semanales.append({'ahoraCC': ahoraCC, 'ayer8CC': ayer8CC, 'ayer1CC': ayer1CC, 'ayer9CC': ayer9CC, 'ayer2CC': ayer2CC, 'ayer10CC': ayer10CC,'ayer3CC': ayer3CC, 'ayer11CC': ayer11CC,'ayer4CC': ayer4CC, 'ayer12CC': ayer12CC,'ayer5CC': ayer5CC, 'ayer13CC': ayer13CC,'ayer6CC': ayer6CC, 'ayer14CC': ayer14CC,'ayer7CC': ayer7CC, 'ayer15CC': ayer15CC})
    


    #print(repor)
    #print(Ventas_Semanales)
    #Graficos


    ctx = {'CLIENTES_TOTAL': cliente_t, 'CLIENTE_VENTA': total_dinero, 'PROVEEDOR_TOTAL':proveedor,'PROVEEDOR_COMPRA':total_dinero_compras,'CLIENTES_COBROS': len(datos), 'CLIENTES_COBROS_TOTAL':cuenta_cobrar_total, 'COMPRAS_CONTEO': conteo, 'COMPRAS_C_FINAL': total_compras_final,'VENTAS_SEMANALES':Ventas_Semanales,'COMPRAS_SEMANALES':Compras_Semanales }
    return render(request, 'base/index.html' , ctx)


from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/store')
    else:
        form = SignUpForm()
    return render(request, 'base/signup.html', {'form': form})



#@permission_required("Presentacion.view")
@login_required(login_url='/login/')
@method_decorator(csrf_exempt)
def List(request, Model):
    if Model == "Presentacion": #Verificamos el modelo que nos lllega
        data = Presentacion.objects.all() #Realizamos la consulta
        template = "base/list.html" #Template al que enviaremos la informacion, de ser necesario la modificacion se envia a otro template
        tablename = "Presentacion" #Nombre de la tabla
        th = [{'name':'id'},{'name':'Nombre'},{'name':'Descripcion'},{'name':'Action'}] #Encabezados de la tabla
        ajaxData = [{"data":"id"},{"data":"nombre"},{"data":"descripcion"},{"data":"action"}] #Iteracion de campos a buscar para rellenar la tabla
    if Model == "Categoria":
        data = Categoria.objects.all()
        template = "base/list.html"
        th = [{'name':'id'},{'name':'Name'},{'name':'Description'},{'name':'Action'}]
        ajaxData = [{"data":"id"},{"data":"nombre"},{"data":"descripcion"},{"data":"action"}]
        tablename = "Categoria"
    if Model == "Color":
        data = Color.objects.all()
        template = "base/list.html"
        th = [{'name':'id'},{'name':'Name'},{'name':'Description'},{'name':'Action'}]
        ajaxData = [{"data":"id"},{"data":"nombre"},{"data":"descripcion"},{"data":"action"}]
        tablename = "Color"
    if Model == "Talla":
        data = Talla.objects.all()
        template = "base/list.html"
        th = [{'name':'id'},{'name':'Name'},{'name':'Description'},{'name':'Action'}]
        ajaxData = [{"data":"id"},{"data":"nombre"},{"data":"descripcion"},{"data":"action"}]
        tablename = "Talla"
    if Model == "SubCategoria":
        data = SubCategoria.objects.all()
        template = "base/list.html"
        th = [{'name':'id'},{'name':'Name'},{'name':'Description'},{'name':'Action'}]
        ajaxData = [{"data":"id"},{"data":"nombre"},{"data":"descripcion"},{"data":"action"}]
        tablename = "Sub Categoria"
    if Model == "Componente":
        data = Componente.objects.all()
        template = "base/list.html"
        th = [{'name':'id'},{'name':'Nombre'},{'name':'Presentacion'},{'name':'Categoria'},{'name':'Serie'},{'name':'Compra'},{'name':'Venta'},{'name':'ISV'},{'name':'Stock Inicial'},{'name':'Stock Actual'},{'name':'Accion'}]
        ajaxData = [{"data":"id"},{"data":"nombre"},{"data":"presentacion"},{"data":"categoria"},{"data":"serie"},{"data":"pre_compra"},{"data":"pre_venta"},{"data":"isv"},{"data":"stock_inicial"},{"data":"stock_actual"},{"data":"accion"}]
        tablename = "Componente"
    if Model == "Cliente":
        data = Cliente.objects.all()
        template = "base/list.html"
        th = [{'name':'id'},{'name':'Identidad'},{'name':'Nombre'},{'name':'Apellido'},{'name':'Telefono'},{'name':'Email'},{'name':'Direccion'},{'name':'Accion'}]
        ajaxData = [{"data":"id"},{"data":"identidad"},{"data":"nombre"},{"data":"apellidos"},{"data":"telefono"},{"data":"email"},{"data":"direccion"},{"data":"accion"}]
        tablename = "Cliente"
    if Model == "Proveedores":
        data = Proveedores.objects.all()
        template = "base/list.html"
        th = [{'name':'id'},{'name':'Empresa'},{'name':'Nombre'},{'name':'Apellido'},{'name':'direccion'},{'name':'Telefono'},{'name':'Phone'},{'name':'Email'},{'name':'Accion'}]
        ajaxData = [{"data":"id"},{"data":"empresa"},{"data":"nombre"},{"data":"apellidos"},{"data":"direccion"},{"data":"telefono"},{"data":"phone"},{"data":"email"},{"data":"accion"}]
        tablename = "Proveedores"
    if Model == "Compras":
        data = Compras.objects.all()
        template = "base/list.html"
        th = [{'name':'id'},{'name':'Codigo'},{'name':'Fecha'},{'name':'Proveedor'},{'name':'N# Factura'},{'name':'Tipo Pago'},{'name':'Isv Total'},{'name':'SubTotal'},{'name':'Total'},{'name':'Accion'}]
        ajaxData = [{"data":"id"},{"data":"codigo"},{"data":"date_create"},{"data":"proveedor"},{"data":"factura"},{"data":"pago"},{"data":"isv"},{"data":"subtotal"},{"data":"total"},{"data":"accion"}]
        tablename = "Compras"
    if Model == "Ventas":
        data = Ventas.objects.all()
        template = "base/list.html"
        th = [{'name':'id'},{'name':'Codigo'},{'name':'Fecha'},{'name':'Cliente'},{'name':'Pago'},{'name':'Isv'},{'name':'Sub Total'},{'name':'Total'},{'name':'Accion'}]
        ajaxData = [{"data":"id"},{"data":"codigo"},{"data":"date_create"},{"data":"cliente"},{"data":"pago"},{"data":"isv"},{"data":"subtotal"},{"data":"total"},{"data":"accion"}]
        tablename = "Ventas"
    
    
    
    if request.POST:
        #print("data post table")
        datas = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                datas = []
                for i in data:
                    datas.append(i.toJSON())
                    #print(i.toJSON())
            else:
                datas['error'] = 'Ha ocurrido un error'
        except Exception as e:
            datas['error'] = str(e)
        #print(data)
        return JsonResponse(datas, safe=False)



    ctx = {'object_list' : data, 'TABLENAME':tablename ,'TH':th, 'AJAXD':ajaxData,'Add':Model }
    
    
    #print(template)
    return render(request, template , ctx)

@login_required(login_url='/login/')
@method_decorator(csrf_exempt)
def Create(request, Model):
    if Model == "Presentacion": #Modelo en que se trabaja
        tablename = "Presentacion" #Nombre de la tabla
        form = PresentacionForm() #Formulario creado para esta tabla
    if Model == "Color": 
        tablename = "Color" 
        form = ColorForm()
    if Model == "Talla": 
        tablename = "Talla" 
        form = TallaForm()
    if Model == "SubCategoria": 
        tablename = "Sub Categoria" 
        form = SubCategoriaForm()
    if Model == "Categoria":
        tablename = "Categoria"
        form = CategoriaForm()
    if Model == "Componente":
        tablename = "Componente"
        form = ComponenteForm()
    if Model == "Cliente":
        tablename = "Cliente"
        form = ClienteForm()
    if Model == "Proveedores":
        tablename = "Proveedores"
        form = ProveedoresForm()
    if Model == "Compras":
        tablename = "Compras"
        form = ComprasForm()
    if Model == "Ventas":
        tablename = "Ventas"
        #form = VentasForm()
        form = VentasForm()
        #edit = Ventas()
        form = form.save(commit=False)
        form.owner = request.user
        form.isv = 0
        form.total = 0
        form.subtotal = 0
        form.comentario = "ORDEN DE VENTA"
        form.save()
        last_id = Ventas.objects.all().order_by('id').last()
        return HttpResponseRedirect('/base/'+ str(Model) +'/'+ str(last_id.id) +'/update/')
    


    if request.POST:
        if Model == "Presentacion":
            form = PresentacionForm(request.POST,request.FILES)
        if Model == "Talla":
            form = TallaForm(request.POST,request.FILES)
        if Model == "Color":
            form = ColorForm(request.POST,request.FILES)
        if Model == "SubCategoria":
            form = SubCategoriaForm(request.POST,request.FILES)
        if Model == "Categoria":
            form = CategoriaForm(request.POST,request.FILES)
        if Model == "Componente":
            form = ComponenteForm(request.POST,request.FILES)
        if Model == "Cliente":
            form = ClienteForm(request.POST,request.FILES)
        if Model == "Proveedores":
            form = ProveedoresForm(request.POST,request.FILES)
        if Model == "Compras":
            form = ComprasForm(request.POST,request.FILES)
            edit = Compras()
        if Model == "Ventas":
            form = VentasForm(request.POST,request.FILES)
            edit = Ventas()
        
        print(form)
        form = form.save(commit=False)
        form.owner = request.user
        form.save()

        if Model == "Compras":
            last_id = Compras.objects.all().order_by('id').last()
            return HttpResponseRedirect('/base/'+ str(Model) +'/'+ str(last_id.id) +'/update/')
        elif Model == "Ventas":
            last_id = Ventas.objects.all().order_by('id').last()
            return HttpResponseRedirect('/base/'+ str(Model) +'/'+ str(last_id.id) +'/update/')
        else:
            return HttpResponseRedirect('/base/'+ str(Model) +'/list')
            #return reverse_lazy('rrhh:list' ,args=Model)


    if Model == "Compras":
        ctx = {'form':form , 'tablename': tablename , 'lists' : Model }
        return render(request, 'base/create_compra.html' , ctx)
    if Model == "Ventas":
        ctx = {'form':form , 'tablename': tablename , 'lists' : Model }
        return render(request, 'base/create_venta.html' , ctx)
    else:
        ctx = {'form':form , 'tablename': tablename , 'lists' : Model }
        return render(request, 'base/create.html' , ctx)

@login_required(login_url='/login/')
@method_decorator(csrf_exempt)
def Update(request, Model, id):
    relacion = ""
    totalcRentabilidad = 0
    taltavRentabilidad = 0
    totalcProveedor = 0 
    totalvCliente = 0
    if Model == "Presentacion":
        p = Presentacion.objects.get(pk=id)
        form = PresentacionForm(instance=p)
        tablename = "Presentacion"
        relacion = Componente.objects.filter(presentacion=p)
    if Model == "Color":
        p = Color.objects.get(pk=id)
        form = ColorForm(instance=p)
        tablename = "Color"
        relacion = Componente.objects.filter(color=p)
    if Model == "Talla":
        p = Talla.objects.get(pk=id)
        form = TallaForm(instance=p)
        tablename = "Talla"
        relacion = Componente.objects.filter(talla=p)
    if Model == "SubCategoria":
        p = SubCategoria.objects.get(pk=id)
        form = SubCategoriaForm(instance=p)
        tablename = "Sub Categoria"
        relacion = Componente.objects.filter(subcategoria=p)
    if Model == "Categoria":
        p = Categoria.objects.get(pk=id)
        form = CategoriaForm(instance=p)
        tablename = "Categoria"
        relacion = Componente.objects.filter(categoria=p)
    if Model == "Componente":
        p = Componente.objects.get(pk=id)
        form = ComponenteForm(instance=p)
        tablename = "Componente"
        compras = DetalleCompra.objects.filter(componente=p)
        ventas = DetalleVentas.objects.filter(componente=p)
        #retabilidad incial
        #en este apartado se calcula la rentabilidad tanto inicial
        rentabilidad = ((float(p.pre_venta) - float(p.pre_compra))/float(p.pre_venta)) * 100
        for i in compras:
            totalcRentabilidad += i.total
        for e in ventas:
            taltavRentabilidad += i.total
        #Extraemos la rentabilidad global del producto vendido desde 0 al la fecha actual
        if taltavRentabilidad == 0 or totalcRentabilidad == 0:
            retabilidadGlobal = 0
        else:
            retabilidadGlobal = ((float(taltavRentabilidad) - float(totalcRentabilidad))/float(taltavRentabilidad)) * 100

    if Model == "Cliente":
        p = Cliente.objects.get(pk=id)
        form = ClienteForm(instance=p)
        tablename = "Cliente"
        ventas = Ventas.objects.filter(cliente=p)
        for i in ventas:
            if i.total == None or i.total == 0:
                totalvCliente += 0
            else:
                totalvCliente += i.total

    if Model == "Proveedores":
        p = Proveedores.objects.get(pk=id)
        form = ProveedoresForm(instance=p)
        tablename = "Proveedores"
        compras = Compras.objects.filter(proveedor=p)
        for i in compras:
            if i.total == None or i.total == 0:
                totalcProveedor += 0
            else:
                totalcProveedor += i.total
        

    if Model == "Compras":
        p = Compras.objects.get(pk=id)
        form = ComprasForm(instance=p)
        tablename = "Compras"
    if Model == "Ventas":
        p = Ventas.objects.get(pk=id)
        form = VentasForm(instance=p)
        tablename = "Ventas"
    

    
    if request.method == 'POST':
        if Model == "Presentacion":
            form = PresentacionForm(request.POST,request.FILES,instance=p)
        if Model == "SubCategoria":
            form = SubCategoriaForm(request.POST,request.FILES,instance=p)
        if Model == "Talla":
            form = TallaForm(request.POST,request.FILES,instance=p)
        if Model == "Color":
            form = ColorForm(request.POST,request.FILES,instance=p)
        if Model == "Categoria":
            form = CategoriaForm(request.POST,request.FILES,instance=p)
        if Model == "Componente":
            form = ComponenteForm(request.POST,request.FILES,instance=p)
            print("Componentes_update")
        if Model == "Cliente":
            form = ClienteForm(request.POST,request.FILES,instance=p)
        if Model == "Proveedores":
            form = ProveedoresForm(request.POST,request.FILES,instance=p)
        if Model == "Compras":
            form = ComprasForm(request.POST,request.FILES,instance=p)
        if Model == "Ventas":
            form = VentasForm(request.POST,request.FILES,instance=p)
       

    if form.is_valid():
        form = form.save(commit=False)
        

        if Model == "Compras" and p.proceso == 2:
            #si el modelo de compra pasa a finalizar el proceso
            #empieza a calcular los totales
            if p.isv == None or p.total == None or p.subtotal == None:
                isv = 0
                total = 0
                subtotal = 0
            else:
                isv = p.isv
                total = p.total
                subtotal = p.subtotal
                
            
            detalles = DetalleCompra.objects.filter(compra = p.id)
            #print(detalles)
            #Iteracion para calculos y subida de componentes a inventario
            for i in detalles:
                isv += i.isv
                total += i.total
                id_componente = i.componente.id
                componente = Componente.objects.get(pk=i.componente.id)
                #print(componente.nombre)
                componente.stock_inicial = float(componente.stock_inicial) + float(i.cantidad)
                componente.stock_actual = float(componente.stock_actual) + float(i.cantidad)
                componente.save()

            subtotal = total - isv
            #Guardado de campos especiales 
            form.isv = isv
            form.total = total
            form.subtotal = subtotal
            


        
        #form.save_m2m()
        
        form.owner = request.user #Usuario que agrega el objeto
        p.save() # Guardamos el objeto
        #Redireccionado especial
        if Model == "Compras":
            return HttpResponseRedirect('/base/'+ str(Model) +'/'+ str(p.id) +'/update/')
        else:
            return HttpResponseRedirect('/base/'+ str(Model) +'/list/')
    

    if Model == "Compras":
        detalle = DetalleCompra.objects.filter(compra=id)
        ids = id
        ctx = {'form':form , 'tablename': tablename , 'lists' : Model ,'detalle':detalle,'ID':ids ,'P':p}
        return render(request, 'base/create_compra.html' , ctx)
    if Model == "Ventas":
        detalle = DetalleVentas.objects.filter(ventas=id)
        ids = id
        ctx = {'form':form , 'tablename': tablename , 'lists' : Model ,'detalle':detalle,'ID':ids ,'P':p}
        return render(request, 'base/create_venta.html' , ctx)
    if Model== "Componente":
        ctx = {'form':form , 'tablename': tablename , 'lists' : Model ,'RELACION' : relacion, 'VENTAS' : ventas, 'COMPRAS': compras, 'RENTABILIDAD': rentabilidad,'RENTABILIDADGLOBAL': retabilidadGlobal}
        return render(request, 'base/create.html' , ctx)
    if Model=="Proveedores":
        ctx = {'form':form , 'tablename': tablename , 'lists' : Model ,'RELACION' : relacion,  'COMPRAS': compras, 'TOTAL': totalcProveedor}
        return render(request, 'base/create.html' , ctx)
    if Model=="Cliente":
        ctx = {'form':form , 'tablename': tablename , 'lists' : Model ,'RELACION' : relacion, 'VENTAS': ventas, 'TOTAL': totalvCliente}
        return render(request, 'base/create.html' , ctx)
    else:
        ctx = {'form':form , 'tablename': tablename , 'lists' : Model ,'RELACION' : relacion}
        return render(request, 'base/create.html' , ctx)



@login_required(login_url='/login/')
@method_decorator(csrf_exempt)
def Delete(request, Model, id):

    #print("recibiendo " + str(Model)  + "Y el ID :" + str(id))
    if Model == "Presentacion":
        dele = Presentacion.objects.get(pk=id)
    if Model == "SubCategoria":
        dele = SubCategoria.objects.get(pk=id)
    if Model == "Talla":
        dele = Talla.objects.get(pk=id)
    if Model == "Color":
        dele = Color.objects.get(pk=id)
    if Model == "Categoria":
        dele = Categoria.objects.get(pk=id)
    if Model == "Componente":
        dele = Componente.objects.get(pk=id)
    if Model == "Cliente":
        dele = Cliente.objects.get(pk=id)
    if Model == "Proveedores":
        dele = Proveedores.objects.get(pk=id)
    if Model == "Compras":
        dele = Compras.objects.get(pk=id)
    if Model == "Ventas":
        dele = Ventas.objects.get(pk=id)
    if Model == "Carrito_Detalle":
        dele = Detalle_Carrito.objects.get(pk=id)


    

    #dele = Company.objects.get(pk=id)
    try:
        if Model == "Compras":
            print("Enviar correo con informacion que estan eliminando")
        elif Model == "Ventas":
            print("Enviar correo con informacion que estan eliminando")
        else:
            dele.delete()
        
        if Model == "Carrito_Detalle":
            return HttpResponseRedirect('/store/carrito/')
        else:
            return HttpResponseRedirect('/base/'+ str(Model) +'/list')
    except:
        print("Un Erro al eliminar registro")


#Listado de cuentas por cobara
@login_required(login_url='/login/')
def ListCuentasPorCobrar(request):
    cliente = Cliente.objects.all()
    ventas = Ventas.objects.filter(pago=2)
    cuentas = CuentasPorPagar.objects.all()
    datos = []
    total_ventas = 0
    total_abono = 0
    total_resta = 0 
    for i in cliente:
        for c in ventas:
            if i.id == c.cliente.id:
                total_ventas += float(c.total)

        for u in cuentas:
            if i.id == u.cliente.id:
                total_abono += float(u.abono)
                
        if total_ventas > 0 and total_abono < total_ventas:
            total_resta = total_ventas - total_abono
            datos.append({'id':str(i.id),'identidad':str(i.identidad),'nombre':str(i.nombre),'apellidos':str(i.apellidos), 'ventas':str(total_ventas), 'abono':str(total_abono), 'restante':str(total_resta)})

        total_abono = 0
        total_ventas= 0
        total_resta = 0 
                
    #print(datos)            
        
    
    ctx = {'DATOS': datos, 'TABLENAME' : 'Cuentas Por Cobrar'}
    return render(request, 'base/list_cobros.html' , ctx)


@login_required(login_url='/login/')
def abonoCuenta(request,id):
    if request.method == 'POST':
        print("POST")
        #Abonos = request.GET.get('Abonos')
        #print(Abonos)

    elif request.method == 'GET':
        cliente = Cliente.objects.get(pk=id)
        cuentas = CuentasPorPagar.objects.filter(cliente=id)
        ventas = Ventas.objects.filter(pago=2).filter(cliente=id)
        Abonos = ""
        Abonos = request.GET.get('Abonos')
        
        
        
        total_ventas = 0
        total_abono = 0
        total_resta = 0 

        
        for c in ventas:
            if cliente.id == c.cliente.id:
                total_ventas += float(c.total)

        for u in cuentas:
            if cliente.id == u.cliente.id:
                total_abono += float(u.abono)
        
        total_resta = total_ventas - total_abono

        #proceso para agregar abonos y validar datos
        if Abonos == None:
            print("Ingresa un dato")
        else:
            if total_resta > 0:
                print("a guardar informa")
                form = CuentasPorPagar()
                form.owner = request.user
                form.abono = float(Abonos)
                form.cliente = cliente
                form.save()
                resta_total_final = total_resta - float(Abonos)
                #Envio de email para notificar el abono de pago
                detalle = []
                today = date.today()
                from datetime import datetime
                now = datetime.now()
                detalle.append({'fecha':str(today), 'hora':str(now),'abono':float(Abonos),'pendiente':float(resta_total_final)})
                SendEmailT= SendEmailAbonoThread(cliente, detalle )
                SendEmailT.start()
                #Envio finalizado 

                return HttpResponseRedirect('/base/cobros/'+str(id)+'/')



    ctx = {'CLIENTE': cliente , 'PAGOS': cuentas ,'VENTATOTAL': total_ventas, 'TOTALABONO' : total_abono , 'RESTA':total_resta}
    return render(request, 'base/cobros_abono.html', ctx)


#Reportes
@login_required(login_url='/login/')
def Reporte(request):
    ctx={}
    today = date.today()
    print("Hoy es por la gran" + str(today))
    if request.method == 'POST':
        print("POST")
        
    elif request.method == 'GET':
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_final = request.GET.get('fecha_final')
        selec_reporte = request.GET.get('selec_reporte')
        

        #Validar fechas
        if fecha_final == None or fecha_final == "":
            fecha_inicio = today
        if fecha_final == None or fecha_final == "":
            fecha_final = today
        #ctx={'fecha_final':fecha_final, 'fecha_inicio':fecha_inicio}

        #Consultas
        totalc = 0
        totalv = 0
        if selec_reporte == "1. Compras":
            compras = Compras.objects.filter(date_create__range=[fecha_inicio, fecha_final])
            for i in compras:
                if i.total:
                    totalc += float(i.total)
            ctx={'fecha_final':fecha_final, 'fecha_inicio':fecha_inicio, 'compras': compras,'totalc':totalc}

        elif selec_reporte == "2. Ventas":
            ventas = Ventas.objects.filter(date_create__range=[fecha_inicio, fecha_final])
            for i in ventas:
                if i.total:
                    totalv += float(i.total)
            ctx={'fecha_final':fecha_final, 'fecha_inicio':fecha_inicio, 'ventas': ventas,'totalv': totalv}

        elif selec_reporte == "3. Todo":
            compras = Compras.objects.filter(date_create__range=[fecha_inicio, fecha_final])
            for i in compras:
                if i.total:
                    totalc += float(i.total)
            ventas = Ventas.objects.filter(date_create__range=[fecha_inicio, fecha_final])
            for i in ventas:
                if i.total:
                    totalv += float(i.total)
            ctx={'fecha_final':fecha_final, 'fecha_inicio':fecha_inicio, 'compras': compras, 'ventas': ventas,'totalv': totalv,'totalc': totalc}
        else:
            compras = Compras.objects.filter(date_create__range=[str(today), str(today)])
            for i in compras:
                if i.total:
                    totalc += float(i.total)
            ventas = Ventas.objects.filter(date_create__range=[str(today), str(today)])
            for i in ventas:
                if i.total:
                    totalv += float(i.total)
            ctx={'fecha_final':fecha_final, 'fecha_inicio':fecha_inicio, 'compras': compras, 'ventas': ventas,'totalv': totalv,'totalc': totalc}
    
    return render(request, 'base/reporte.html' , ctx)