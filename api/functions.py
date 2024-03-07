from .models import Carrinho, ItemDoCarrinho
from .serializers import CarrinhoSerializer, ItemDoCarrinhoSerializerDTO, ProdutoSerializer

def get_carrinho(request):        
    carrinho = Carrinho.objects.get(usuario=request.user)
    itens_carrinho = ItemDoCarrinho.objects.filter(carrinho=carrinho)

    itens_serializer = []
    for item in itens_carrinho: 
        produto_data = ProdutoSerializer(item.produto, context={"request": request}).data
        itens_serializer.append(ItemDoCarrinhoSerializerDTO(item, context={"produto": produto_data, "request": request}).data)

    serializer = CarrinhoSerializer(carrinho, context={'itensDoCarrinho': itens_serializer, "request": request})
    return serializer.data
