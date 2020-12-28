from pathlib import Path

from django.http import HttpResponse
from rest_framework import viewsets, permissions
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from file_storage.models import File
from file_storage.serializers import FileSerializer
from file_storage.utils import create_dir_if_not_exists, get_sha256_hash
from main_app.settings import TEMP_DIR_PATH, TARGET_DIR_PATH


class FilesViewSet(viewsets.ModelViewSet):
    tempdir = TEMP_DIR_PATH
    target_dir = TARGET_DIR_PATH

    queryset = File.objects.all()
    serializer_class = FileSerializer
    authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated, ]
    http_method_names = ['get', 'post', 'delete']

    def perform_create(self, serializer: FileSerializer):
        create_dir_if_not_exists(self.tempdir)
        if not serializer.is_valid():
            return APIException('Something wrong due to uploading. Data is not valid')

        file = serializer.validated_data.get('file')
        temp_file = Path(self.tempdir, file.name)
        with open(Path(self.tempdir, file.name).as_posix(), 'wb') as f:
            chunk_hashes = []
            for chunk in file.chunks():
                f.write(chunk)
                # Чтобы сократить потребляемую память, берём хеш от каждого чанка.
                chunk_hashes.append(get_sha256_hash(chunk))
        # после берём хеш от полученных хешей
        file_hash = get_sha256_hash(''.join(chunk_hashes).encode())
        target_path = self.target_dir.joinpath(file_hash[:2], file_hash)
        create_dir_if_not_exists(target_path.parent)
        temp_file.replace(target_path)
        serializer.save(file_hash=file_hash, file_path=target_path.as_posix())

    def retrieve(self, request, *args, **kwargs):
        file_hash = kwargs.get('pk')
        file = File.objects.filter(file_hash=file_hash)
        if file.exists():
            file = file[0]
            if not Path(file.file_path).exists():
                # если запись о файле есть в бд, но сам файл удалили из хранилища
                file.delete()
                return Response('File was deleted from storage')
            with open(file.file_path, 'rb') as f:
                file_body = f.read()
            response = HttpResponse(file_body)
            response['Content-Disposition'] = f'attachment; filename="{file.file_hash}"'
            return response
        else:
            return Response('File not found')