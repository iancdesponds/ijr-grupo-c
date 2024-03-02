# Generated by Django 5.0.2 on 2024-03-02 12:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrinho',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ItemDoCarrinho',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantidade', models.IntegerField()),
                ('carrinho', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.carrinho')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.produto')),
            ],
        ),
    ]