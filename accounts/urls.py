from django.urls import path

from .views import register, login_view, logout_view, user_profile, update_profile, browse_user_topics

# Create your urls here.


app_name = 'accounts'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/<int:user_id>/', user_profile, name='profile'),
    path('profile/update/<int:user_id>/', update_profile, name='update-profile'),
    path('profile/<int:user_id>/topics/', browse_user_topics, name='user-topics'),
]
