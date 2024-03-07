from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('produtos/', ProdutoListCreate.as_view(), name='produto-list-create'),
    path('produtos/<int:pk>/', ProdutoDetail.as_view(), name='produto-update-delete'),
    path('registro/', RegistroView.as_view(), name='registro'),
    path('login/', LoginView.as_view(), name='registro'),
    path('produtos/<int:id_produto>/carrinho/', ProdutoNoCarrinhoView.as_view(), name='adicionar-item'),
    path('checkout/', CheckOut.as_view(), name='pagamento'),
    path('carrinho/', CarrinhoView.as_view(), name='compras'),
    path('compras/', CompraView.as_view(), name='compras'),
    path('', include(router.urls)),

]   