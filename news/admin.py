from django.contrib import admin
from .models import Category, NewsArticle, SavedArticle

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')

@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'is_trending', 'views', 'created_at')
    list_filter = ('category', 'is_featured', 'is_trending')
    search_fields = ('title', 'source')

admin.site.register(SavedArticle)
