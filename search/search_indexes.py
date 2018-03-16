from haystack import indexes
from search.models import Product


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name', boost=1.125)
    price = indexes.DecimalField(model_attr='price')
    category = indexes.CharField(model_attr='category')
    description = indexes.CharField(model_attr='description')
    created_at = indexes.DateTimeField(model_attr='created_at')

    def get_model(self):
        return Product

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
