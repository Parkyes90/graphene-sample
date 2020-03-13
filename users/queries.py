from .models import User
from .types import UserArrayType


def resolve_user(root, info, pk):
    return User.objects.get(pk=pk)


def resolve_all_users(root, info, page):
    if page < 1:
        page = 1
    page_size = 20
    queryset = User.objects.all()
    total = queryset.count()
    start = (page - 1) * page_size
    end = page * page_size
    return UserArrayType(arr=queryset[start:end], total=total)


def resolve_me(root, info):
    user = info.context.user
    if not user.is_authenticated:
        raise Exception("You need to be logged in")
    return user
