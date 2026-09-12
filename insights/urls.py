from django.urls import path
from .views import (
    CategoryListCreateView, CategoryDeleteView,
    ArticleListCreateView, ArticleDetailView
)

urlpatterns = [
    # Categories
    path('categories/',        CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDeleteView.as_view(),  name='category-delete'),

    # Articles
    path('articles/',            ArticleListCreateView.as_view(), name='article-list-create'),
    path('articles/<int:pk>/',   ArticleDetailView.as_view(),     name='article-detail'),
]