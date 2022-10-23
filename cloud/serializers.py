from rest_framework import serializers
from cloud.models import Folder, File, CustomUser, History, Company


class UserSerializer(serializers.Serializer):
    folder_count = serializers.IntegerField(required=False)
    file_count = serializers.IntegerField(required=False)
    id = serializers.IntegerField()
    email = serializers.EmailField()
    name = serializers.CharField(max_length=512)
    surname = serializers.CharField(max_length=512)
    is_admin = serializers.BooleanField(default=False)


class CompanySerializerList(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    company_folders = FolderSerializer(many=True, read_only=True)
    folder_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Company
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(CompanySerializer, self).to_representation(instance)
        representation['folder_count'] = Folder.objects.filter(company=instance.id).count()
        return representation


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(HistorySerializer, self).to_representation(instance)
        representation['user'] = instance.user.email
        representation['date'] = instance.date.strftime('%d-%m-%Y')
        representation['time'] = instance.time.strftime('%H:%M')
        return representation


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        user = CustomUser.objects.create(email=self.validated_data['email'],
                                         first_name=self.validated_data['first_name'],
                                         last_name=self.validated_data['last_name'])
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={"input_type": "password"}, required=True)
    new_password = serializers.CharField(style={"input_type": "password"}, required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError({'current_password': 'Does not match'})
        return value


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(FileSerializer, self).to_representation(instance)
        representation['created'] = instance.created.strftime('%d-%m-%Y')
        return representation


class FolderSerializerList(serializers.ModelSerializer):
    file_count = serializers.IntegerField(read_only=True)
    folder_files = FileSerializer(many=True)

    class Meta:
        model = Folder
        fields = ['folder_files', 'file_count', 'company', 'name', 'id']
        depth = 1

    def to_representation(self, instance):
        representation = super(FolderSerializerList, self).to_representation(instance)
        representation['file_count'] = File.objects.filter(folder=instance.id).count()
        return representation


class FolderSerializerRetrieve(serializers.ModelSerializer):
    folder = FileSerializer(many=True)
    file_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Folder
        fields = '__all__'
        depth = 1

    def to_representation(self, instance):
        representation = super(FolderSerializerRetrieve, self).to_representation(instance)
        representation['created'] = instance.created.strftime('%d-%m-%Y')
        representation['file_count'] = File.objects.filter(folder=instance.id).count()
        return representation
