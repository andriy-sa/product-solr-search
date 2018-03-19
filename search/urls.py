from django.urls import path

from search import views

app_name = 'search'
urlpatterns = [
    path('sync_docs/', views.SyncDocumentsAPIView.as_view(), name='sync_docs'),
    path('products/', views.ProductsSearchAPIView.as_view(), name='products'),
]
