from django.db.models.functions import Length
from haystack import indexes

from .models import Attachement


class AttachementIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    id = indexes.IntegerField(model_attr="id")
    name = indexes.CharField(model_attr="name")
    comment = indexes.CharField(model_attr="comment")

    class Meta:
        model = Attachement
        fields = ["ref", "id", "pdf_text"]

    def get_model(self):
        return Attachement

    def index_queryset(self, using=None):  # noqa: ARG002
        """Used when the entire index for model is updated."""
        return (
            self.get_model().objects
            .annotate(text_len=Length("text"))
            .filter(text_len__gte=10)
            )
