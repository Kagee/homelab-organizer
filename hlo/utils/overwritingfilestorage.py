from django.conf import settings
from django.core.files.storage import FileSystemStorage


class OverwritingFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, *_args, **_kwargs):
        if self.exists(name):
            (settings.MEDIA_ROOT / name).unlink()
        return name
