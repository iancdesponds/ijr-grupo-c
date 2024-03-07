from django.contrib import admin
from .models import *

admin.site.register(Produto)
admin.site.register(Carrinho)
admin.site.register(ItemDoCarrinho)
admin.site.register(User)
admin.site.register(Compra)
admin.site.register(ItemDaCompra)