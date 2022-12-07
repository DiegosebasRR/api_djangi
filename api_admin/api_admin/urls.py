
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from api.views import Login
  
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(('api.urls','api'))),
    path('api_generate_token/', views.obtain_auth_token),
    path('login/',Login.as_view(), name = 'login'),
]