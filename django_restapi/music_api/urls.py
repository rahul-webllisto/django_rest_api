from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [    
    path('list/', views.ListSongsView.as_view(), name='song_list'),
    path('detail/<int:pk>', views.song_detail, name='song_detail'),
    path('api-token-auth/', obtain_jwt_token, name='create-token'),
    path('register/', views.RegisterUserView.as_view(), name="auth-register"),
    path('login/', views.LoginView.as_view(), name="login")
]
