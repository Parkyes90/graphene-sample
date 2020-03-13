import graphene
from graphene_django import DjangoObjectType

from rooms.models import Room


class RoomType(DjangoObjectType):
    class Meta:
        model = Room


class Query(graphene.ObjectType):
    all_rooms = graphene.List(RoomType)

    def resolve_all_rooms(self, info):
        return Room.objects.all()


class Mutation:
    pass


schema = graphene.Schema(query=Query)
