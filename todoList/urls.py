from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.utils.translation import gettext_lazy as _
from .views import TodoViewSet

# Create a router for TodoViewSet with descriptive base name
router = DefaultRouter()
router.register(
    r'todos',  # URL prefix
    TodoViewSet,  # ViewSet class
    basename='todo'  # Base name for URL reversing
)

# Root API documentation
API_TITLE = _('Todo Management API')
API_DESCRIPTION = _('A REST API for managing todo tasks')

# Use the auto-generated URL patterns from the router
urlpatterns = [
    # Include all routes generated by the router
    *router.urls,
    
    # Additional custom URLs can be added here if needed
    # path('custom-endpoint/', custom_view, name='custom-endpoint'),
]