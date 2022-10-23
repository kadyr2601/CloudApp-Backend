from django.contrib import admin
from cloud.models import Folder, Company, File, History, CustomUser

admin.site.register(Company)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'name')
    list_filter = ('date', )


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ('company', 'name')


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'file_size', 'folder')

