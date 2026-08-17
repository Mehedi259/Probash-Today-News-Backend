from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, NewsArticleViewSet, SavedArticleViewSet, AdminStatsView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'news', NewsArticleViewSet)
router.register(r'saved', SavedArticleViewSet, basename='saved')

urlpatterns = [
    path('admin/stats/', AdminStatsView.as_view(), name='admin_stats'),
    path('', include(router.urls)),
]
