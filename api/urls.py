from django.urls import path
from . import views

urlpatterns = [
    # Health check
    path('health/', views.health_check, name='health-check'),

    # Example endpoints demonstrating Cerberus metrics
    path('metrics-example/', views.metrics_example, name='metrics-example'),
    path('slow/', views.slow_endpoint, name='slow-endpoint'),
    path('error/', views.error_example, name='error-example'),

    # CRUD endpoints for items
    path('items/', views.item_list, name='item-list'),
    path('items/<int:pk>/', views.item_detail, name='item-detail'),
]
