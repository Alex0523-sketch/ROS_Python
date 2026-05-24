from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_agregar_codigo_pedido'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidomodel',
            name='email_cliente',
            field=models.EmailField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='pagomodel',
            name='email_cliente',
            field=models.EmailField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='pagomodel',
            name='motivo_rechazo',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
