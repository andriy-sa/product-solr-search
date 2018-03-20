from django.urls import path

from search import views

app_name = 'search'
urlpatterns = [
    path('sync_docs/', views.SyncDocumentsAPIView.as_view(), name='sync_docs'),
    path('products/', views.ProductsSearchAPIView.as_view(), name='products'),
    path('autocomplete/', views.ProductAutocompleteAPIView.as_view(), name='autocomplete'),
    path('facets/', views.ProductCategoryFacetsAPIView.as_view(), name='facets'),
]
