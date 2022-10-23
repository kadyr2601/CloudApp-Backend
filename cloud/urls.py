from django.urls import path
from cloud.views import LoginView, GetMe, HistoryList, CompanyList, CompanyFolders, FolderFiles, FileDelete,\
                        FileCreate, DownloadHandler, UserRegistration, FileSearch


urlpatterns = [
    path('login/', LoginView.as_view()),
    path('registration/', UserRegistration.as_view()),
    path('get-me/', GetMe.as_view()),
    path('history-list/', HistoryList.as_view()),
    path('company-list/', CompanyList.as_view()),
    path('company/<pk>/', CompanyFolders.as_view()),
    path('folder/<pk>/', FolderFiles.as_view()),
    path('file-delete/<pk>/', FileDelete.as_view()),
    path('file-create/', FileCreate.as_view()),
    path('file-action/', DownloadHandler.as_view()),
    path('file-search/', FileSearch.as_view()),
]
