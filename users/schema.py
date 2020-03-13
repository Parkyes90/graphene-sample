import graphene

from .models import User
from .types import UserArrayType, UserType


class Query:
    all_users = graphene.Field(UserArrayType, page=graphene.Int())
    user = graphene.Field(UserType, pk=graphene.ID(required=True))

    def resolve_all_users(self, info, page):
        if page < 1:
            page = 1
        page_size = 20
        queryset = User.objects.all()
        total = queryset.count()
        start = (page - 1) * page_size
        end = page * page_size
        return UserArrayType(arr=queryset[start:end], total=total)

    def resolve_user(self, info, pk):
        return User.objects.get(pk=pk)
