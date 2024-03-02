from rest_framework import generics
from .models import Produto, ItemDoCarrinho, Carrinho
from .serializers import ProdutoSerializer, ItemDoCarrinhoSerializer, CarrinhoSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class ProdutoList(generics.ListCreateAPIView):
    serializer_class = ProdutoSerializer

    def get_queryset(self):
        queryset = Produto.objects.all()
        prod = self.request.query_params.get('produto', None)
        if prod is not None:
            queryset = queryset.filter(nome__icontains=prod)
        return queryset

class ProdutoDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProdutoSerializer
    queryset = Produto.objects.all()

class CarrinhoViewSet(viewsets.ModelViewSet):
    queryset = Carrinho.objects.all()
    serializer_class = CarrinhoSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        carrinho = Carrinho.objects.get(usuario=request.user)
        itens_carrinho = ItemDoCarrinho.objects.filter(carrinho=carrinho)
        itensSerializer = ItemDoCarrinhoSerializer(itens_carrinho, many=True)
        serializer = CarrinhoSerializer(carrinho, context={'itensDoCarrinho': itensSerializer.data})
        return Response(serializer.data)

class RegistroView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Os campos "username" e "password" são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if User.objects.filter(username=username).exists():
                return Response({'error': 'Este nome de usuário já está em uso.'}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.create_user(username=username, password=password)
            cart = Carrinho.objects.create(usuario=user)
            authenticated_user = authenticate(username=username, password=password)
            if authenticated_user:
                token, created = Token.objects.get_or_create(user=authenticated_user)
                return Response({'token': token.key}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Falha na autenticação'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro durante o registro: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Os campos "username" e "password" são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

class AdicionarItemNoCarrinho(APIView):
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

            if(quantidade > produto.quantidade):
                return Response({'error': 'Quantidade insuficiente em estoque'}, status=status.HTTP_400_BAD_REQUEST)

            item = ItemDoCarrinho.objects.filter(carrinho=carrinho, produto=produto)
            if(item.exists()):
                nova_quantidade = item.get().quantidade + quantidade
                if(nova_quantidade > produto.quantidade):
                    return Response({'error': 'Quantidade insuficiente em estoque'}, status=status.HTTP_400_BAD_REQUEST)
                item.update(quantidade=nova_quantidade)
                return Response({'id': item.get().id}, status=status.HTTP_200_OK)
            else:
                item = ItemDoCarrinho.objects.create(carrinho=carrinho, produto=produto, quantidade=quantidade)
                return Response({'id': item.id}, status=status.HTTP_201_CREATED)
        
        except Carrinho.DoesNotExist:
            return Response({'error': 'Carrinho não encontrado'}, status=status.HTTP_400_BAD_REQUEST)
        except Produto.DoesNotExist:
            return Response({'error': 'Produto não encontrado'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro ao adicionar o item no carrinho: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # def delete(self, request, id_produto):