from django.urls import path
from . import views

urlpatterns = [
    path('searches/', views.SearchList.as_view(), name='search_list'),
    path('searches/<int:id>/', views.SearchDetail.as_view(), name='search_detail'),
    path('searches/<int:id>/posts/', views.PostsBySearch.as_view(), name='posts_by_search'),
    path('scrape/', views.ScrapeView.as_view(), name='scrape'),
]