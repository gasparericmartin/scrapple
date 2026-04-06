from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('searches-ui/', views.SearchesView.as_view(), name='searches'),
    path('searches-ui/<int:id>/delete/', views.SearchDeleteView.as_view(), name='search_delete'),
]