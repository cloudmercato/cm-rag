from django.urls import path
from ui import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('query', views.QueryView.as_view(), name="query"),
]
