from django.urls import path
from .views import signup_view
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('accounts/logout-get/', LogoutView.as_view(), name='logout_get'),  # Allows GET logout
]