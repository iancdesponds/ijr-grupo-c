# Generated by Django 5.0.2 on 2024-03-04 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_produto_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='produtosImg/'),
        ),
    ]
