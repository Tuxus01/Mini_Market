# Generated by Django 3.0.5 on 2020-05-11 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0006_auto_20200511_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallecompra',
            name='cantidad',
            field=models.DecimalField(decimal_places=10, max_digits=40, verbose_name='Cantidad'),
        ),
        migrations.AlterField(
            model_name='detallecompra',
            name='isv',
            field=models.DecimalField(decimal_places=10, max_digits=40, verbose_name='Isv'),
        ),
        migrations.AlterField(
            model_name='detallecompra',
            name='precio_c',
            field=models.DecimalField(decimal_places=10, max_digits=40, verbose_name='Precio Compra'),
        ),
        migrations.AlterField(
            model_name='detallecompra',
            name='precio_v',
            field=models.DecimalField(decimal_places=10, max_digits=40, verbose_name='Precio Venta'),
        ),
        migrations.AlterField(
            model_name='detallecompra',
            name='total',
            field=models.DecimalField(decimal_places=10, max_digits=40, verbose_name='Total'),
        ),
    ]
