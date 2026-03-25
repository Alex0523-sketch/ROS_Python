from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        # Campos requeridos por AbstractBaseUser
        migrations.AddField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        # Campos requeridos por PermissionsMixin
        migrations.AddField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(
                blank=True,
                related_name='custom_user_set',
                related_query_name='custom_user',
                to='auth.group',
                verbose_name='groups',
            ),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(
                blank=True,
                related_name='custom_user_set',
                related_query_name='custom_user',
                to='auth.permission',
                verbose_name='user permissions',
            ),
        ),
        # Eliminar el campo password del modelo original (AbstractBaseUser lo maneja)
        migrations.RemoveField(
            model_name='user',
            name='password',
        ),
        # Re-agregar password con el formato de AbstractBaseUser (max_length=128)
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]
