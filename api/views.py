from rest_framework import generics
from django.contrib.auth import authenticate
from .models import Produto, ItemDoCarrinho, Carrinho, User
from .serializers import *
from .permissions import *
from .functions import *

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class ProdutoListCreate(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsGetMethodOrIsAdmin]
    serializer_class = ProdutoSerializer
    queryset = Produto.objects.all().order_by("-estoque")

    def get_serializer_context(self):
        return {'request': self.request}

class ProdutoDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsGetMethodOrIsAdmin]

    serializer_class = ProdutoSerializer
    queryset = Produto.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}
    
class CarrinhoView(APIView):
    queryset = Carrinho.objects.all()
    serializer_class = CarrinhoSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}

    def get(self, request, *args, **kwargs):
        return Response(get_carrinho(request), status=status.HTTP_200_OK)

class RegistroView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Os campos "email" e "password" são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if User.objects.filter(email=email).exists():
                return Response({'error': 'Este email já está em uso.'}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.create_user(email=email, password=password)
            cart = Carrinho.objects.create(usuario=user)
            authenticated_user = authenticate(email=email, password=password)
            if authenticated_user:
                token, created = Token.objects.get_or_create(user=authenticated_user)
                return Response({'token': token.key}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Falha na autenticação'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro durante o registro: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Os campos "email" e "password" são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

class ProdutoNoCarrinhoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id_produto):
        quantidade = request.data.get('quantidade')

        if not quantidade:
            return Response({'error': 'O campo "quantidade" é origatório.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            id_carrinho = request.user.carrinho.id
            carrinho = Carrinho.objects.get(id=id_carrinho)
            produto = Produto.objects.get(id=id_produto)

            if(quantidade > produto.estoque):
                return Response({'error': 'Quantidade insuficiente em estoque'}, status=status.HTTP_400_BAD_REQUEST)

            item = ItemDoCarrinho.objects.filter(carrinho=carrinho, produto=produto)
            if(item.exists()):
                nova_quantidade = item.get().quantidade + quantidade
                if(nova_quantidade > produto.estoque):
                    return Response({'error': 'Quantidade insuficiente em estoque'}, status=status.HTTP_400_BAD_REQUEST)
                elif(nova_quantidade < 0):
                    return Response({'error': 'Quantidade inválida.'}, status=status.HTTP_400_BAD_REQUEST)
                elif(nova_quantidade == 0):
                    item.delete()
                else:
                    item.update(quantidade=nova_quantidade)
            else:
                item = ItemDoCarrinho.objects.create(carrinho=carrinho, produto=produto, quantidade=quantidade)

            carrinho.qtdItens += quantidade
            carrinho.total += produto.preco * quantidade
            carrinho.save()
            return Response(get_carrinho(request), status=status.HTTP_200_OK)
        
        except Carrinho.DoesNotExist:
            return Response({'error': 'Carrinho não encontrado'}, status=status.HTTP_400_BAD_REQUEST)
        except Produto.DoesNotExist:
            return Response({'error': 'Produto não encontrado'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro ao adicionar o item no carrinho: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id_produto, *args, **kwargs):
        try:
            carrinho = Carrinho.objects.get(usuario=request.user)
            produto = Produto.objects.get(id=id_produto)
            nova_quantidade = request.data.get('quantidade')

            item = ItemDoCarrinho.objects.filter(carrinho=carrinho, produto=produto).first()

            if item:
                if(nova_quantidade > produto.estoque):
                    return Response({'error': 'Quantidade insuficiente em estoque'}, status=status.HTTP_400_BAD_REQUEST)
                elif(nova_quantidade < 0):
                    return Response({'error': 'Quantidade inválida.'}, status=status.HTTP_400_BAD_REQUEST)
                elif(nova_quantidade == 0):
                    item.delete()
                else:
                    delta = nova_quantidade - item.quantidade
                    item.quantidade = nova_quantidade
                    item.save()
                    carrinho.qtdItens += delta
                    carrinho.total += produto.preco * delta 
                    carrinho.save()
                return Response(get_carrinho(request), status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Produto não encontrado no carrinho.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro ao atualizar a quantidade do produto no carrinho: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id_produto):
        try:
            id_carrinho = request.user.carrinho.id
            carrinho = Carrinho.objects.get(id=id_carrinho)
            produto = Produto.objects.get(id=id_produto)
            item = ItemDoCarrinho.objects.get(carrinho=carrinho, produto=produto)
            carrinho.qtdItens -= item.quantidade
            carrinho.total -= produto.preco * item.quantidade
            item.delete()
            carrinho.save()
            return Response(get_carrinho(request), status=status.HTTP_200_OK)
        except Carrinho.DoesNotExist:
            return Response({'error': 'Carrinho não encontrado'}, status=status.HTTP_400_BAD_REQUEST)
        except Produto.DoesNotExist:
            return Response({'error': 'Produto não encontrado'}, status=status.HTTP_400_BAD_REQUEST)
        except ItemDoCarrinho.DoesNotExist:
            return Response({'error': 'Item não encontrado'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro ao remover o item do carrinho: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class CheckOut(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        carrinho = Carrinho.objects.get(usuario=user)
        if carrinho.qtdItens == 0:
            return Response({'error': 'Seu carrinho está vazio'})
        try:
            itens_carrinho = ItemDoCarrinho.objects.filter(carrinho=carrinho)
            for item in itens_carrinho:
                if item.quantidade > item.produto.estoque:
                    return Response({'error': f'Quantidade insuficiente em estoque para o produto {item.produto.nome}'}, status=status.HTTP_400_BAD_REQUEST)

            compra = Compra.objects.create(usuario=user, valor=carrinho.total, qtdItens=carrinho.qtdItens)
            for item in itens_carrinho:
                produto = Produto.objects.get(id=item.produto.id)
                produto.estoque -= item.quantidade
                ItemDaCompra.objects.create(compra=compra, produto=produto, quantidade=item.quantidade)
                item.delete()
                produto.save()
            carrinho.qtdItens = 0
            carrinho.total = 0
            carrinho.save()
            return Response({'success': 'Pagamento realizado com sucesso!'})
        except Exception as e:
            return Response({'error': f'Ocorreu um erro ao processar o pagamento: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class CompraView(APIView):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            compras = Compra.objects.filter(usuario=request.user).order_by('-data')
            compra_serializer = []
            for compra in compras:
                itens_compra = ItemDaCompra.objects.filter(compra=compra)
                itens_serializer = []
                for item in itens_compra:
                    produto_data = ProdutoSerializer(item.produto, context={"request": request}).data
                    itens_serializer.append(ItemDaCompraSerializer(item, context={"produto": produto_data, "request": request}).data)
                compra_serializer.append(CompraSerializer(compra, context={'itensDaCompra': itens_serializer, "request": request}).data)
            return Response(compra_serializer, status=status.HTTP_200_OK)
        except Compra.DoesNotExist:
            return Response({'error': 'Nenhuma compra encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro ao buscar as compras: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)