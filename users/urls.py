from django.urls import path
from django.contrib.auth.views import LogoutView

from users.views import (
    SignInView,
    SignUpView,
    EditProfileView,
    ProfileDetailView,
    ProfileListView,
    ProfileWiseLikedPostView
)

app_name = 'users'

urlpatterns = [
    path('signin/', SignInView.as_view(), name='signin'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(template_name='home.html'), name='logout'),
    path('edit-profile/', EditProfileView.as_view(), name='edit-profile'),
    path('profile/<int:pk>/detail/', ProfileDetailView.as_view(), name='profile'),
    path('curators/', ProfileListView.as_view(), name='curators'),
    path('liked-post/', ProfileWiseLikedPostView.as_view(), name='liked_post'),
]
