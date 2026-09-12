from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import Category, Article
from .serializers import (
    CategorySerializer, CategoryCreateSerializer,
    ArticleSerializer, ArticleCreateUpdateSerializer
)


#Categories

class CategoryListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Travel Insights'],
        summary='List All Categories',
        description='Returns all blog categories.',
        responses={200: CategorySerializer(many=True)},
    )
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response({
            'status' : 'success',
            'total'  : categories.count(),
            'data'   : serializer.data
        }, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Travel Insights'],
        summary='Create Category',
        description='Add a new blog category.',
        request=CategoryCreateSerializer,
        responses={201: CategorySerializer},
    )
    def post(self, request):
        serializer = CategoryCreateSerializer(data=request.data)
        if serializer.is_valid():
            category = serializer.save()
            return Response({
                'status'  : 'success',
                'message' : 'Category created successfully',
                'data'    : CategorySerializer(category).data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'status'  : 'error',
            'message' : serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class CategoryDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Travel Insights'],
        summary='Delete Category',
        description='Delete a blog category by ID.',
        responses={200: None},
    )
    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            category.delete()
            return Response({
                'status'  : 'success',
                'message' : 'Category deleted successfully'
            }, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({
                'status'  : 'error',
                'message' : 'Category not found'
            }, status=status.HTTP_404_NOT_FOUND)


#Articles

class ArticleListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes     = [MultiPartParser, FormParser]

    @extend_schema(
        tags=['Travel Insights'],
        summary='List All Articles',
        description='Returns a paginated list of all articles. Supports search by title, category, or status.',
        parameters=[
            OpenApiParameter('search', OpenApiTypes.STR, description='Search by title or category'),
            OpenApiParameter('page',   OpenApiTypes.INT, description='Page number',      default=1),
            OpenApiParameter('limit',  OpenApiTypes.INT, description='Results per page', default=10),
        ],
        responses={200: ArticleSerializer(many=True)},
    )
    def get(self, request):
        search = request.query_params.get('search', '')
        page   = int(request.query_params.get('page',  1))
        limit  = int(request.query_params.get('limit', 10))

        articles = Article.objects.select_related('category').all()

        if search:
            articles = articles.filter(
                Q(title__icontains=search)             |
                Q(category__name__icontains=search)    |
                Q(status__icontains=search)
            )

        total      = articles.count()
        start      = (page - 1) * limit
        end        = start + limit
        paginated  = articles[start:end]
        serializer = ArticleSerializer(
            paginated, many=True, context={'request': request}
        )

        return Response({
            'status' : 'success',
            'total'  : total,
            'page'   : page,
            'limit'  : limit,
            'pages'  : (total + limit - 1) // limit,
            'data'   : serializer.data
        }, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Travel Insights'],
        summary='Create Article',
        description='Create a new travel insight article with banner image upload.',
        request=ArticleCreateUpdateSerializer,
        responses={201: ArticleSerializer},
    )
    def post(self, request):
        serializer = ArticleCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            article = serializer.save()
            return Response({
                'status'  : 'success',
                'message' : 'Article created successfully',
                'data'    : ArticleSerializer(
                                article, context={'request': request}
                            ).data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'status'  : 'error',
            'message' : serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes     = [MultiPartParser, FormParser]

    def get_object(self, pk):
        try:
            return Article.objects.select_related('category').get(pk=pk)
        except Article.DoesNotExist:
            return None

    @extend_schema(
        tags=['Travel Insights'],
        summary='Get Single Article',
        description='Returns details of a specific article by ID.',
        responses={200: ArticleSerializer},
    )
    def get(self, request, pk):
        article = self.get_object(pk)
        if not article:
            return Response({
                'status'  : 'error',
                'message' : 'Article not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ArticleSerializer(article, context={'request': request})
        return Response({
            'status' : 'success',
            'data'   : serializer.data
        }, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Travel Insights'],
        summary='Update Article',
        description='Update an existing article by ID.',
        request=ArticleCreateUpdateSerializer,
        responses={200: ArticleSerializer},
    )
    def put(self, request, pk):
        article = self.get_object(pk)
        if not article:
            return Response({
                'status'  : 'error',
                'message' : 'Article not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ArticleCreateUpdateSerializer(
            article, data=request.data, partial=True
        )
        if serializer.is_valid():
            article = serializer.save()
            return Response({
                'status'  : 'success',
                'message' : 'Article updated successfully',
                'data'    : ArticleSerializer(
                                article, context={'request': request}
                            ).data
            }, status=status.HTTP_200_OK)

        return Response({
            'status'  : 'error',
            'message' : serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=['Travel Insights'],
        summary='Delete Article',
        description='Delete an article by ID.',
        responses={200: None},
    )
    def delete(self, request, pk):
        article = self.get_object(pk)
        if not article:
            return Response({
                'status'  : 'error',
                'message' : 'Article not found'
            }, status=status.HTTP_404_NOT_FOUND)

        article.delete()
        return Response({
            'status'  : 'success',
            'message' : 'Article deleted successfully'
        }, status=status.HTTP_200_OK)