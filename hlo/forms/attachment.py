import logging

from crispy_forms.helper import FormHelper  # type: ignore[import-untyped]
from crispy_forms.layout import (  # type: ignore[import-untyped]
    Column,
    Field,
    Row,
)
from django.forms import ModelForm, modelformset_factory

from hlo.models import Attachment

logger = logging.getLogger(__name__)


class AttachmentForm(ModelForm):
    class Meta:
        model = Attachment
        exclude = ["comment", "text", "manual_input", "sha1"]  # noqa: DJ006


AttachmentFormSet = modelformset_factory(
    model=Attachment,
    form=AttachmentForm,
    extra=1,
)


class AttachmentFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = "POST"
        self.form_class = "form-vertical"
        self.label_class = "col"
        self.field_class = "col"
        self.render_required_fields = True
        self.form_tag = False
        self.add_layout(
            Column(
                Row(
                    Column(Field("name")),
                    Column(
                        Field("type"),
                    ),
                    Column(Field("file")),
                ),
            ),
        )
