from django.urls import path
from users.infrastructure.views.auth_views import login_view, logout_view
from users.infrastructure.views.public_views import index_view

urlpatterns = [
    path('', index_view, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
