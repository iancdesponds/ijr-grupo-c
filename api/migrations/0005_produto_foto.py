# Generated by Django 5.0.2 on 2024-03-04 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_rename_quantidade_produto_estoque'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='produtos/'),
        ),
    ]
