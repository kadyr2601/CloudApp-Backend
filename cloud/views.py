from django.contrib.auth import authenticate, login
from rest_framework import status, filters
from rest_framework.generics import CreateAPIView, ListAPIView, get_object_or_404, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from cloud.serializers import FileSerializer, FolderSerializer, FolderSerializerRetrieve, RegistrationSerializer, \
    PasswordChangeSerializer, UserSerializer, HistorySerializer, CompanySerializerList,\
    CompanySerializer, FolderSerializerList
from cloud.models import Folder, CustomUser, File, History, Company
from cloud.utils import convert_size, get_tokens_for_user, create_history


class UserRegistration(CreateAPIView):
    serializer_class = RegistrationSerializer


class LoginView(APIView):
    def post(self, request):
        email_data = request.data['email']
        password_data = request.data['password']
        get_user = CustomUser.objects.get(email=email_data)
        validate_password = get_user.check_password(password_data)
        if validate_password:
            user = authenticate(request, email=email_data, password=password_data)
            login(request, user)
            auth_data = get_tokens_for_user(request.user)
            create_history(user.id, 'authenticate', None, folder=False, file=False)
            return Response({**auth_data}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class GetMe(APIView):
    def get(self, request):
        user = get_object_or_404(CustomUser, id=request.user.id)
        file_count = File.objects.filter(user=user).count()
        folder_count = Folder.objects.filter(user=user).count()
        if user.is_admin:
            data = {
                    "id": user.id,
                    "email": user.email,
                    "name": user.first_name,
                    "surname": user.last_name,
                    "folder_count": folder_count,
                    "file_count": file_count,
                    "is_admin": True
                }
            serializer = UserSerializer(data)
            return Response(serializer.data)
        else:
            data = {
                "id": user.id,
                "email": user.email,
                "name": user.first_name,
                "surname": user.last_name,
                "folder_count": folder_count,
                "file_count": file_count,
            }
            serializer = UserSerializer(data)
            return Response(serializer.data)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = PasswordChangeSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_201_CREATED)


class HistoryList(ListAPIView):
    queryset = History.objects.all()[:50]
    serializer_class = HistorySerializer


class CompanyList(ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializerList


class CompanyFolders(RetrieveAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        create_history(request.user.id, 'looked', obj.name, False, False)
        return super().retrieve(request, *args, **kwargs)


class FolderFiles(RetrieveAPIView):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializerList

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        create_history(request.user.id, 'looked', obj.name, True, False)
        return super().retrieve(request, *args, **kwargs)


class FileSearch(ListAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]

    # def get_queryset(self):
    #     return Folder.objects.filter(user=self.request.user.id)


class FileCreate(APIView):
    def post(self, request):
        files = request.FILES.getlist('files')
        folder_id = request.data['folder']
        user = CustomUser.objects.get(id=request.user.id)
        folder = Folder.objects.get(id=folder_id)
        for i in files:
            file = File.objects.create(
                user=user,
                folder=folder,
                file_size=convert_size(i.size),
                file=i,
                name=i.name
            )
            create_history(user.id, 'uploaded', file.name, False, True)
        return Response(status=status.HTTP_201_CREATED)


class FileDelete(APIView):
    def post(self, request, pk):
        file = File.objects.get(pk=pk)
        file.delete()
        create_history(request.user.id, 'deleted', file.name, False, True)
        return Response({"successfully deleted"}, status=status.HTTP_204_NO_CONTENT)


class DownloadHandler(APIView):
    def post(self, request):
        file_name = request.data['file_name']
        action_type = request.data['action_type']
        if action_type == 'downloaded':
            create_history(request.user.id, 'downloaded', file_name, False, True)
            return Response({"successfully downloaded"}, status=status.HTTP_200_OK)
        elif action_type == 'uploaded':
            create_history(request.user.id, 'uploaded', file_name, False, True)
            return Response({"successfully downloaded"}, status=status.HTTP_201_CREATED)
