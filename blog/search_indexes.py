import datetime
from haystack import indexes
from .models import Post

class PostIndex(indexes.SearchIndex, indexes.Indexable):
	author = indexes.CharField(model_attr='author')
	description = indexes.EdgeNgramField(model_attr="text", null=True)
	text = indexes.EdgeNgramField(document=True, use_template=True, template_name='search/indexes/myapp/post_text.txt')
	title = indexes.EdgeNgramField(model_attr='title')
	published_date = indexes.DateTimeField(model_attr='published_date')

	def get_model(self):
		return Post

	def index_queryset(self, using=None):
		return self.get_model().objects.filter(published_date__lte=datetime.datetime.now())
