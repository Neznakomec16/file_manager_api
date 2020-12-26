from rest_framework import serializers

from file_storage.models import File


class FileSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    create_date = serializers.DateTimeField(read_only=True)
    file = serializers.FileField(allow_empty_file=False, max_length=10**9, write_only=True)
    file_hash = serializers.CharField(max_length=64, read_only=True)

    class Meta:
        model = File
        fields = ['id', 'file', 'create_date', 'file_hash', ]

    def create(self, validated_data):
        validated_data.pop('file')
        file, created = File.objects.get_or_create(**validated_data)
        return file
