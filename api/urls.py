from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarrinhoViewSet, ProdutoList, ProdutoDetail

router = DefaultRouter()
router.register(r'carrinho', CarrinhoViewSet)

urlpatterns = [
    path('produtos/', ProdutoList.as_view(), name='produto-create'),
    path('produtos/<int:pk>/', ProdutoDetail.as_view(), name='produto-update-delete'),
    path('registro/', RegistroView.as_view(), name='registro'),
    path('login/', LoginView.as_view(), name='registro'),
    path('produtos/<int:id_produto>/adicionar/', AdicionarItemNoCarrinho.as_view(), name='adicionar-item'),
    path('', include(router.urls)),

]   