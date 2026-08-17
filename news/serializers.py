from rest_framework import serializers
from .models import Category, NewsArticle, SavedArticle

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class NewsArticleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    
    class Meta:
        model = NewsArticle
        fields = '__all__'

class SavedArticleSerializer(serializers.ModelSerializer):
    article = NewsArticleSerializer(read_only=True)
    article_id = serializers.PrimaryKeyRelatedField(
        queryset=NewsArticle.objects.all(), source='article', write_only=True
    )

    class Meta:
        model = SavedArticle
        fields = ('id', 'article', 'article_id', 'saved_at')
