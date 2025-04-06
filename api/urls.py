from django.urls import path
from .views import *

urlpatterns = [
    path('', CarListView.as_view(), name='car-list'),
    path('<int:pk>/', CarDetailView.as_view(), name='car-detail'),
    path('create/', CreateCarView.as_view(), name='create-car'),
    path('add_to_favorites/', add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/', remove_from_favorites, name='remove_from_favorites'),
    path('get_favorites/', get_favorites, name='get_favorites'),
    path('user_posts/', user_posts, name='user-posts'),
]
