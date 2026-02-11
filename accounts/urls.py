from django.urls import path

from .views import register, login_view, logout_view, user_profile, update_profile

# Create your urls here.


app_name = 'accounts'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/<int:user_id>/', user_profile, name='profile'),
    path('profile/update/<int:user_id>/', update_profile, name='update-profile'),
]
