from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        user = self.model(email=self.normalize_email(email), first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.model(email=self.normalize_email(email))
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=85, unique=True)
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Company(models.Model):
    name = models.CharField(max_length=1024)

    def __str__(self):
        return self.name


class Folder(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_folders')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='folder_user')
    name = models.CharField(max_length=1024)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class File(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='file_user')
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='folder_files')
    file_size = models.CharField(max_length=256)
    file = models.FileField(upload_to='Cloud/')
    name = models.CharField(max_length=1024)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


ACTIONS = (
    ('created', 'Created'),
    ('uploaded', 'Uploaded'),
    ('deleted', 'Deleted'),
    ('downloaded', 'Downloaded'),
    ('looked', 'Looked'),
    ('authenticate', 'Authenticate'),
)


class History(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    action = models.CharField(choices=ACTIONS, max_length=256)
    name = models.CharField(max_length=2056, null=True, blank=True)
    folder = models.BooleanField(default=False)
    file = models.BooleanField(default=False)
    date = models.DateField()
    time = models.TimeField()

    class Meta:
        ordering = ('-id', )
