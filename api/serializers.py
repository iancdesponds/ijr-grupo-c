from rest_framework import serializers
from .models import *

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ('id', 'nome', 'descricao', 'preco', 'quantidade')

class ItemDoCarrinhoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemDoCarrinho
        fields = ('carrinho', 'produto', 'quantidade')

class ItemDoCarrinhoSerializerDTO(serializers.ModelSerializer):
    produto = ProdutoSerializer()
    class Meta:
        model = ItemDoCarrinho
        fields = ('produto', 'quantidade')

    def __init__(self, *args, **kwargs):
        """Aceita dados adicionais no contexto."""
        super(ItemDoCarrinhoSerializerDTO, self).__init__(*args, **kwargs)
        self.produtos_data = self.context.get('produto')

    def to_representation(self, instance):
        """Adiciona dados dos itens do carrinho ao retorno"""
        representation = super(ItemDoCarrinhoSerializerDTO, self).to_representation(instance)
        representation['produto'] =  self.produtos_data
        return representation


class CarrinhoSerializer(serializers.ModelSerializer):
    itensDoCarrinho = ItemDoCarrinhoSerializerDTO(many=True, read_only=True)

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
        
