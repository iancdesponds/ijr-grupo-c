# Generated by Django 5.0.2 on 2024-03-04 20:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_user_is_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('qtdItens', models.IntegerField()),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ItemDaCompra',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantidade', models.IntegerField()),
                ('compra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.compra')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.produto')),
            ],
        ),
    ]