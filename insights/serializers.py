from rest_framework import serializers
from .models import Category, Article


#Category
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['id', 'created_at']


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = ['name']

    def validate_name(self, value):
        if Category.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("A category with this name already exists.")
        return value


#Article
class ArticleSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model  = Article
        fields = [
            'id', 'title', 'category', 'category_name',
            'body', 'banner_image', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'category_name', 'created_at', 'updated_at']


class ArticleCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Article
        fields = [
            'title', 'category', 'body',
            'banner_image', 'status'
        ]

    def validate_category(self, value):
        if not Category.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Selected category does not exist.")
        return value