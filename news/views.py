from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, NewsArticle, SavedArticle
from .serializers import CategorySerializer, NewsArticleSerializer, SavedArticleSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

class NewsArticleViewSet(viewsets.ModelViewSet):
    queryset = NewsArticle.objects.all().order_by('-created_at')
    serializer_class = NewsArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category__slug', 'category__name', 'is_featured', 'is_trending']
    search_fields = ['title', 'description', 'source']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=['views'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_articles = self.queryset.filter(is_featured=True)[:3]
        serializer = self.get_serializer(featured_articles, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def trending(self, request):
        trending_articles = self.queryset.filter(is_trending=True)[:5]
        serializer = self.get_serializer(trending_articles, many=True)
        return Response(serializer.data)

class SavedArticleViewSet(viewsets.ModelViewSet):
    serializer_class = SavedArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedArticle.objects.filter(user=self.request.user).order_by('-saved_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.db.models import Sum
from datetime import timedelta
from django.utils import timezone

User = get_user_model()

class AdminStatsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        total_news = NewsArticle.objects.count()
        total_views = NewsArticle.objects.aggregate(Sum('views'))['views__sum'] or 0
        total_users = User.objects.count()
        
        # Example static viewData for charts
        view_data = [
            {"name": "Sat", "views": 400},
            {"name": "Sun", "views": 300},
            {"name": "Mon", "views": 500},
            {"name": "Tue", "views": 450},
            {"name": "Wed", "views": 600},
            {"name": "Thu", "views": 800},
            {"name": "Fri", "views": 900},
        ]
        
        # Category distribution
        category_data = []
        for cat in Category.objects.all():
            count = NewsArticle.objects.filter(category=cat).count()
            category_data.append({"name": cat.name, "count": count})
            
        return Response({
            "stats": [
                {"label": "Total News", "value": total_news},
                {"label": "Total Views", "value": total_views},
                {"label": "Total Users", "value": total_users},
                {"label": "Growth", "value": "+15%"},
            ],
            "viewData": view_data,
            "categoryData": category_data
        })
