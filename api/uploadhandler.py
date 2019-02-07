from django.core.files.uploadhandler import TemporaryFileUploadHandler

from .models import Upload


class TrackedFileUploadHandler(TemporaryFileUploadHandler):
    """
    Upload handler with monitoring.
    """

    def new_file(self, *args, **kwargs):
        super().new_file(*args, **kwargs)
        # Небольшой воркараунд - иногда прилетает tuple
        if isinstance(args[1], tuple):
            file_name = args[1][0]
        else:
            file_name = args[1]

        self.upload = Upload.objects.create(
            file_name=file_name,
            state=Upload.ACTIVE_STATE
        )

    def upload_complete(self):
        self.upload.file_size = self.file.size
        self.upload.file_name = self.file_name
        self.upload.state = Upload.COMPLETED_STATE
        self.upload.save()
