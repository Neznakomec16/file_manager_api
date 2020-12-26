from pathlib import Path

from django.views import View
from rest_framework import viewsets, permissions
from rest_framework.exceptions import APIException, MethodNotAllowed
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response

from file_storage.models import File
from hashlib import sha256
from file_storage.serializers import FileSerializer


class GetFileView(View):
    def get(self, request, file_hash):
        print(file_hash)


class FilesViewSet(viewsets.ModelViewSet):
    tempdir = Path('/tmp/file_storage_tempdir')
    target_dir = Path(Path.home(), 'file_manager')

    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def perform_create(self, serializer: FileSerializer):
        if not self.tempdir.exists():
            self.tempdir.mkdir(parents=True)
        if not serializer.is_valid():
            return APIException('Something wrong due to uploading. Data is not valid')

        file = serializer.validated_data.get('file')
        temp_file = Path(self.tempdir, file.name)
        with open(Path(self.tempdir, file.name).as_posix(), 'wb') as f:
            chunk_hashes = []
            for chunk in file.chunks():
                f.write(chunk)
                chunk_hashes.append(sha256(chunk).hexdigest())
        file_hash = sha256(''.join(chunk_hashes).encode()).hexdigest()
        target_path = self.target_dir.joinpath(file_hash[:2], file_hash)
        if not target_path.parent.exists():
            target_path.parent.mkdir(parents=True)
        temp_file.replace(target_path)
        serializer.save(file_hash=file_hash, file_path=target_path.as_posix())
