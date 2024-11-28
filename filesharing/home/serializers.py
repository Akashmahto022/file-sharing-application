from rest_framework import serializers
from .models import *
import shutil

class FileSerializer(serializers.Serializer):
    files = serializers.ListField(
        child = serializers.FileField(max_length = 100000, allow_empty_file = False, use_url = False)
    )
    
    folder = serializers.CharField(required = False)
    
    def zip_files(self, folder):
        shutil.make_archive(folder, 'zip', folder)
    
    def create(self, validated_date):
        folder = Folder.objects.create()
        files = validated_date.pop('files')
        files_objs = []
        for file in files:
            files_obj = Files.objects.create(folder = folder, file = file)
            files_objs.append(files_obj)
        
        self.zip_files(folder.uid)
        
        return {'files': {}, 'folder': str(folder.uid)}