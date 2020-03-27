from django.urls import path
from .views import (
    PostCreatView,
    PostCategoryView,
    add_to_like,
    remove_from_like
)

app_name = 'posts'

urlpatterns = [
    path('post-create/', PostCreatView.as_view(), name='post_create'),
    path('post/<int:pk>/category/', PostCategoryView.as_view(), name='post_category'),
    path('<int:pk>/add-to-like/', add_to_like, name='add_to_like'),
    path('<int:pk>/remove-from-like/', remove_from_like, name='remove_from_like')
]
