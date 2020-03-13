import graphene
from graphene_django import DjangoObjectType

from .models import Room


class RoomType(DjangoObjectType):

    is_fav = graphene.Boolean()

    class Meta:
        model = Room

    def resolve_is_fav(self, info):
        user = info.context.user
        if not user.is_authenticated:
            return False

        return self in user.favs.all()


class RoomListType(graphene.ObjectType):

    arr = graphene.List(RoomType)
    total = graphene.Int()
