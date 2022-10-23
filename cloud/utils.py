import math
from rest_framework_simplejwt.tokens import RefreshToken
from cloud.models import History, CustomUser
import datetime


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {'refresh': str(refresh), 'access': str(refresh.access_token)}


def create_history(user_id, action_type, action_name, folder, file):
    user = CustomUser.objects.get(id=user_id)
    History.objects.create(user=user,
                           action=action_type,
                           time=datetime.datetime.now(),
                           date=datetime.date.today(),
                           name=action_name,
                           folder=folder,
                           file=file)
