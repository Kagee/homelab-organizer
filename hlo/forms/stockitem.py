import logging

from crispy_forms.bootstrap import (  # type: ignore[import-untyped]
    FieldWithButtons,
    StrictButton,
)
from crispy_forms.helper import (  # type: ignore[import-untyped]
    FormHelper,
)
from crispy_forms.layout import (  # type: ignore[import-untyped]
    HTML,
    Column,
    Div,
    Field,
    Layout,
    Row,
    Submit,
)
from django import forms
from django.forms import ModelForm
from django_bootstrap_icons.templatetags.bootstrap_icons import (  # type: ignore[import-untyped]
    bs_icon,
)
from django_select2.forms import (  # type: ignore[import-untyped]
    ModelSelect2TagWidget,
)
from taggit.models import Tag  # type: ignore[import-untyped]

from hlo.models import StockItem

logger = logging.getLogger(__name__)


class TagChoices(ModelSelect2TagWidget):
    queryset = Tag.objects.all().order_by("name")
    search_fields = ["name__icontains"]
    empty_label = "foo"  # "Start typing to search or create tags..."

    def get_model_field_values(self, value) -> dict:
        return {"name": value}

    def create_option(  # noqa: PLR0913
        self,
        name,
        value,
        label,
        _selected,
        index,
        subindex=None,
        attrs=None,
    ):
        # if there are *any* options, set them as selected="selected", as
        # that is how we specify initial values while using ajax data
        # https://github.com/codingjoe/django-select2/issues/4#issuecomment-2106265109
        selected = "selected"
        return super().create_option(
            name,
            value,
            label,
            selected,
            index,
            subindex,
            attrs,
        )

    def value_from_datadict(self, data, files, name):
        """Create objects for missing tags.

        Return comma separates string of tags.
        """
        values = set(super().value_from_datadict(data, files, name))
        names = self.queryset.filter(name__in=list(values)).values_list(
            "name",
            flat=True,
        )
        names = set(map(str, names))
        cleaned_values = list(names)
        # if a value is not in names (tag with name does
        # not exists), it has to be created
        cleaned_values += [
            self.queryset.create(name=val).name for val in (values - names)
        ]
        # django-taggit expects a comma-separated list
        return ",".join(cleaned_values)


class StockItemForm(ModelForm):
    class Meta:
        model = StockItem
        fields = [
            "name",
            "count",
            "count_unit",
            "comment",
            "tags",
            "category",
            "project",
            "storage",
            "orderitems",
            "attachments",
            "thumbnail",
        ]

        widgets = {
            "tags": TagChoices(
                data_view="stockitem-tag-auto-json",
                attrs={
                    "data-placeholder": "...",
                    "data-token-separators": ",",
                },
            ),
            "name": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, initial_tags=None, **kwargs):
        if initial_tags is None:
            initial_tags = []

        # "count_unit": forms.Select(choices=[(1, 2), (3, 4), (5, 6)]),

        # We need this so self.fields is populated
        super().__init__(*args, **kwargs)

        # logger.debug(dir(self.fields["count_unit"]))

        units = (
            StockItem.objects.order_by()
            .values_list("count_unit", flat=True)
            .distinct()
        )
        # In a fresh db, we may not have any units
        if not units:
            units = ["units"]

        self.fields["count_unit"].widget = forms.Select(
            choices=[(x, x) for x in units]
        )

        self.fields["count_unit"].initial = "items"

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-2"
        self.helper.field_class = "col-10"

        self.fields["tags"].widget.choices = initial_tags
        self.fields["comment"].widget.attrs["rows"] = 2

        self.helper.layout = Layout(
            FieldWithButtons(
                "name",
                StrictButton(
                    bs_icon("keyboard"),
                    css_id="keyboard_btn",
                    css_class="btn btn-primary",
                    data_bs_toggle="modal",
                    data_bs_target="#keyboardModel",
                ),
            ),
            Row(
                Column(
                    HTML("Count"),
                    css_class="col-2",  # Column 2
                ),
                Column(
                    Div(
                        Field(
                            "count",
                            css_class="field-count",
                            template="crispy_raw_field.html",
                        ),
                        FieldWithButtons(
                            Field(
                                "count_unit",
                                css_class="field-count-unit",
                                template="crispy_raw_field.html",
                            ),
                            StrictButton(
                                bs_icon("plus-circle"),
                                css_id="unit_btn",
                                css_class="btn btn-primary",
                            ),
                            input_size="fwb-1 w-50",
                            css_class="fwb-2",
                            template="crispy_raw_field.html",
                        ),
                        css_class="input-group",
                    ),
                    css_class="col-10",  # Column 2
                ),
                css_class="mb-3",
            ),
            Field("tags"),
            Field("comment"),
            HTML("""<div id="div_id_thumbnail_render" class="mb-3 row">
                 <div id="div_id_thumbnail_render" class="col-2">
                    Rotate thumbnail
                 </div>
                 <div id="div_id_thumbnail_render" class="col-10">
            """),
            StrictButton(
                bs_icon("arrow-clockwise"),
                css_id="btn_rotate_90_right",
                css_class="btn btn-primary ps-4 pe-4",
            ),
            StrictButton(
                bs_icon("arrow-repeat"),
                css_id="btn_rotate_180",
                css_class="btn btn-primary ps-4 pe-4",
            ),
            StrictButton(
                bs_icon("arrow-counterclockwise"),
                css_id="btn_rotate_90_left",
                css_class="btn btn-primary ps-4 pe-4",
            ),
            StrictButton(
                bs_icon("x-circle"),
                css_id="id_thumbnail_btnclear",
                css_class="btn btn-primary ps-4 pe-4",
            ),
            HTML("""
                 </div>
                 </div>"""),
            Field("thumbnail"),
            HTML("""
                    <div id="dropzone">
                    
                        <div id="div_id_thumbnail_render" class="mb-3 row">
                            <div class="col-form-label pt-0 col-2">
                                {% if stockitem.thumbnail_url %}
                                    Thumbnail (Stock item)
                                {% elif orderitem.thumbnail %}
                                    Thumbnail (Order item)
                                {% endif %}
                            </div>
                            <div class="col-10">
                                {% if stockitem.thumbnail_url %}
                                    <img alt="Image thumbnail"
                                        src="{{ stockitem.thumbnail_url }}"
                                        class="img-fluid"
                                        style="max-width: 50%" id="thumbnail" />
                                {% elif orderitem.thumbnail %}
                                    <img alt="Image thumbnail"
                                        src="{{ orderitem.thumbnail.url }}"
                                        class="img-fluid"
                                        style="max-width: 50%" id="thumbnail" />
                                {% else %}
                                    <!-- Hidden img for preview -->
                                    <img alt="Image thumbnail"
                                        src="#"
                                        class="img-fluid d-none"
                                        style="max-width: 50%" id="thumbnail" />
                                {% endif %}
                            </div>
                        </div>
                    
            """),
            # We already have this is we have a image set :thinking_face:
            HTML("</div><!-- id=dropzone -->"),
            Field("category"),
            Field("project"),
            Field("storage"),
            Field("orderitems"),
            Field("attachments"),
            HTML('<p class="text-end">'),
            Submit("submit", "{{ title }}"),
            HTML("</p>"),
        )
