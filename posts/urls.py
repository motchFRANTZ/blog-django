# posts/urls.py

from django.urls import path
from .views import (
    PostListView, PostDetailView, PostCreateView, 
    PostUpdateView, PostDeleteView 
)

urlpatterns = [
    # 1. Rota de Criação (Mais Específica)
    path('new/', PostCreateView.as_view(), name='post_create'), # <-- VEM PRIMEIRO!
    
    # 2. Rota de Edição/Exclusão (Também deve vir antes da genérica)
    path('<slug:slug>/edit/', PostUpdateView.as_view(), name='post_update'), 
    path('<slug:slug>/delete/', PostDeleteView.as_view(), name='post_delete'),
    
    # 3. Rota de Detalhe (Genérica com slug)
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'), 
    
    # 4. Rota de Lista (Vazio, a mais genérica de todas)
    path('', PostListView.as_view(), name='post_list'), 
]