from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from haystack.query import SearchQuerySet
from search.models import Category, Product
from search.serializers import ProductSearchRequestSerializer, solr_products_serialize


class SyncDocumentsAPIView(APIView):
    def post(self, request):
        Product.objects.all().delete()
        Category.objects.all().delete()

        category = Category(name='CPU')
        category.save()
        category2 = Category(name='Graphic Card')
        category2.save()
        Product(name="Intel Core i5", price=5500, category=category, description="First CPU test description").save()
        Product(name="Intel Core i7-8700K", price=9800, category=category,
                description="Second CPU another description").save()
        Product(name="GeForce GTX 1080", price=35000, category=category2,
                description="Description for gtx video card").save()

        return Response({'success': True}, status.HTTP_200_OK)


class ProductsSearchAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ProductSearchRequestSerializer

    def get(self, request):
        serializer = self.serializer_class(data=request.GET)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        q = serializer.data.get('q')
        categories = serializer.data.get('categories').split(',') if serializer.data.get('categories') else None
        result = SearchQuerySet().models(Product)

        if q:
            result = result.filter(content=q)
        if categories:
            result = result.filter(category_str__in=categories)

        result = solr_products_serialize(result)

        return Response(result, status.HTTP_200_OK)


class ProductAutocompleteAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = None

    def get(self, request):
        q = request.GET.get('q')
        if not q:
            return Response([], status.HTTP_200_OK)

        result = SearchQuerySet().models(Product).filter(name_auto=q)
        result = solr_products_serialize(result)

        return Response(result, status.HTTP_200_OK)


class ProductCategoryFacetsAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = None

    def get(self, request):
        facets = SearchQuerySet().models(Product).facet('category_str').facet_counts()

        return Response(facets, status.HTTP_200_OK)
