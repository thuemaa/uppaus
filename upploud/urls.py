from django.urls import path
from . import views
from django.contrib.auth import views as authviews

urlpatterns = [
    path('<int:cur_page>', views.upploudhome, name='upploudhome'),
    path('', views.upploudhome, name='upploudhome'),
    path('login/', authviews.LoginView.as_view(template_name='login.html'), name='userlogin'),
    path('logout/', authviews.LogoutView.as_view(), name='logout'),
    path('signup/', views.usersignup, name='usersignup'),
    path('userimages/', views.userimages, name='userimages'),
    path('upload/', views.upload, name='upload'),
    path('view/<int:img_pk>', views.view, name='view')
]