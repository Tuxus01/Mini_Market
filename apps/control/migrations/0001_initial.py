# Generated by Django 3.0.5 on 2020-05-07 17:23

import apps.control.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('date_create', models.DateField(auto_now_add=True, verbose_name='Date of Create')),
                ('date_change', models.DateField(auto_now=True, verbose_name='Date of Change')),
                ('date_delete', models.DateField(auto_now=True, verbose_name='Date of Delete')),
                ('date_time_c', models.TimeField(auto_now_add=True)),
                ('date_time_m', models.TimeField(auto_now=True)),
                ('nombre', models.CharField(max_length=80, unique=True, verbose_name='Categoria ')),
                ('descripcion', models.TextField(blank=True, max_length=600, null=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('date_create', models.DateField(auto_now_add=True, verbose_name='Date of Create')),
                ('date_change', models.DateField(auto_now=True, verbose_name='Date of Change')),
                ('date_delete', models.DateField(auto_now=True, verbose_name='Date of Delete')),
                ('date_time_c', models.TimeField(auto_now_add=True)),
                ('date_time_m', models.TimeField(auto_now=True)),
                ('identidad', models.CharField(max_length=15, unique=True, verbose_name='Identidad')),
                ('nombre', models.CharField(max_length=150, verbose_name='Nombres ')),
                ('apellidos', models.CharField(blank=True, max_length=150, null=True, verbose_name='Apellidos')),
                ('telefono', models.CharField(blank=True, max_length=10, null=True, verbose_name='Telefono')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('direccion', models.TextField(blank=True, max_length=300, null=True, verbose_name='Direccion ')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Componente',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('date_create', models.DateField(auto_now_add=True, verbose_name='Date of Create')),
                ('date_change', models.DateField(auto_now=True, verbose_name='Date of Change')),
                ('date_delete', models.DateField(auto_now=True, verbose_name='Date of Delete')),
                ('date_time_c', models.TimeField(auto_now_add=True)),
                ('date_time_m', models.TimeField(auto_now=True)),
                ('nombre', models.CharField(max_length=100, unique=True, verbose_name='Nombre Producto ')),
                ('serie', models.CharField(max_length=300, unique=True)),
                ('pre_compra', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Precio Compra')),
                ('pre_venta', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Precion Venta')),
                ('isv', models.IntegerField(choices=[(1, '0%'), (2, '15%'), (3, '18%')], default=2)),
                ('stock_inicial', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Stock Inicial')),
                ('stock_actual', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Stock Actual')),
                ('descripcion', models.TextField(blank=True, max_length=600, null=True)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to=apps.control.models.Componente_file)),
                ('categoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='control.Categoria')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Compras',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('date_create', models.DateField(auto_now_add=True, verbose_name='Date of Create')),
                ('date_change', models.DateField(auto_now=True, verbose_name='Date of Change')),
                ('date_delete', models.DateField(auto_now=True, verbose_name='Date of Delete')),
                ('date_time_c', models.TimeField(auto_now_add=True)),
                ('date_time_m', models.TimeField(auto_now=True)),
                ('codigo', models.CharField(default=apps.control.models.code_compras, max_length=60, unique=True, verbose_name='Codigo')),
                ('factura', models.CharField(blank=True, max_length=150, null=True, verbose_name='Numero Factura')),
                ('pago', models.IntegerField(choices=[(1, 'Efectivo'), (2, 'Credito'), (3, 'Tarjeta')], default=1)),
                ('isv', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='ISV')),
                ('comentarios', models.TextField(blank=True, max_length=1800, null=True, verbose_name='Comentarios')),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Sub Total')),
                ('total', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Ventas',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('date_create', models.DateField(auto_now_add=True, verbose_name='Date of Create')),
                ('date_change', models.DateField(auto_now=True, verbose_name='Date of Change')),
                ('date_delete', models.DateField(auto_now=True, verbose_name='Date of Delete')),
                ('date_time_c', models.TimeField(auto_now_add=True)),
                ('date_time_m', models.TimeField(auto_now=True)),
                ('codigo', models.CharField(default=apps.control.models.code_ventas, max_length=60, unique=True, verbose_name='Codigo')),
                ('pago', models.IntegerField(choices=[(1, 'Efectivo'), (2, 'Credito'), (3, 'Tarjeta')], default=1)),
                ('isv', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='ISV')),
                ('comentarios', models.TextField(blank=True, max_length=1800, null=True, verbose_name='Comentarios')),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Sub Total')),
                ('total', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total')),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='control.Cliente')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Proveedores',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('date_create', models.DateField(auto_now_add=True, verbose_name='Date of Create')),
                ('date_change', models.DateField(auto_now=True, verbose_name='Date of Change')),
                ('date_delete', models.DateField(auto_now=True, verbose_name='Date of Delete')),
                ('date_time_c', models.TimeField(auto_now_add=True)),
                ('date_time_m', models.TimeField(auto_now=True)),
                ('rtn', models.CharField(max_length=15, unique=True, verbose_name='RTN')),
                ('empresa', models.CharField(blank=True, max_length=150, null=True, verbose_name='Empresa ')),
                ('nombre', models.CharField(max_length=150, verbose_name='Nombres ')),
                ('apellidos', models.CharField(blank=True, max_length=150, null=True, verbose_name='Apellidos')),
                ('direccion', models.TextField(blank=True, max_length=300, null=True, verbose_name='Direccion ')),
                ('telefono', models.CharField(blank=True, max_length=10, null=True, verbose_name='Telefono')),
                ('phone', models.CharField(blank=True, max_length=10, null=True, verbose_name='Telefono')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Presentacion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('date_create', models.DateField(auto_now_add=True, verbose_name='Date of Create')),
                ('date_change', models.DateField(auto_now=True, verbose_name='Date of Change')),
                ('date_delete', models.DateField(auto_now=True, verbose_name='Date of Delete')),
                ('date_time_c', models.TimeField(auto_now_add=True)),
                ('date_time_m', models.TimeField(auto_now=True)),
                ('nombre', models.CharField(max_length=80, unique=True, verbose_name='Presentacion ')),
                ('descripcion', models.TextField(blank=True, max_length=600, null=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DetalleVentas',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('date_create', models.DateField(auto_now_add=True, verbose_name='Date of Create')),
                ('date_change', models.DateField(auto_now=True, verbose_name='Date of Change')),
                ('date_delete', models.DateField(auto_now=True, verbose_name='Date of Delete')),
                ('date_time_c', models.TimeField(auto_now_add=True)),
                ('date_time_m', models.TimeField(auto_now=True)),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Cantidad')),
                ('precio_c', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Precio Compra')),
                ('precio_v', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Precio Venta')),
                ('isv', models.IntegerField(default=0, verbose_name='isv')),
                ('total', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Total')),
                ('componente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control.Componente')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('ventas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control.Ventas')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DetalleCompra',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('date_create', models.DateField(auto_now_add=True, verbose_name='Date of Create')),
                ('date_change', models.DateField(auto_now=True, verbose_name='Date of Change')),
                ('date_delete', models.DateField(auto_now=True, verbose_name='Date of Delete')),
                ('date_time_c', models.TimeField(auto_now_add=True)),
                ('date_time_m', models.TimeField(auto_now=True)),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Cantidad')),
                ('precio_c', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Precio Compra')),
                ('precio_v', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Precio Venta')),
                ('isv', models.IntegerField(default=0, verbose_name='isv')),
                ('total', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Total')),
                ('componente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control.Componente')),
                ('compra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control.Compras')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='compras',
            name='proveedor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='control.Proveedores'),
        ),
        migrations.AddField(
            model_name='componente',
            name='presentacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='control.Presentacion'),
        ),
    ]
