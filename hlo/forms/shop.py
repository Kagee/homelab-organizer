from crispy_forms.helper import FormHelper  # type: ignore[import-untyped]
from django.forms import ModelForm

from hlo.models import Shop


class ShopForm(ModelForm):
    class Meta:
        model = Shop
        fields = [
            "name",
            "branch_name",
            "icon",
            "order_url_template",
            "item_url_template",
        ]

    def __init__(self, *args, **kwargs):
        # We need this so self.fields is populated
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-2"
        self.helper.field_class = "col-10"
