from .commontree import CommonTreeModel


class Category(CommonTreeModel):
    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return str(self.name)
