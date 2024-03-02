from rest_framework import serializers
from .models import *

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ('id', 'nome', 'descricao', 'preco', 'quantidade')

class ItemDoCarrinhoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemDoCarrinho
        fields = ('id', 'carrinho', 'produto', 'quantidade')

class CarrinhoSerializer(serializers.ModelSerializer):
    itensDoCarrinho = ItemDoCarrinhoSerializer(many=True, read_only=True)

    class Meta:
        model = Carrinho
        fields = ('id', 'usuario', 'itensDoCarrinho', 'qtdItens', 'total')
    
    def __init__(self, *args, **kwargs):
        """Aceita dados adicionais no contexto."""
        super(CarrinhoSerializer, self).__init__(*args, **kwargs)
        self.itensDoCarrinho_data = self.context.get('itensDoCarrinho')

    def to_representation(self, instance):
        """Adiciona dados dos itens do carrinho ao retorno"""
        representation = super(CarrinhoSerializer, self).to_representation(instance)
        representation['itensDoCarrinho'] = self.itensDoCarrinho_data
        return representation