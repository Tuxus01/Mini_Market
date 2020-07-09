from datetime import datetime
from django.forms import *
from .models import  *

class PresentacionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        #self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Presentacion
        #fields = ['name','description','status']
        fields = '__all__'
        exclude = ['owner']

class TallaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        #self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Talla
        #fields = ['name','description','status']
        fields = '__all__'
        exclude = ['owner']


class SubCategoriaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        #self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = SubCategoria
        #fields = ['name','description','status']
        fields = '__all__'
        exclude = ['owner']



class ColorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        #self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Color
        #fields = ['name','description','status']
        fields = '__all__'
        exclude = ['owner']


class CategoriaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        #self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Categoria
        #fields = ['name','description','status']
        fields = '__all__'
        exclude = ['owner']


class ComponenteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        #self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Componente
        #fields = ['name','description','status']
        fields = '__all__'
        exclude = ['owner','stock_inicial','stock_actual']


class ClienteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        #self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Cliente
        #fields = ['name','description','status']
        fields = '__all__'
        exclude = ['owner']


class ProveedoresForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        #self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Proveedores
        #fields = ['name','description','status']
        fields = '__all__'
        exclude = ['owner']


class ComprasForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'

        self.fields['codigo'].widget.attrs['readonly'] = True
        self.fields['isv'].widget.attrs['readonly'] = True
        self.fields['subtotal'].widget.attrs['readonly'] = True
        self.fields['total'].widget.attrs['readonly'] = True
        self.fields['proveedor'].widget.attrs['class'] = "form-control js-select2 "
        self.fields['pago'].widget.attrs['class'] = "form-control js-select2 "
        self.fields['proceso'].widget.attrs['class'] = "form-control js-select2"
    class Meta:
        model = Compras
        #fields = ['name','description','status']
        fields = '__all__'
        exclude = ['owner']


class VentasForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        #self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Ventas
        #fields = ['name','description','status']
        fields = '__all__'
        exclude = ['owner']
