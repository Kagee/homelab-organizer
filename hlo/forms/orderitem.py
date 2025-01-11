import logging

from crispy_forms.helper import FormHelper  # type: ignore[import-untyped]
from django.forms import ModelForm

from hlo.models import OrderItem

logger = logging.getLogger(__name__)


class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        exclude = ["manual_input", "sha1_id"]  # noqa: DJ006

    def __init__(self, *args, **kwargs):
        # We need this so self.fields is populated
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-2"
        self.helper.field_class = "col-10"
