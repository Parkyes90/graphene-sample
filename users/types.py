import graphene
from graphene_django import DjangoObjectType

from .models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ("password", "is_superuser", "last_login", "is_staff")


class UserArrayType(graphene.ObjectType):
    arr = graphene.List(UserType)
    total = graphene.Int()