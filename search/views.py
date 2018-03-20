from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from haystack.query import SearchQuerySet
from search.models import Category, Product
from search.serializers import solr_products_serialize


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
    def get(self, request):
        q = request.GET.get('q')
        #result = SearchQuerySet().models(Product).filter(content=q)
        result = SearchQuerySet().models(Product).filter(name_auto=q)

        result = solr_products_serialize(result)

        # facets = SearchQuerySet().models(Product).facet('category')
        # print(facets.facet_counts())
        # by where in
        # data = SearchQuerySet().models(Product).filter(category__in=['CPU','Graphic Card'])
        # result = solr_products_serialize(data)

        return Response(result, status.HTTP_200_OK)
