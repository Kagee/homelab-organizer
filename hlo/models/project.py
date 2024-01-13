from . import CommonTreeModel


class Project(CommonTreeModel):
    def __str__(self):
        return str(self.name)
