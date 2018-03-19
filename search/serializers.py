from rest_framework.serializers import ModelSerializer


class ProductSerializer(ModelSerializer):
    pass


def solr_products_serialize(solr_result):
    result = []
    for item in solr_result:
        result.append({
            'pk': item.pk[0],
            'name': item.name_str,
            'price': float(item.price.replace('[', '').replace(']', '')),
            'category': item.category_str,
            'description': item.description_str,
            'created_at': item.created_at_str
        })

    return result
