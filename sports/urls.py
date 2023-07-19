from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'sports'

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<str:sport_name>/', views.detail, name='detail'),
    path('upload/', views.Upload.as_view(), name='upload'),
    path('get_checkbox/', views.get_checkbox, name='get_checkbox'),

]
